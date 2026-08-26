# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json,sqlite3

class AmazonScraperSQlitePipeline:
    TABLE_MAP = {
        "GPU": ("gpu_data.db", "gpu_data"),
        "CPU": ("cpu_data.db", "cpu_data"),
    }

    def open_spider(self, spider):
        db_name, self.table = self.TABLE_MAP[spider.name]
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT,
                price TEXT,
                image_url TEXT,
                shipping_cost TEXT,
                delivery_text TEXT,
                UNIQUE(product_name)
            )
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO {self.table}
            (product_name, price, image_url, shipping_cost, delivery_text)
            VALUES (?, ?, ?, ?, ?)
        ''', (adapter.get('product_name'), adapter.get('price'),
              adapter.get('image_url'), adapter.get('shipping_cost'),
              adapter.get('delivery_text')))
        self.connection.commit()
        return item
    
class CpuAmazonScraperPipeline:
    def process_item(self, item,spider):
        if spider.name == "CPU":
            # Process CPU items
            # You can add any additional processing logic here if needed
            
            return item
class GpuAmazonScraperPipeline:
    def process_item(self, item,spider):
        if spider.name == "GPU":
            # Process GPU items
            # You can add any additional processing logic here if needed
            pass
        return item
