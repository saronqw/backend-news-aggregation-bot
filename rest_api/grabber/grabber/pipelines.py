from asgiref.sync import sync_to_async
from rest_framework.parsers import JSONParser

from rest_api.serializers import NewsItemSerializer


class GrabberPipeline:

    # def process_item(self, item, spider):
    #     return item
    # content = ''
    # json_array = []

    # def process_item(self, item, spider):
    #
    #     # line = json.dumps(ItemAdapter(item).asdict()) + "\n"
    #     # self.content += line
    #     self.json_array.append(item)
    #     return item
    #
    #
    # def close_spider(self, spider):
    #     print(self.json_array)
    #     data = JSONParser().parse(self.json_array)
    #     serializer = NewsItemSerializer(data=data)
    #     serializer.is_valid()
    #     serializer.save()
    def process_item(self, item, spider):
        item.save()
        return item
