from rest_framework import serializers

from rest_api.models import NewsItem, University


class NewsItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsItem
        # fields = ['url', 'id', 'title', 'description', 'link', 'university', 'datetime']
        fields = ['id', 'title', 'description', 'full_text', 'link', 'university', 'pub_date']


class UniversitySerializer(serializers.ModelSerializer):
    news = NewsItemSerializer(many=True)

    class Meta:
        model = University
        fields = ['id', 'name', 'news']
        # fields = ['url', 'id', 'name', 'news']
