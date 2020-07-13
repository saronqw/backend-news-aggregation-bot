from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_api import views
from rest_api.views import NewsItemViewSet, UniversityViewSet, NewsItemLastWeekViewSet

router = DefaultRouter()
router.register(r'news', views.NewsItemViewSet)
router.register(r'universities', views.UniversityViewSet)
router.register(r'lastnews', NewsItemLastWeekViewSet, basename='lastnews')

last_news = NewsItemLastWeekViewSet.as_view({'get': 'list'})

news_list = NewsItemViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

news_detail = NewsItemViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

university_list = UniversityViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

university_detail = UniversityViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', include(router.urls)),
    path('news/', news_list, name='news-list'),
    path('news/<int:pk>/', news_detail, name='news-detail'),
    path('universities/', university_list, name='university-list'),
    path('universities/<int:pk>/', university_detail, name='university-detail'),
]