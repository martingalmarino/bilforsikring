#!/usr/bin/env python3
"""
🕷️ Sistema de Scraping Ético - Bilforsikring.dk
Scraper principal con rate limiting y respeto a robots.txt
"""

import asyncio
import aiohttp
import time
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import random

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ScrapingConfig:
    """Configuración del sistema de scraping"""
    max_requests_per_second: float = 0.5  # Máximo 1 request cada 2 segundos
    user_agent: str = "BilforsikringBot/1.0 (+https://bilforsikring.dk/bot-info)"
    request_timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 5
    respect_robots_txt: bool = True
    cache_duration_hours: int = 24

class RateLimiter:
    """Rate limiter para controlar la velocidad de requests"""
    
    def __init__(self, max_requests_per_second: float):
        self.max_requests_per_second = max_requests_per_second
        self.min_interval = 1.0 / max_requests_per_second
        self.last_request_time = 0.0
    
    async def wait_if_needed(self):
        """Espera si es necesario para respetar el rate limit"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()

class RobotsTxtChecker:
    """Verificador de robots.txt para respetar las directivas"""
    
    def __init__(self):
        self.robots_cache = {}
    
    def can_fetch(self, url: str, user_agent: str) -> bool:
        """Verifica si podemos hacer scraping de la URL según robots.txt"""
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            if base_url not in self.robots_cache:
                robots_url = urljoin(base_url, '/robots.txt')
                rp = RobotFileParser()
                rp.set_url(robots_url)
                rp.read()
                self.robots_cache[base_url] = rp
            
            return self.robots_cache[base_url].can_fetch(user_agent, url)
        except Exception as e:
            logger.warning(f"Error checking robots.txt for {url}: {e}")
            return True  # Si no podemos verificar, asumimos que está permitido

class EthicalScraper:
    """Scraper principal con principios éticos"""
    
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.rate_limiter = RateLimiter(config.max_requests_per_second)
        self.robots_checker = RobotsTxtChecker()
        self.session = None
        self.cache = {}
    
    async def __aenter__(self):
        """Context manager entry"""
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=2)
        timeout = aiohttp.ClientTimeout(total=self.config.request_timeout)
        headers = {
            'User-Agent': self.config.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'da-DK,da;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.session:
            await self.session.close()
    
    async def fetch_page(self, url: str, retries: int = None) -> Optional[str]:
        """Obtiene una página web respetando rate limits y robots.txt"""
        if retries is None:
            retries = self.config.max_retries
        
        # Verificar robots.txt si está habilitado
        if self.config.respect_robots_txt:
            if not self.robots_checker.can_fetch(url, self.config.user_agent):
                logger.warning(f"Robots.txt disallows scraping: {url}")
                return None
        
        # Verificar cache
        cache_key = f"{url}_{datetime.now().strftime('%Y%m%d%H')}"
        if cache_key in self.cache:
            logger.info(f"Using cached data for: {url}")
            return self.cache[cache_key]
        
        for attempt in range(retries + 1):
            try:
                # Rate limiting
                await self.rate_limiter.wait_if_needed()
                
                # Añadir jitter aleatorio para parecer más humano
                jitter = random.uniform(0.1, 0.5)
                await asyncio.sleep(jitter)
                
                logger.info(f"Fetching: {url} (attempt {attempt + 1})")
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        # Cachear el resultado
                        self.cache[cache_key] = content
                        return content
                    elif response.status == 429:  # Too Many Requests
                        wait_time = self.config.retry_delay * (2 ** attempt)
                        logger.warning(f"Rate limited, waiting {wait_time}s")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.warning(f"HTTP {response.status} for {url}")
                        
            except asyncio.TimeoutError:
                logger.warning(f"Timeout for {url} (attempt {attempt + 1})")
            except Exception as e:
                logger.error(f"Error fetching {url}: {e}")
            
            if attempt < retries:
                wait_time = self.config.retry_delay * (2 ** attempt)
                logger.info(f"Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
        
        logger.error(f"Failed to fetch {url} after {retries + 1} attempts")
        return None

class DataValidator:
    """Validador y limpiador de datos"""
    
    @staticmethod
    def validate_price(price_str: str) -> Optional[Dict]:
        """Valida y normaliza precios"""
        if not price_str:
            return None
        
        # Extraer número y moneda
        import re
        price_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:kr|DKK)', price_str, re.IGNORECASE)
        if price_match:
            price_value = float(price_match.group(1).replace(',', '.'))
            return {
                'value': price_value,
                'currency': 'DKK',
                'formatted': f"{price_value:,.0f} kr."
            }
        return None
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Valida URLs"""
        try:
            from urllib.parse import urlparse
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Limpia texto de caracteres extraños"""
        if not text:
            return ""
        return ' '.join(text.split())  # Normaliza espacios

class DataManager:
    """Gestor de datos con backup y versionado"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(f"{data_dir}/backups", exist_ok=True)
    
    def backup_current_data(self, filename: str):
        """Crea backup de los datos actuales"""
        source_path = f"{self.data_dir}/{filename}"
        if os.path.exists(source_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{self.data_dir}/backups/{filename}_{timestamp}"
            import shutil
            shutil.copy2(source_path, backup_path)
            logger.info(f"Backup created: {backup_path}")
    
    def save_data(self, filename: str, data: List[Dict]):
        """Guarda datos con backup automático"""
        self.backup_current_data(filename)
        
        # Añadir metadatos
        enriched_data = {
            'data': data,
            'metadata': {
                'last_updated': datetime.now().isoformat(),
                'total_records': len(data),
                'scraper_version': '1.0.0'
            }
        }
        
        filepath = f"{self.data_dir}/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(enriched_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Data saved to {filepath} ({len(data)} records)")

async def main():
    """Función principal del scraper"""
    logger.info("🚀 Starting Bilforsikring.dk Ethical Scraper")
    
    config = ScrapingConfig()
    data_manager = DataManager()
    validator = DataValidator()
    
    async with EthicalScraper(config) as scraper:
        # Aquí irían los scrapers específicos
        logger.info("✅ Scraper initialized successfully")
        
        # Ejemplo de uso
        test_url = "https://www.tryg.dk/forsikring/bil"
        content = await scraper.fetch_page(test_url)
        
        if content:
            logger.info(f"✅ Successfully fetched {len(content)} characters from {test_url}")
        else:
            logger.error(f"❌ Failed to fetch {test_url}")

if __name__ == "__main__":
    asyncio.run(main())
