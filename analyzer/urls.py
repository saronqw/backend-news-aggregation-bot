from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import LineChartJSONView

urlpatterns = [
    path('', views.index, name='index')
]

urlpatterns += [
  path('chart', TemplateView.as_view(template_name='analyzer/test.html'), name='line_chart'),
  path('chartJSON', LineChartJSONView.as_view(), name='line_chart_json'),
]
