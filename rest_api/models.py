from django.db import models


class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.CharField(max_length=200)
    university = models.ForeignKey('University', related_name='news', on_delete=models.CASCADE)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.title


class University(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
