# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Album(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    album_url= scrapy.Field()
    title = scrapy.Field()
    artist = scrapy.Field()
    license = scrapy.Field()
    license_url = scrapy.Field()
    numsongs = scrapy.Field()
