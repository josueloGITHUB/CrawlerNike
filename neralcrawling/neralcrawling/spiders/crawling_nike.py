import scrapy
import pandas as pd
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ProductoNike(scrapy.Item):
    nombre = scrapy.Field()
    descripcion = scrapy.Field()
    precio = scrapy.Field()
    enlace = scrapy.Field()

class MyFancySpider(CrawlSpider):
    name = 'myfancycrawler'
    allowed_domains = ['www.nike.com']
    start_urls = ['https://www.nike.com/']
    rules = (
        Rule(LinkExtractor(allow="mx/w"), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(MyFancySpider, self).__init__(*args, **kwargs)
        self.items = []

    def parse_item(self, response):
        item = ProductoNike()
        item['nombre'] = response.css('.product-card__title::text').get()
        item['descripcion'] = response.css('.product-card__subtitle::text').get()
        item['precio'] = response.css('.product-price::text').get()
        item['enlace'] = response.url  
        
        # Puedes imprimir los resultados para verificar
        self.log(f'Item extraído: {item}')

        # Agrega el item a la lista de items
        self.items.append(item)

        return item

    def closed(self, reason):
        # Cuando la araña está cerrada, crea un DataFrame y guarda en Excel
        df = pd.DataFrame({
            'Nombre': [item['nombre'] for item in self.items],
            'Descripción': [item['descripcion'] for item in self.items],
            'Precio': [item['precio'] for item in self.items],
            'Enlace': [item['enlace'] for item in self.items],
        })

        # Guarda el DataFrame en un archivo Excel en el path proporcionado
        ruta_archivo = r'C:\Users\Oscar Adame\source\repos\Crawler\CrawlerNike\neralcrawling\resultados_nike.xlsx'
        df.to_excel(ruta_archivo, index=False)
