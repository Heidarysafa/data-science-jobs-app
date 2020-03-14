# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndidV1Item(scrapy.Item):
    # define the fields for your item here like: job_title, company, location, date,description,\
            #day,posted_date, state, city, term
    job_title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    day = scrapy.Field()
    posted_date = scrapy.Field()
    state = scrapy.Field()
    city = scrapy.Field()
    search_term = scrapy.Field()
    
