# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy_djangoitem import DjangoItem

import scrapy

from rest_api.models import NewsItem, University

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aggregator.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
class GrabberItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# class NewsItem(scrapy.Item):
#     title = scrapy.Field()
#     description = scrapy.Field()
#     link = scrapy.Field()
#     pub_date = scrapy.Field()
#     university_id = scrapy.Field()

class ScrapyNewsItem(DjangoItem):
    django_model = NewsItem


class ScrapyUniversityItem(DjangoItem):
    django_model = University
