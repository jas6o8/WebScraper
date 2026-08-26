# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass,field
import scrapy


@dataclass
class GpuAmazonScraperItem:
    product_name: str
    price: str
    image_url: str
    delivery_text: str = field(default="NO shipping = NO delivery")
    shipping_cost:str=field(default="free shipping")

@dataclass
class CpuAmazonScraperItem:
    product_name: str
    price: str
    image_url: str
    delivery_text: str = field(default="NO shipping = NO delivery")
    shipping_cost:str=field(default="free shipping")

@dataclass
class RamAmazonScraperItem:
    product_name: str
    price: str
    image_url: str
    delivery_text: str = field(default="NO shipping = NO delivery")
    shipping_cost:str=field(default="free shipping")

@dataclass
class PsuAmazonScraperItem:
    product_name: str
    price: str
    image_url: str
    delivery_text: str = field(default="NO shipping = NO delivery")
    shipping_cost:str=field(default="free shipping")

@dataclass
class MotherBoardAmazonScraperItem:
    product_name: str
    price: str
    image_url: str
    delivery_text: str = field(default="NO shipping = NO delivery")
    shipping_cost:str=field(default="free shipping")