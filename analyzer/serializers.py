from rest_framework import serializers

from analyzer.models import Keyword


class KeywordSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField('get_score')

    def get_score(self, keyword):
        return round(keyword.coef * keyword.count * 1500)

    class Meta:
        model = Keyword
        fields = ['id', 'coef', 'count', 'tag', 'university', 'score']
