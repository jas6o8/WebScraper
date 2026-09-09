from urllib import response
import os
import scrapy
from ..items import GpuAmazonScraperItem
from urllib.parse import urlencode

class GpuSpider(scrapy.Spider):
    name = "GPU"
    allowed_domains = ["amazon.com", "api.scrape.do"]
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'AUTOTHROTTLE_ENABLED': True,
        
    }
    API_KEY = os.environ.get("SCRAPEDO_KEY ")

    async def start(self):
        target_url = 'https://www.amazon.com/s?k=gpu'
        # Route request through ScraperAPI endpoint
        proxy_url = self.build_proxy_url(target_url)
        
        yield scrapy.Request(url=proxy_url, callback=self.parse)
    page_number = 2
    max_pages = 5
    def build_proxy_url(self, target_url):
            return f'https://api.scrape.do/?{urlencode({"token": self.API_KEY, "url": target_url, "render": "true"})}'
    

    def parse(self, response):
        for q in response.css('div[data-component-type="s-search-result"]'):
            name = q.css('h2 span::text').get()

            if name and any(k in name.upper() for k in ['RTX', 'RX', 'GTX', 'RADEON', 'GEFORCE']):
                shipping_cost = q.css('.a-span12::text').get()
                delivery_text = q.css('.s-align-children-center .a-size-small::text').get()

                if shipping_cost:
                    shipping_cost = shipping_cost.strip()
                if delivery_text:
                    delivery_text = delivery_text.strip()
                else:
                    delivery_text = "no delivery to your location"

                yield GpuAmazonScraperItem(
                    product_name=name.strip(),
                    price=q.css('.a-price-whole::text').get(),
                    image_url=q.css('img.s-image::attr(src)').get(),
                    shipping_cost=shipping_cost,
                    delivery_text=delivery_text
                )
        next_page_href = response.css('a.s-pagination-next::attr(href)').get()
        if next_page_href and self.page_number <= self.max_pages:
             full_url = response.urljoin(next_page_href)
             proxy_url = self.build_proxy_url(full_url)
             self.page_number += 1
             yield scrapy.Request(url=proxy_url, callback=self.parse)
                