# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class WhatsonItem(scrapy.Item):
    # Product details
    name = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    location = scrapy.Field()
    website = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    facebook = scrapy.Field()
    instagramLinks = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    features = scrapy.Field()
    backgroundImage = scrapy.Field()
    images = scrapy.Field()

    # Housekeeping fields
    pagelink = scrapy.Field()
    # Project = scrapy.Field()
    # Spider = scrapy.Field()
    # Server = scrapy.Field()
    # Date = scrapy.Field()