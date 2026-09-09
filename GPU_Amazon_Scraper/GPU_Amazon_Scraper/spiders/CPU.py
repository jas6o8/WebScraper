import scrapy
import os
import re
from urllib.parse import urlencode
from ..items import CpuAmazonScraperItem


class CpuSpider(scrapy.Spider):
    name = "CPU"
    allowed_domains = ["amazon.com", "scrape.do"]

    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
    }
    API_KEY = os.environ.get("SCRAPEDO_KEY")
    page_number = 2
    max_pages = 5

    exclude_keywords = [
        'MOTHERBOARD', 'RAM', 'MEMORY', 'DDR4', 'DDR5',
        'FAN', 'DIMM', 'SODIMM',
        'SSD', 'HDD', 'STORAGE', 'POWER SUPPLY', 'PSU', 'CASE',
    ]
    cpu_pattern = re.compile(
        r'(CORE\s*(I[3579]|ULTRA)|RYZEN\s*[3579]|THREADRIPPER)',
        re.IGNORECASE
    )

    async def start(self):
        target_url = "https://www.amazon.com/s?k=cpu+processor"
        proxy_url = self.build_proxy_url(target_url)
        yield scrapy.Request(url=proxy_url, callback=self.parse)

    def build_proxy_url(self, target_url):
        return f'https://api.scrape.do/?{urlencode({"token": self.API_KEY, "url": target_url, "render": "true"})}'

    def parse(self, response):
        next_page = None
        products = response.css('div[data-component-type="s-search-result"]')

        for q in products:
            name = q.css('h2 span::text').get()
            if not name:
                continue

            name_upper = name.upper()
            is_excluded = any(x in name_upper for x in self.exclude_keywords)
            is_cpu = self.cpu_pattern.search(name) and 'PROCESSOR' in name_upper

            if is_cpu and not is_excluded:
                shipping_cost = q.css('.a-span12::text').get()
                delivery_text = q.css('.s-align-children-center .a-size-small::text').get()

                shipping_cost = shipping_cost.strip() if shipping_cost else None
                delivery_text = delivery_text.strip() if delivery_text else "no delivery to your location"

                yield CpuAmazonScraperItem(
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