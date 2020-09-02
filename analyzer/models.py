
from django.db import models
from rest_api.models import University


class KeywordGroup(models.Model):
    group_name = models.CharField(max_length=50)

    def __str__(self):
        return self.group_name


class Keyword(models.Model):
    coef = models.FloatField()
    count = models.IntegerField()
    tag = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    group = models.ForeignKey(KeywordGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag
