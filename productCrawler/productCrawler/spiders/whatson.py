#-*- coding: utf-8 -*-
import scrapy
import socket
import datetime
import json
import string
import re
import urllib
from urllib.request import urlretrieve
from urllib.request import urlopen

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from ..items import WhatsonItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from bs4 import BeautifulSoup
from selenium import webdriver


class ProductLoader(ItemLoader):
    name_in = MapCompose(str.strip, str.title)
    name_out = Join("")

    date_in = MapCompose(str.strip)
    date_out = Join("")

    time_in = MapCompose(str.strip)
    time_out = Join(",")

    location_in = MapCompose(str.strip)
    location_out = Join(",")

    website_in = MapCompose(str.strip)
    website_out = Join("")

    phone_in = MapCompose(str.strip)
    phone_out = Join("")

    email_in = MapCompose(str.strip)
    email_out = Join("")

    facebook_in = MapCompose(str.strip)
    facebook_out = Join("")

    instagramLinks_in = MapCompose(str.strip)
    instagramLinks_out = Join("")

    description_in = MapCompose(str.strip, lambda x: x.replace("\n", " "), lambda x: x.replace(";", ","))
    description_out = Join("")

    price_in = MapCompose(str.strip)
    price_out = Join("")

    features_in = MapCompose(str.strip)
    features_out = Join("")

    backgroundImage_in = MapCompose(str.strip)
    backgroundImage_out = Join("")

    pagelink_out = Join("")


class WhatsonSpider(CrawlSpider):
    name = 'whatson'

    def start_requests(self):
        with open("whatson-url.json", "r") as fp:
            urls = json.load(fp)
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_item,
            )

    def parse_item(self, response):
        loader = ProductLoader(item=WhatsonItem(), response=response)
        loader.add_xpath('name', '//div[@class="contact-title"]/h1/text()')

        date_content = response.xpath('//div[@class="date"]').extract()
        str_date_content = ''.join(date_content)
        date_content_list = str_date_content.split("<br>", -1)

        str_only_date_content = ''.join(date_content_list[0])
        text = BeautifulSoup(str_only_date_content, "lxml").text
        cleanr = re.compile('<.*?>')
        datetext = re.sub(cleanr, '', text)
        loader.add_value('date', datetext.replace('\n', '').replace(' ', ''))

        str_only_time_content = ''.join(date_content_list[len(date_content_list) - 1])
        text = BeautifulSoup(str_only_time_content, "lxml").text
        cleanr = re.compile('<.*?>')
        timetext = re.sub(cleanr, '', text)
        loader.add_value('time', timetext.replace('\n', '').replace(' ', ''))

        location = response.xpath('//dl[@class="contact-info"]/dl[1]/a/span/text()').extract()

        loader.add_value('location', ''.join(location[0]).replace('\n', '').replace(' ', ''))

        phone = response.xpath('//dl[@class="contact-info"]/dl[2]/a/span/text()').extract()
        loader.add_value('phone', ''.join(phone[0]))

        all_data = response.xpath('//script[@type="application/ld+json"]').extract()
        str_all_data = ''.join(all_data)

        split_email = str_all_data.split('"email":', -1)
        str_email_content = ''.join(split_email[1])
        email = str_email_content.split(',"contactType":', -1)[0]
        # print("--------------------", email)
        loader.add_value('email', email.replace('"', ''))

        split_site = str_all_data.split('"url":', -1)
        if len(split_site) > 1:
            str_site_content = ''.join(split_site[1])
            site = str_site_content.split(',"name":', -1)[0]
            loader.add_value('website', site.replace('"', '').replace('},', ''))

        instagram = response.xpath('//div[@class="social-icons__container"]/a[1]/@href').extract()
        if len(instagram) > 0:
            loader.add_value('instagramLinks', ''.join(instagram[0]))

        facebookLink = response.xpath('//div[@class="social-icons__container"]/a[2]/@href').extract()
        if len(facebookLink) > 0:
            loader.add_value('facebook', ''.join(facebookLink[0]))

        loader.add_xpath('description', '//div[@class="overview infosection"]/p/text()')

        # loader.add_xpath('price', '//div[@class="price infosection"]/p/text()')
        price = response.xpath('//div[@class="price infosection"]/p/text()').extract()
        str_price = ''.join(price)
        loader.add_value('price', str_price.replace('\n', '').replace(' ', ''))

        # feature_title = response.xpath('//li[@class="feature-list__list-item"]/h3').extract()
        feature = response.xpath('//div[@class="features infosection"]').extract()
        feature_content = ''.join(feature)

        text = BeautifulSoup(feature_content, "lxml").text
        cleanr = re.compile('<.*?>')
        featuretext = re.sub(cleanr, '', text)
        loader.add_value('features', featuretext.replace('\n',''))

        image = response.xpath('//img[@class="product-carousel__image"]/@src').extract()
        image_title = response.xpath('//img[@class="product-carousel__image"]/@alt').extract()
        image_url = 'https://southaustralia.com' + image[0]
        loader.add_value('backgroundImage', image_url)

        # get the image source
        # f = open("images/"+image_title[0], 'wb')
        # f.write(urlopen(image_url).read())
        # f.close()

        # get the html source
        f2 = open("htmls/"+image_title[0]+".html",'w')
        html = urlopen(response.url).read()
        soup = BeautifulSoup(html)
        f2.write(str(soup))
        f2.close()

        loader.add_value('pagelink', response.url)

        yield loader.load_item()
