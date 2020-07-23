from asgiref.sync import sync_to_async
from rest_framework.parsers import JSONParser

from rest_api.serializers import NewsItemSerializer


class GrabberPipeline:

    def process_item(self, item, spider):
        item.save()
        return item
