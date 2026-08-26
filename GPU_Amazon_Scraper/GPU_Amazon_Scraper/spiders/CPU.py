from urllib.parse import urlencode
import scrapy
from ..items import CpuAmazonScraperItem
import os ,re

class CpuSpider(scrapy.Spider):
    name = "CPU"
    allowed_domains = ["amazon.com"]
    start_urls = ["https://www.amazon.com/s?i=specialty-aps&bbn=16225007011&rh=n%3A16225007011%2Cn%3A193870011&ref=nav_em__nav_desktop_sa_intl_computer_components_0_2_7_3"]

    custom_settings = {
        "USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ),
        "AUTOTHROTTLE_ENABLED": True,
        
    }
    API_KEY = os.environ.get("SCRAPERAPI_KEY ")
    page_number = 2

    def start_requests(self):
        # Target CPUs specifically
        target_url = "https://www.amazon.com/s?k=cpu+processor"
        proxy_url = f"http://api.scraperapi.com/?{urlencode({'api_key': self.API_KEY, 'url': target_url})}"

        yield scrapy.Request(url=proxy_url, callback=self.parse)

    def parse(self, response):
            exclude_keywords = [
        'MOTHERBOARD', 'RAM', 'MEMORY', 'DDR4', 'DDR5',
        'FAN', 'DIMM', 'SODIMM',
            'SSD', 'HDD', 'STORAGE', 'POWER SUPPLY', 'PSU', 'CASE',]

            cpu_pattern = re.compile(
            r'(CORE\s*(I[3579]|ULTRA)|RYZEN\s*[3579]|THREADRIPPER)',
            re.IGNORECASE
            )
            for q in response.css('.desktop-grid-content-view'):
                name = q.css('.a-color-base.a-text-normal span::text').get()
    
                if not name:
                    continue

                name_upper = name.upper()
                is_excluded = any(x in name_upper for x in exclude_keywords)
                is_cpu = cpu_pattern.search(name) and 'PROCESSOR' in name_upper

                if is_cpu and not is_excluded:
                    shipping_cost = q.css('.a-span12::text').get()
                    delivery_text = q.css('.s-align-children-center .a-size-small::text').get()
    
                    if shipping_cost:
                        shipping_cost = shipping_cost.strip()
                    if delivery_text:
                        delivery_text = delivery_text.strip()
                    else:
                        delivery_text = "no delivery to your location"
    
                    yield CpuAmazonScraperItem(
                        product_name=name.strip(),
                        price=q.css('.a-price-whole::text').get(),
                        image_url=q.css('img.s-image::attr(src)').get(),
                        shipping_cost=shipping_cost,
                        delivery_text=delivery_text
                    )
                    next_page="https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cn%3A193870011&page="+str(self.page_number)+"&qid=1786819904&xpid=j19T6UnzfTL5K&ref=sr_pg_2"
            max_pages = 5  # Set the maximum number of pages to scrape
            if next_page and self.page_number <= max_pages:
                self.page_number += 1
                yield response.follow(next_page, callback=self.parse)

            names = [
            "AMD Ryzen 5 5500 6-Core, 12-Thread Unlocked Desktop Processor with Wraith Stealth Cooler",
            "Thermalright Peerless Assassin 120 SE CPU Cooler, 6 Heat Pipes AGHP Technology, Dual 120mm PWM Fans, 1550RPM Speed, for AMD:AM4 AM5/Intel LGA 1700/1150/1151/1200/1851,PC Cooler",
            # ...rest of your 41
            ]

            for n in names:
                nu = n.upper()
                if cpu_pattern.search(n) and 'PROCESSOR' in nu and not any(x in nu for x in exclude_keywords):
                    print("KEEP:", n)
                else:
                    print("DROP:", n)
                
                                