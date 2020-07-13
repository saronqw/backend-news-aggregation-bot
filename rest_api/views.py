from datetime import *

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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
        interval = params.get("interval", "seven")

        count_days_ago = (datetime.now() - timedelta(days=self.get_days(interval)))

        name = params.get("name", "all")

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


class NewsItemViewSet(viewsets.ModelViewSet):
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # @action(detail=False, renderer_classes=[renderers.StaticHTMLRenderer])
    # def news_from_last_week(self, request, *args, **kwargs):
    #     last_week = (datetime.now() - timedelta(days=7))
    #
    #     # serializer = NewsItemSerializer(context={'request': request}, instance=NewsItem.objects.filter(datetime__range=[last_week, datetime.now()]), )
    #     # serializer.is_valid()  # проверяем валидность
    #     # content = JSONRenderer().render(serializer.data)
    #     # return Response(
    #     #     content
    #     # )
    #
    #     resp =  NewsItem.objects.filter(datetime__range=[last_week, datetime.now()])
    #     return Response(
    #         resp
    #     )


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
