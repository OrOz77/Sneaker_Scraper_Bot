# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShoeItem(scrapy.Item):
    # shoe is defined by:
    #   brand
    #   model name
    #   model number
    #   colorway
    #   price
    #   sizes available
    #   website source

    _id = scrapy.Field()        #necessary for db storage
    brand = scrapy.Field()
    modelName = scrapy.Field()
    modelNumber = scrapy.Field()
    colorway = scrapy.Field()
    price = scrapy.Field()
    sizes = scrapy.Field()
    urlSource = scrapy.Field()
    url = scrapy.Field()
    imageUrl = scrapy.Field()
