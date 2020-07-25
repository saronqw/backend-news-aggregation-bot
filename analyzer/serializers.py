from rest_framework import serializers

from analyzer.models import Keyword


class KeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keyword
        fields = ['id', 'coef', 'count', 'tag', 'university']
