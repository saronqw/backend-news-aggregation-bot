import math
from datetime import *

import numpy
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from analyzer.models import Keyword
from analyzer.serializers import KeywordSerializer
from rest_api.models import NewsItem, University
from chartjs.views.lines import BaseLineOptionsChartView
from django.http import HttpResponse
from django.template import loader

max_line = 0


class KeywordViewSet(viewsets.ViewSet):

    def list(self, request):

        def top_tags(university_id):
            tag_items = Keyword.objects.filter(university_id=university_id).order_by('-coef')
            counts = []
            for item in tag_items:
                counts.append(item.count)
            counts_median = numpy.median(counts) + (len(tag_items) // 100) * 2 - 2

            result_tags = []
            for item in tag_items:
                if counts_median <= item.count < counts_median * 3 and (
                        item.tag.find(' ') != -1 or item.tag.find('-') != -1):
                    # print('tag: {} | coef: {} | count: {}'.format(item.tag, item.coef, item.count))
                    result_tags.append(item)
            # print('median ' + str(counts_median))
            return result_tags

        def all_top_tags():
            top = []
            tags_text = []

            def alreadyExist(item):
                if item.tag in tags_text:
                    return True
                else:
                    return False

            for university_id in range(1, 11):
                top_tags_items = top_tags(university_id)
                i = 0
                tag = top_tags_items[i]
                while alreadyExist(tag):
                    i += 1
                    tag = top_tags_items[i]
                top.append(tag)
                tags_text.append(tag.tag)
                # print('tag: {} | coef: {} | count: {}'.format(tag.tag, tag.coef, tag.count))
            return top

        tags = all_top_tags()

        serializer = KeywordSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)


def index(request):
    template = loader.get_template('analyzer/index.html')
    return HttpResponse(template.render(request=request))


class LineChartJSONView(BaseLineOptionsChartView):

    def get_dataset_options(self, index, color):
        return []

    def get_labels(self):
        labels = [
            'COVID19',
            'BTS',
            'LGBT',
            'Last Of Us 2',
            'Empty cities'
        ]
        return labels

    def get_data(self):
        data1 = [
            666,
            541,
            433,
            325,
            277]
        return [data1]

    def get_options(self):
        return {
            'scales': {
                'xAxes': [{
                    'gridLines': {
                        'display': False
                    }
                }]
            },
            'plugins': {
                'colorschemes': {
                    'scheme': 'office.Story6'
                }
            },
            'responsive': True,
            'legend': {
                'display': False
            },
            'title': {
                'display': True,
                'text': 'Chart of university tags'
            },
            'animation': {
                'duration': 1500,
                'easing': 'easeOutSine'
            }
        }


class ComparisonChartJSONView(BaseLineOptionsChartView):

    def get_dataset_options(self, index, color):
        return []

    def get_labels(self):
        labels = [
            'ТГУ',
            'НГУ',
            'Harvard',
            'Stanford',
            'Caltech',
            'Cambridge',
            'ИТМО',
            'NUS',
            'СПбГУ',
        ]
        return labels

    def get_data(self):
        data = [
            (79 - 35) / 10,
            (59 - 35) / 10,
            (58 - 35) / 10,
            (65 - 35) / 10,
            (77 - 35) / 10,
            (71 - 35) / 10,
            (85 - 35) / 10,
            (51 - 35) / 10,
            (75 - 35) / 10,
        ]
        return [data]

    def get_options(self):
        return {
            'plugins': {
                # 'colorschemes': {
                #     'scheme': 'office.Story6'
                # }
            },
            'responsive': True,
            'legend': {
                'position': 'right',
                'labels': {
                    'boxWidth': 60
                }
            },
            'title': {
                'display': True,
                'text': 'Chart.js Doughnut Chart',
            },
            'animation': {
                'duration': 1500
            },
            # 'startAngle': math.pi
            # 'circumference': math.pi,
            # 'rotation': math.pi
        }


def calc_week_publication_number():
    count_days_ago = datetime.now() - timedelta(3*370)
    news_items = NewsItem.objects.filter(pub_date__range=[count_days_ago, datetime.now()]).order_by('-pub_date')
    today = datetime.now()
    week_ago_date = today - timedelta(days=14) + timedelta(days=-today.weekday(), weeks=1)

    label = datetime.now() + timedelta(days=-today.weekday(), weeks=1) - timedelta(days=7)
    pubNumArray = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for item in news_items:
        id = item.university_id
        news_date = item.pub_date
        while news_date < week_ago_date:
            for i in range(1, len(pubNumArray)):
                (pubNumArray[i])[label] = counts[i]
            counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            label = label - timedelta(days=28)
            week_ago_date = week_ago_date - timedelta(days=28)
        counts[id] += 1

    return pubNumArray


class NewsPerWeekChartJSONView(BaseLineOptionsChartView):

    university_array = calc_week_publication_number()

    def get_providers(self):
        queryset = University.objects.all()
        providers = []
        for university in queryset:
            providers.append(university.name)
        return providers

    def get_dataset_options(self, index, color):
        return {
            'backgroundColor': 'rgba(0, 255, 0, 0)',
            'fill': False,
            'lineTension': 0
        }

    def get_labels(self):
        dict = self.university_array[1]
        keys = dict.keys()
        dates = []
        for date_and_time in keys:
            dates.append(date_and_time.date().strftime('%b %d, %y'))
        dates.reverse()
        return dates

    def get_data(self):
        temp_data = []
        return_array = []
        for dict in self.university_array[1:]:
            temp_data = list(dict.values())
            temp_data.reverse()
            return_array.append(temp_data)

        # one_date = return_array
        # one_date.sort()
        # global max_line
        # max_line = one_date[-1]

        return return_array

    def get_options(self):
        return {
            'plugins': {
                # 'colorschemes': {
                #     'scheme': 'office.Story6'
                # }
            },
            'responsive': True,
            'title': {
                'display': True,
                'text': 'News per week'
            },
            'tooltips': {
                'mode': 'index',
            },
            'scales': {
                'yAxes': [{
                    'ticks': {
                        'suggestedMin': 0,
                        # 'suggestedMax': max_line + 1
                    }
                }]
            }
        }
