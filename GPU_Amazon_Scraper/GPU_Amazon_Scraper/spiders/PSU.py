import scrapy
from urllib.parse import urlencode
import os
from ..items import PsuAmazonScraperItem


class PsuSpider(scrapy.Spider):
    name = "PSU"
    allowed_domains = ["amazon.com", "api.scrape.do"]
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
    }
    API_KEY = os.environ.get("SCRAPEDO_KEY")
    page_number = 2

    async def start(self):
        self.logger.info("start_requests called")
        target_url = 'https://www.amazon.com/s?k=power+supply&rh=n%3A193870011&ref=nb_sb_noss'
        proxy_url = self.build_proxy_url(target_url)
        self.logger.info(f"Requesting: {proxy_url}")
        yield scrapy.Request(url=proxy_url, callback=self.parse)

    def build_proxy_url(self, target_url):
        return f'https://api.scrape.do/?{urlencode({"token": self.API_KEY, "url": target_url, "render": "true"})}'

    def parse(self, response):
        products = response.css('div[data-component-type="s-search-result"]')

        for q in products:
            name = q.css('h2 span::text').get()

            if name and any(k in name.upper() for k in [
                'POWER SUPPLY', 'PSU', 'FULLY MODULAR', 'SEMI MODULAR', 'ASROCK',
                '850W', '750W', '650W', '600W', '550W', '500W', '80+ GOLD'
            ]):
                shipping_cost = q.css('.a-span12::text').get()
                delivery_text = q.css('.s-align-children-center .a-size-small::text').get()

                shipping_cost = shipping_cost.strip() if shipping_cost else None
                delivery_text = delivery_text.strip() if delivery_text else "no delivery to your location"

                yield PsuAmazonScraperItem(
                    product_name=name.strip(),
                    price=q.css('.a-price-whole::text').get(),
                    image_url=q.css('img.s-image::attr(src)').get(),
                    shipping_cost=shipping_cost,
                    delivery_text=delivery_text
                )

        next_page_href = response.css('a.s-pagination-next::attr(href)').get()
        if next_page_href:
            full_url = response.urljoin(next_page_href)
            proxy_url = self.build_proxy_url(full_url)
            self.page_number += 1
            yield scrapy.Request(url=proxy_url, callback=self.parse)