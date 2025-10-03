#!/usr/bin/env python3
"""
🛠️ Script de configuración e instalación del sistema de scraping
Configura el entorno y valida la instalación
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ es requerido")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        sys.exit(1)

def create_directories():
    """Crea los directorios necesarios"""
    directories = [
        "data",
        "data/backups", 
        "logs",
        "metrics",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Directorio creado: {directory}")

def create_config_file():
    """Crea archivo de configuración"""
    config = {
        "scraping": {
            "max_requests_per_second": 0.5,
            "user_agent": "BilforsikringBot/1.0 (+https://bilforsikring.dk/bot-info)",
            "request_timeout": 30,
            "max_retries": 3,
            "retry_delay": 5,
            "respect_robots_txt": True,
            "cache_duration_hours": 24
        },
        "targets": {
            "bilforsikring": [
                "https://www.tryg.dk/forsikring/bil",
                "https://www.topdanmark.dk/forsikring/bil",
                "https://www.if.dk/forsikring/bil",
                "https://www.gf.dk/bil"
            ],
            "leasing": [
                "https://www.leaseplan.dk/privatleasing",
                "https://www.aldautomotive.dk/privatleasing",
                "https://www.tesla.com/da_dk/model3/design"
            ]
        },
        "notifications": {
            "email_enabled": False,
            "webhook_enabled": False,
            "log_level": "INFO"
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("⚙️ Archivo de configuración creado: config.json")

def create_test_files():
    """Crea archivos de test básicos"""
    test_content = '''#!/usr/bin/env python3
"""
Tests básicos para el sistema de scraping
"""

import pytest
import asyncio
from main_scraper import EthicalScraper, ScrapingConfig

@pytest.mark.asyncio
async def test_scraper_initialization():
    """Test de inicialización del scraper"""
    config = ScrapingConfig()
    async with EthicalScraper(config) as scraper:
        assert scraper is not None

@pytest.mark.asyncio
async def test_rate_limiting():
    """Test del rate limiting"""
    config = ScrapingConfig(max_requests_per_second=2.0)
    scraper = EthicalScraper(config)
    
    # Test que el rate limiter funciona
    start_time = asyncio.get_event_loop().time()
    await scraper.rate_limiter.wait_if_needed()
    await scraper.rate_limiter.wait_if_needed()
    end_time = asyncio.get_event_loop().time()
    
    # Debería haber esperado al menos 0.5 segundos (1/2 requests per second)
    assert end_time - start_time >= 0.4

def test_data_validation():
    """Test de validación de datos"""
    from main_scraper import DataValidator
    
    validator = DataValidator()
    
    # Test validación de precios
    valid_price = validator.validate_price("399 kr./md")
    assert valid_price is not None
    assert valid_price['value'] == 399.0
    
    # Test validación de URLs
    assert validator.validate_url("https://www.tryg.dk") == True
    assert validator.validate_url("invalid-url") == False

if __name__ == "__main__":
    pytest.main([__file__])
'''
    
    with open("tests/test_basic.py", "w") as f:
        f.write(test_content)
    
    print("🧪 Archivos de test creados")

def create_docker_files():
    """Crea archivos Docker para containerización"""
    dockerfile_content = '''FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p data logs metrics

# Ejecutar scraper
CMD ["python", "run_scraper.py", "--type", "all"]
'''
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    docker_compose_content = '''version: '3.8'

services:
  scraper:
    build: .
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - SCRAPER_ENV=production
      - LOG_LEVEL=INFO
    restart: unless-stopped
    
  # Opcional: Base de datos para métricas
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: scraper_metrics
      POSTGRES_USER: scraper
      POSTGRES_PASSWORD: scraper_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
'''
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content)
    
    print("🐳 Archivos Docker creados")

def run_basic_test():
    """Ejecuta un test básico del sistema"""
    print("🧪 Ejecutando test básico...")
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/test_basic.py", "-v"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tests básicos pasaron correctamente")
        else:
            print(f"⚠️ Algunos tests fallaron: {result.stdout}")
    except Exception as e:
        print(f"⚠️ No se pudieron ejecutar los tests: {e}")

def main():
    """Función principal de configuración"""
    print("🛠️ Configurando sistema de scraping ético...")
    print("="*50)
    
    # Verificar Python
    check_python_version()
    
    # Crear directorios
    create_directories()
    
    # Instalar dependencias
    install_dependencies()
    
    # Crear archivos de configuración
    create_config_file()
    
    # Crear archivos de test
    create_test_files()
    
    # Crear archivos Docker
    create_docker_files()
    
    # Ejecutar test básico
    run_basic_test()
    
    print("\n" + "="*50)
    print("🎉 Configuración completada exitosamente!")
    print("\n📋 Próximos pasos:")
    print("1. Revisar config.json y ajustar según necesidades")
    print("2. Ejecutar: python run_scraper.py --type test")
    print("3. Para scraping completo: python run_scraper.py --type all")
    print("4. Para automatización: configurar GitHub Actions")
    print("\n📚 Documentación: README.md")
    print("="*50)

if __name__ == "__main__":
    main()
