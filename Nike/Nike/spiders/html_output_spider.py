import scrapy

#a spider to retrieve HTML doc from a URL
class HTMLSpider(scrapy.Spider):
    name = "HTML"
    start_urls = [
        'http://store.nike.com/us/en_us/pd/flyknit-racer-unisex-running-shoe/pid-10064409/pgid-11809455', #Nike sample product page
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'TESThtml-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
