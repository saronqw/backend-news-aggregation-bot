from django.db import models


class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    link = models.CharField(max_length=200)
    university = models.ForeignKey('University', related_name='news', on_delete=models.CASCADE, null=True)
    pub_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class University(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
