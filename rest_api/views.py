import json
from datetime import *
from threading import Thread

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import time
from rest_api.grabber.grabber import RunGrabber

from rest_api.models import NewsItem, University
from rest_api.serializers import NewsItemSerializer, UniversitySerializer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)
        print(token.key)


class NewsItemLastWeekViewSet(viewsets.ViewSet):

    def list(self, request):
        params = request.query_params
        interval = params.get("interval", "seven_days")

        count_days_ago = (datetime.now() - timedelta(days=self.get_days(interval)))

        name = params.get("name", "all")

        # self.update_news()

        if name == "all" or name is None:
            queryset = NewsItem.objects.filter(pub_date__range=[count_days_ago, datetime.now()])
        else:
            queryset = NewsItem.objects.filter(pub_date__range=[count_days_ago, datetime.now()], university__name=name)

        serializer = NewsItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_days(self, interval):
        return {
            'one_day': 1,
            'three_days': 3,
            'seven_days': 7,
        }[interval]

    def update_news(self):
        runner = RunGrabber()
        runner.runGrabbers()
        # runGrabbers()

        # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        # runner = CrawlerRunner()
        # d = runner.crawl(TpuSpider)
        # d.addBoth(lambda _: reactor.stop())
        # reactor.run()  # the script will block here until the crawling is finished


class NewsItemViewSet(viewsets.ModelViewSet):
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
