# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Listing(scrapy.Item):
    Title = scrapy.Field()
    Guests = scrapy.Field()
    Features = scrapy.Field()
    Price = scrapy.Field()
    Rating = scrapy.Field()
    Link = scrapy.Field()
    Destination = scrapy.Field()
