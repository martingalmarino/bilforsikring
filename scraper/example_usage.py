#!/usr/bin/env python3
"""
📖 Ejemplo de uso del sistema de scraping ético
Demuestra cómo usar el scraper de forma segura y efectiva
"""

import asyncio
import json
from datetime import datetime
from main_scraper import EthicalScraper, ScrapingConfig
from bilforsikring_scraper import BilforsikringScraper
from leasing_scraper import LeasingScraper

async def example_basic_scraping():
    """Ejemplo básico de scraping"""
    print("🔍 Ejemplo: Scraping básico")
    print("-" * 40)
    
    # Configuración ética
    config = ScrapingConfig(
        max_requests_per_second=0.5,  # Máximo 1 request cada 2 segundos
        respect_robots_txt=True,      # Respetar robots.txt
        request_timeout=30,           # Timeout de 30 segundos
        max_retries=3                 # Máximo 3 reintentos
    )
    
    async with EthicalScraper(config) as scraper:
        # Ejemplo: Obtener una página
        url = "https://www.tryg.dk/forsikring/bil"
        content = await scraper.fetch_page(url)
        
        if content:
            print(f"✅ Página obtenida: {len(content)} caracteres")
            print(f"📄 Primeros 200 caracteres: {content[:200]}...")
        else:
            print("❌ No se pudo obtener la página")

async def example_bilforsikring_scraping():
    """Ejemplo de scraping de seguros de auto"""
    print("\n🏢 Ejemplo: Scraping de bilforsikring")
    print("-" * 40)
    
    config = ScrapingConfig()
    
    async with EthicalScraper(config) as scraper:
        bilforsikring_scraper = BilforsikringScraper(scraper)
        
        # Scraping de todos los proveedores
        data = await bilforsikring_scraper.scrape_all_providers()
        
        print(f"📊 Productos encontrados: {len(data)}")
        
        for product in data[:2]:  # Mostrar solo los primeros 2
            print(f"\n🏢 {product.udbyder}")
            print(f"   Producto: {product.produkt}")
            print(f"   Precio: {product.pris_mdr}")
            print(f"   Dækning: {product.dækning}")
            print(f"   Tilvalg: {', '.join(product.tilvalg)}")
            print(f"   Kampagne: {product.kampagne}")

async def example_leasing_scraping():
    """Ejemplo de scraping de leasing"""
    print("\n🚗 Ejemplo: Scraping de leasing")
    print("-" * 40)
    
    config = ScrapingConfig()
    
    async with EthicalScraper(config) as scraper:
        leasing_scraper = LeasingScraper(scraper)
        
        # Scraping de todos los proveedores
        data = await leasing_scraper.scrape_all_providers()
        
        print(f"📊 Vehículos encontrados: {len(data)}")
        
        for vehicle in data[:2]:  # Mostrar solo los primeros 2
            print(f"\n🚗 {vehicle.mærke} {vehicle.model}")
            print(f"   Variant: {vehicle.variant}")
            print(f"   Precio: {vehicle.pris_mdr}")
            print(f"   Udbetaling: {vehicle.udbetaling}")
            print(f"   Løbetid: {vehicle.løbetid}")
            print(f"   Kampagne: {vehicle.kampagne}")

async def example_data_validation():
    """Ejemplo de validación de datos"""
    print("\n✅ Ejemplo: Validación de datos")
    print("-" * 40)
    
    from main_scraper import DataValidator
    
    validator = DataValidator()
    
    # Ejemplos de validación de precios
    price_examples = [
        "399 kr./md",
        "2.495 kr./md", 
        "3.995 kr./md",
        "På anmodning",
        "invalid price"
    ]
    
    print("💰 Validación de precios:")
    for price in price_examples:
        result = validator.validate_price(price)
        if result:
            print(f"   ✅ '{price}' → {result['formatted']}")
        else:
            print(f"   ❌ '{price}' → Inválido")
    
    # Ejemplos de validación de URLs
    url_examples = [
        "https://www.tryg.dk/forsikring/bil",
        "https://www.leaseplan.dk/privatleasing",
        "invalid-url",
        "ftp://example.com"
    ]
    
    print("\n🔗 Validación de URLs:")
    for url in url_examples:
        is_valid = validator.validate_url(url)
        status = "✅" if is_valid else "❌"
        print(f"   {status} '{url}'")

async def example_rate_limiting():
    """Ejemplo de rate limiting"""
    print("\n⏱️ Ejemplo: Rate limiting")
    print("-" * 40)
    
    from main_scraper import RateLimiter
    
    # Crear rate limiter (1 request por segundo)
    rate_limiter = RateLimiter(1.0)
    
    print("🔄 Simulando 3 requests con rate limiting...")
    
    for i in range(3):
        start_time = asyncio.get_event_loop().time()
        await rate_limiter.wait_if_needed()
        end_time = asyncio.get_event_loop().time()
        
        elapsed = end_time - start_time
        print(f"   Request {i+1}: {elapsed:.2f}s elapsed")

async def example_robots_txt_check():
    """Ejemplo de verificación de robots.txt"""
    print("\n🤖 Ejemplo: Verificación de robots.txt")
    print("-" * 40)
    
    from main_scraper import RobotsTxtChecker
    
    robots_checker = RobotsTxtChecker()
    user_agent = "BilforsikringBot/1.0"
    
    test_urls = [
        "https://www.tryg.dk/forsikring/bil",
        "https://www.topdanmark.dk/forsikring/bil",
        "https://www.if.dk/forsikring/bil"
    ]
    
    for url in test_urls:
        can_fetch = robots_checker.can_fetch(url, user_agent)
        status = "✅ Permitido" if can_fetch else "❌ Bloqueado"
        print(f"   {status}: {url}")

async def main():
    """Función principal con todos los ejemplos"""
    print("🕷️ SISTEMA DE SCRAPING ÉTICO - EJEMPLOS DE USO")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Ejecutar todos los ejemplos
        await example_basic_scraping()
        await example_bilforsikring_scraping()
        await example_leasing_scraping()
        await example_data_validation()
        await example_rate_limiting()
        await example_robots_txt_check()
        
        print("\n" + "=" * 60)
        print("🎉 Todos los ejemplos ejecutados exitosamente!")
        print("\n💡 Consejos para uso en producción:")
        print("   • Ejecutar en horarios de bajo tráfico (2-6 AM)")
        print("   • Monitorear logs para detectar problemas")
        print("   • Respetar siempre robots.txt y ToS")
        print("   • Usar rate limiting apropiado")
        print("   • Validar datos antes de guardar")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error ejecutando ejemplos: {e}")
        print("💡 Verifica que todas las dependencias estén instaladas")

if __name__ == "__main__":
    asyncio.run(main())
