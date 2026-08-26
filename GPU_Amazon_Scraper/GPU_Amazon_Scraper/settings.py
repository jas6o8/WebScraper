BOT_NAME = "GPU_Amazon_Scraper"

SPIDER_MODULES = ["GPU_Amazon_Scraper.spiders"]
NEWSPIDER_MODULE = "GPU_Amazon_Scraper.spiders"

# Disable robots.txt parsing (Amazon blocks bot paths in robots.txt)
ROBOTSTXT_OBEY = False

# Single modern User-Agent (Chrome 124+)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# Default request headers matching a real desktop browser
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

# Remove scrapy_user_agents middleware entirely
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
    #'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    #'rotating_proxies.middlewares.BanDetectionMiddleware': 620,

}
ROTATING_PROXY_LIST = [
    'http://proxy1.com:8000',
    'http://username:password@proxy2.com:8000',
    'http://167.99.1.1:8080',
]

# Throttling to reduce ban rate
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

FEED_EXPORT_ENCODING = "utf-8"
ITEM_PIPELINES = {
    "GPU_Amazon_Scraper.pipelines.AmazonScraperSQlitePipeline": 300,
    
    
}