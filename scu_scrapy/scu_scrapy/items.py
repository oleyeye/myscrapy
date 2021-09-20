# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MentorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    domain = scrapy.Field()
    abstract = scrapy.Field()
    fullContent = scrapy.Field()
    url = scrapy.Field()
