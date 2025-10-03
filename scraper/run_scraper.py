#!/usr/bin/env python3
"""
🚀 Script principal para ejecutar el sistema de scraping
Punto de entrada para el sistema de scraping ético
"""

import asyncio
import argparse
import logging
import sys
import os
from datetime import datetime
from typing import List

# Añadir el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_scraper import EthicalScraper, ScrapingConfig, DataManager
from bilforsikring_scraper import BilforsikringScraper
from leasing_scraper import LeasingScraper

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'scraper_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScrapingOrchestrator:
    """Orquestador principal del sistema de scraping"""
    
    def __init__(self):
        self.config = ScrapingConfig()
        self.data_manager = DataManager()
        self.results = {
            'bilforsikring': [],
            'leasing': [],
            'errors': [],
            'stats': {
                'start_time': None,
                'end_time': None,
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0
            }
        }
    
    async def run_scraping(self, scrape_type: str = 'all'):
        """Ejecuta el scraping según el tipo especificado"""
        logger.info(f"🚀 Starting scraping process: {scrape_type}")
        self.results['stats']['start_time'] = datetime.now()
        
        try:
            async with EthicalScraper(self.config) as scraper:
                if scrape_type in ['all', 'bilforsikring']:
                    await self._scrape_bilforsikring(scraper)
                
                if scrape_type in ['all', 'leasing']:
                    await self._scrape_leasing(scraper)
                
                if scrape_type == 'test':
                    await self._run_tests(scraper)
                
        except Exception as e:
            logger.error(f"❌ Critical error in scraping process: {e}")
            self.results['errors'].append(str(e))
        
        finally:
            self.results['stats']['end_time'] = datetime.now()
            await self._save_results()
            self._print_summary()
    
    async def _scrape_bilforsikring(self, scraper):
        """Scraping de seguros de auto"""
        logger.info("🏢 Starting bilforsikring scraping...")
        
        try:
            bilforsikring_scraper = BilforsikringScraper(scraper)
            data = await bilforsikring_scraper.scrape_all_providers()
            
            if data:
                # Convertir a formato JSON
                json_data = []
                for item in data:
                    json_data.append({
                        'udbyder': item.udbyder,
                        'produkt': item.produkt,
                        'pris_mdr': item.pris_mdr,
                        'pris_år': item.pris_år,
                        'dækning': item.dækning,
                        'tilvalg': item.tilvalg,
                        'kampagne': item.kampagne,
                        'link': item.link,
                        'last_updated': item.last_updated,
                        'data_source': item.data_source,
                        'reliability_score': item.reliability_score,
                        'additional_info': item.additional_info
                    })
                
                self.results['bilforsikring'] = json_data
                self.data_manager.save_data('bilforsikring.json', json_data)
                logger.info(f"✅ Bilforsikring scraping completed: {len(json_data)} products")
            else:
                logger.warning("⚠️ No bilforsikring data found")
                
        except Exception as e:
            logger.error(f"❌ Error in bilforsikring scraping: {e}")
            self.results['errors'].append(f"Bilforsikring: {str(e)}")
    
    async def _scrape_leasing(self, scraper):
        """Scraping de leasing"""
        logger.info("🚗 Starting leasing scraping...")
        
        try:
            leasing_scraper = LeasingScraper(scraper)
            data = await leasing_scraper.scrape_all_providers()
            
            if data:
                # Convertir a formato JSON
                json_data = []
                for item in data:
                    json_data.append({
                        'mærke': item.mærke,
                        'model': item.model,
                        'variant': item.variant,
                        'pris_mdr': item.pris_mdr,
                        'udbetaling': item.udbetaling,
                        'løbetid': item.løbetid,
                        'km_år': item.km_år,
                        'kampagne': item.kampagne,
                        'link': item.link,
                        'last_updated': item.last_updated,
                        'data_source': item.data_source,
                        'reliability_score': item.reliability_score,
                        'additional_info': item.additional_info
                    })
                
                self.results['leasing'] = json_data
                self.data_manager.save_data('leasing.json', json_data)
                logger.info(f"✅ Leasing scraping completed: {len(json_data)} vehicles")
            else:
                logger.warning("⚠️ No leasing data found")
                
        except Exception as e:
            logger.error(f"❌ Error in leasing scraping: {e}")
            self.results['errors'].append(f"Leasing: {str(e)}")
    
    async def _run_tests(self, scraper):
        """Ejecuta tests del sistema"""
        logger.info("🧪 Running scraper tests...")
        
        # Test básico de conectividad
        test_url = "https://www.tryg.dk"
        content = await scraper.fetch_page(test_url)
        
        if content:
            logger.info("✅ Basic connectivity test passed")
        else:
            logger.error("❌ Basic connectivity test failed")
            self.results['errors'].append("Connectivity test failed")
    
    async def _save_results(self):
        """Guarda los resultados del scraping"""
        try:
            # Guardar métricas
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'scrape_type': 'all',
                'results': self.results,
                'summary': {
                    'total_bilforsikring': len(self.results['bilforsikring']),
                    'total_leasing': len(self.results['leasing']),
                    'total_errors': len(self.results['errors']),
                    'duration_seconds': (
                        self.results['stats']['end_time'] - self.results['stats']['start_time']
                    ).total_seconds() if self.results['stats']['end_time'] else 0
                }
            }
            
            self.data_manager.save_data('scraping_metrics.json', [metrics])
            logger.info("📊 Metrics saved successfully")
            
        except Exception as e:
            logger.error(f"❌ Error saving results: {e}")
    
    def _print_summary(self):
        """Imprime resumen del scraping"""
        stats = self.results['stats']
        duration = (stats['end_time'] - stats['start_time']).total_seconds() if stats['end_time'] else 0
        
        print("\n" + "="*60)
        print("📊 SCRAPING SUMMARY")
        print("="*60)
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"🏢 Bilforsikring: {len(self.results['bilforsikring'])} products")
        print(f"🚗 Leasing: {len(self.results['leasing'])} vehicles")
        print(f"❌ Errors: {len(self.results['errors'])}")
        
        if self.results['errors']:
            print("\n🚨 ERRORS:")
            for error in self.results['errors']:
                print(f"   - {error}")
        
        print("="*60)

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Bilforsikring.dk Ethical Scraper')
    parser.add_argument(
        '--type', 
        choices=['all', 'bilforsikring', 'leasing', 'test'],
        default='all',
        help='Type of scraping to perform'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Crear y ejecutar orquestador
    orchestrator = ScrapingOrchestrator()
    
    try:
        asyncio.run(orchestrator.run_scraping(args.type))
    except KeyboardInterrupt:
        logger.info("🛑 Scraping interrupted by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
