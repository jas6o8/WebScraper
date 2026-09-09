import os

import scrapy
from urllib.parse import urlencode
from urllib import response
from ..items import RamAmazonScraperItem


class RamSpider(scrapy.Spider):
    name = "RAM"
    allowed_domains = ["amazon.com"]
    start_urls = ["https://www.amazon.com/s?i=specialty-aps&bbn=16225007011&rh=n%3A16225007011%2Cn%3A193870011&ref=nav_em__nav_desktop_sa_intl_computer_components_0_2_7_3"]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'AUTOTHROTTLE_ENABLED': True,
    }
    API_KEY = os.environ.get("SCRAPEDO_KEY")

    async def start(self):
        target_url = 'https://www.amazon.com/s?k=gpu'
        # Route request through ScraperAPI endpoint
        proxy_url = f'http://api.scraperapi.com/?{urlencode({"api_key": self.API_KEY, "url": target_url})}'
        
        yield scrapy.Request(url=proxy_url, callback=self.parse)
    page_number = 2

    def parse(self, response):
        for q in response.css('.desktop-grid-content-view'):
            name = q.css('.a-color-base.a-text-normal span::text').get()

            if name and any(k in name.upper() for k in ['DDR4','DDR5','DDR3']):
                shipping_cost = q.css('.a-span12::text').get()
                delivery_text = q.css('.s-align-children-center .a-size-small::text').get()

                if shipping_cost:
                    shipping_cost = shipping_cost.strip()
                if delivery_text:
                    delivery_text = delivery_text.strip()
                else:
                    delivery_text = "no delivery to your location"

                yield RamAmazonScraperItem(
                    product_name=name.strip(),
                    price=q.css('.a-price-whole::text').get(),
                    image_url=q.css('img.s-image::attr(src)').get(),
                    shipping_cost=shipping_cost,
                    delivery_text=delivery_text
                )
                next_page="https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cn%3A193870011&page="+str(self.page_number)+"&qid=1786819904&xpid=j19T6UnzfTL5K&ref=sr_pg_2"
        if next_page:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)

                
