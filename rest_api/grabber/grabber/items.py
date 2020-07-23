from scrapy_djangoitem import DjangoItem
from rest_api.models import NewsItem, University
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aggregator.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

class ScrapyNewsItem(DjangoItem):
    django_model = NewsItem


class ScrapyUniversityItem(DjangoItem):
    django_model = University
