from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views
from .views import LineChartJSONView, ComparisonChartJSONView, NewsPerWeekChartJSONView, KeywordViewSet, \
    WordsPerWeekChartJSONView, BoxPlotNewsChartJSONView, BoxPlotWordsChartJSONView, RadarThemeChartJSONView

router = DefaultRouter()
router.register(r'keywords', views.KeywordViewSet, basename='keywords')

keywords_list = KeywordViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('', views.index, name='index'),
    path('line_chartJSON', LineChartJSONView.as_view(), name='line_chart_json'),
    path('comparison_chartJSON', ComparisonChartJSONView.as_view(), name='comparison_chart_json'),
    path('newsperweek_chartJSON', NewsPerWeekChartJSONView.as_view(), name='newsperweek_chart_json'),
    path('wordsperweek_chartJSON', WordsPerWeekChartJSONView.as_view(), name='wordsperweek_chart_json'),
    path('boxplot_news_chartJSON', BoxPlotNewsChartJSONView.as_view(), name='boxplot_news_chart_json'),
    path('boxplot_words_chartJSON', BoxPlotWordsChartJSONView.as_view(), name='boxplot_words_chart_json'),
    path('radar_theme_chartJSON', RadarThemeChartJSONView.as_view(), name='radar_theme_chart_json'),
    path('keywords', keywords_list, name='keywords-list'),
]
