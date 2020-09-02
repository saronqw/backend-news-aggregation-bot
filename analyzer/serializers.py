from rest_framework import serializers

from analyzer.models import Keyword, KeywordGroup


class KeywordGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordGroup
        fields = ['id', 'group_name']


class KeywordSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField('get_score')

    def get_score(self, keyword):
        return round(keyword.coef * keyword.count * 1500)

    class Meta:
        model = Keyword
        fields = ['id', 'coef', 'count', 'tag', 'university', 'score']
