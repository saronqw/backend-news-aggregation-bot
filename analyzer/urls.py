from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import LineChartJSONView, ComparisonChartJSONView, NewsPerWeekChartJSONView

urlpatterns = [
    path('', views.index, name='index'),
    path('line_chartJSON', LineChartJSONView.as_view(), name='line_chart_json'),
    path('comparison_chartJSON', ComparisonChartJSONView.as_view(), name='comparison_chart_json'),
    path('newsperweek_chartJSON', NewsPerWeekChartJSONView.as_view(), name='newsperweek_chart_json'),
]
