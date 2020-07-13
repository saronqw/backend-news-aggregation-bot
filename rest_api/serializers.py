from rest_framework import serializers

from rest_api.models import NewsItem, University


class NewsItemSerializer(serializers.ModelSerializer):
    # university = serializers.HyperlinkedRelatedField(view_name='university-detail', read_only=True)
    # university = serializers.PrimaryKeyRelatedField(queryset=University.name)

    class Meta:
        model = NewsItem
        # fields = ['url', 'id', 'title', 'description', 'link', 'university', 'datetime']
        fields = ['id', 'title', 'description', 'link', 'university', 'pub_date']


class UniversitySerializer(serializers.ModelSerializer):
    news = NewsItemSerializer(many=True)

    class Meta:
        model = University
        fields = ['id', 'name', 'news']
        # fields = ['url', 'id', 'name', 'news']
