import scrapy
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from Sneaker_Scraper.items import ShoeItem


class NikeSpider(CrawlSpider):
    name = 'Nike'
    allowed_domains = ['nike.com']
    rotate_user_agent = True
    start_urls = [                                                                                                          #add any desired shoe URL from Nike.com to scrape new data
        'http://store.nike.com/us/en_us/pd/flyknit-racer-unisex-running-shoe/pid-10064409/pgid-11809455',                   #Unisex Flyknit Racers
    #    'http://store.nike.com/us/en_us/pd/air-zoom-structure-20-shield-mens-running-shoe/pid-11239090/pgid-11462468',      #Men's Air Zoom Structure
    #    'http://store.nike.com/us/en_us/pd/converse-chuck-taylor-all-star-low-top-unisex-shoe/pid-11214172/pgid-11337711',  #Unisex Converse Low Top
    #    'http://store.nike.com/us/en_us/pd/air-jordan-xxxi-mens-basketball-shoe/pid-11189232/pgid-11522191',                #Men's Air Jordan 31
    #    'http://store.nike.com/us/en_us/pd/lunarepic-low-flyknit-womens-running-shoe/pid-11055907/pgid-11862848',           #Women's lunarepic shoe with many colors
    ]

    #set rule to only use certain links on each page
    rules = (
        # Extract links matching each colorway in the 'color-chips' DIV and parse them with the spider's method parse_item
        Rule(
            LinkExtractor(
                allow=(),
                restrict_xpaths="//div[contains(@class, 'color-chips')]//a",
            ),
            callback="parse_item"
        ),
    )

    #builds ShoeItem based on response
    def parse_item(self, response):

        def parseNikeStringForUnisexSizes(_shoeStock):
            splitSizes = re.findall("M (.*?) /", _shoeStock) #Nike.com stock string broken down by left bound 'M ', right bound ' /' for unisex
            return splitSizes

        def parseNikeStringforSizes(_shoeStock):
            splitSizes = _shoeStock.split(':') #Nike.com stock string split by ':' characters
            return splitSizes



        #DIV element 'hero-image-container' contains modelName on Nike.com
        modelName = Selector(response).xpath("//div[contains(@class, 'hero-image-container')]//img/@alt").extract() #modelName

        #DIV element 'color-chips' contains url, colorway, image URL, and productId on Nike.com
        div_colorChips = Selector(response).xpath("//div[contains(@class, 'color-chips')]")

        selectedShoeUrl = div_colorChips.xpath("//li[@class='selected']//a/@href").extract()    #url
        selectedShoeColorway = div_colorChips.xpath("//li[@class='selected']//img/@alt").extract() #colorway
        selectedShoeProductId = div_colorChips.xpath("//li[@class='selected']//a/@data-productid").extract() #productId
        selectedShoeImageUrl = div_colorChips.xpath("//li[@class='selected']//img/@src").extract() #image url

        #DIV element 'exp-pdp-product-price exp-pdp-product-swoosh-price-available' contains price of shoe
        shoePrice = Selector(response).xpath("//div[contains(@class, 'exp-pdp-product-price exp-pdp-product-swoosh-price-available')]//span[@itemprop = 'price']/text()").extract() #price

        #DIV element 'tfc-fitrec-product js-trueFitWidget' -> field 'data-availablesizes' holds stock
        shoeStock = Selector(response).xpath("//div[contains(@class, 'tfc-fitrec-product js-trueFitWidget')]/@data-availablesizes").extract() #string of instock sizes

        if "Unisex" in str(modelName):
            sizesAvailable = parseNikeStringForUnisexSizes(str(shoeStock)) #str() converts unicode string to ASCII string
        else:
            sizesAvailable = parseNikeStringforSizes(str(shoeStock))

        #build item defined in 'items.py' file
        item = ShoeItem()
        item['brand'] = 'Nike'
        item['modelName'] = modelName
        item['modelNumber'] = selectedShoeProductId
        item['colorway'] = selectedShoeColorway
        item['price'] = shoePrice
        item['sizes'] = sizesAvailable
        item['url'] = selectedShoeUrl
        item['urlSource'] = 'Nike.com'
        item['imageUrl'] = selectedShoeImageUrl

        if(item['colorway']):       #ensure object is valid
            yield item
