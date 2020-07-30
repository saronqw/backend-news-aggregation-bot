from datetime import *

import numpy
from chartjs.views.lines import BaseLineOptionsChartView
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets
from rest_framework.response import Response

from analyzer.models import Keyword
from analyzer.serializers import KeywordSerializer
from rest_api.models import NewsItem, University

max_line = 0


def all_top_tags():
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
                result_tags.append(item)
        return result_tags

    top = []
    tags_text = []

    def already_exist(item):
        if item.tag in tags_text:
            return True
        else:
            return False

    for university_id in range(1, 11):
        top_tags_items = top_tags(university_id)
        i = 0
        tag = top_tags_items[i]
        while already_exist(tag):
            i += 1
            tag = top_tags_items[i]
        top.append(tag)
        tags_text.append(tag.tag)
    return top


class KeywordViewSet(viewsets.ViewSet):

    def list(self, request):
        tags = all_top_tags()

        serializer = KeywordSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)


def index(request):
    template = loader.get_template('analyzer/index.html')
    return HttpResponse(template.render(request=request))


class LineChartJSONView(BaseLineOptionsChartView):
    tags = all_top_tags()
    serializer = KeywordSerializer(tags, many=True)
    tags_data = sorted(serializer.data, key=lambda k: k.get('score'), reverse=True)

    def get_dataset_options(self, index, color):
        return []

    def get_labels(self):
        labels = []
        for keyword in self.tags_data:
            labels.append(keyword.get('tag'))

        return labels

    def get_data(self):
        data = []
        for keyword in self.tags_data:
            data.append(keyword.get('score'))

        return [data]

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
                    'scheme': 'tableau.Classic10'
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
                'colorschemes': {
                    'fillAlpha': 0,
                    'scheme': 'tableau.Tableau10',
                }
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
                'text': 'Collaborations with other universities',
            },
            'animation': {
                'duration': 1500
            },
            # 'startAngle': math.pi
            # 'circumference': math.pi,
            # 'rotation': math.pi
        }


def calc_week_publication_number():
    count_days_ago = datetime.now() - timedelta(3 * 370)
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


def calc_publication_words_number():
    count_days_ago = datetime.now() - timedelta(3 * 370)
    news_items = NewsItem.objects.filter(pub_date__range=[count_days_ago, datetime.now()]).order_by('-pub_date')
    today = datetime.now()
    week_ago_date = today - timedelta(days=14) + timedelta(days=-today.weekday(), weeks=1)

    label = datetime.now() + timedelta(days=-today.weekday(), weeks=1) - timedelta(days=7)
    # pubNumDict = {}
    pubWordsNumArray = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for item in news_items:
        id = item.university_id
        news_date = item.pub_date
        while news_date < week_ago_date:
            for i in range(1, len(pubWordsNumArray)):
                (pubWordsNumArray[i])[label] = counts[i]
            counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            label = label - timedelta(days=28)
            week_ago_date = week_ago_date - timedelta(days=28)
        counts[id] += len(item.full_text.split(' '))

    return pubWordsNumArray


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
                'colorschemes': {
                    'scheme': 'tableau.Classic10'
                }
            },
            'responsive': True,
            'title': {
                'display': True,
                'text': 'News per month'
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


class WordsPerWeekChartJSONView(BaseLineOptionsChartView):
    university_array = calc_publication_words_number()

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

        return return_array

    def get_options(self):
        return {
            'plugins': {
                'colorschemes': {
                    'scheme': 'tableau.Classic10'
                }
            },
            'responsive': True,
            'title': {
                'display': True,
                'text': 'Words in news per month'
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


class BoxPlotNewsChartJSONView(BaseLineOptionsChartView):

    def get_providers(self):
        providers = [
            'TPU',
            'TSU',
            'NSU',
            'Harvard',
            'Stanford',
            'Caltech',
            'Cambridge',
            'ITMO',
            'NUS',
            'SPSU',
        ]
        return providers

    def get_dataset_options(self, index, color):
        color_scheme = [
                        'rgba(31,119,180, 0.55)', 'rgba(255,127,14, 0.55)',
                        'rgba(44,160,44, 0.55)', 'rgba(214,39,40, 0.55)',
                        'rgba(148,103,189, 0.55)', 'rgba(140,86,75, 0.55)',
                        'rgba(227,119,194, 0.55)', 'rgba(127,127,127, 0.55)',
                        'rgba(188,189,34, 0.5)', 'rgba(23,190,207, 0.55)'
                    ]

        color_scheme_without_alpha = [
            'rgb(0,0,139)', 'rgb(255,69,0)',
            'rgb(0,128,0)', 'rgb(255,0,0)',
            'rgb(148,0,211)', 'rgb(139,69,19)',
            'rgb(255,20,147)', 'rgb(112,128,144)',
            'rgb(205,133,63)', 'rgb(0,128,128)'
        ]

        options = [ {}, {}, {}, {}, {}, {}, {}, {}, {}, {} ]

        color_index = 0
        for item in options:

            item.update(
                {
                    'backgroundColor': color_scheme[color_index],
                    'borderColor': color_scheme_without_alpha[color_index],
                    'borderWidth': 1,
                    'itemRadius': 0,
                }
            )
            color_index += 1

        for item in options:
            item.update(
                {
                    'borderWidth': 1,
                    'itemRadius': 0,
                }
            )

        return options[index]

    def get_labels(self):
        return [2017, 2018, 2019]

    def get_data(self):
        return [
            [
                [9, 8, 10, 8, 7, 6, 10, 7, 9, 6, 5, 8, 10, 9, 8, 7, 5, 5, 10, 8, 7, 9, 5, 6, 7, 6, 5, 8, 8, 8, 8, 9, 10, 5, 6, 7, 8, 7, 7, 5, 6, 10, 8, 10, 6, 8, 6, 5, 8, 8, 10, 9],
                [0, 3, 3, 0, 7, 4, 4, 5, 4, 6, 5, 5, 7, 0, 1, 0, 7, 1, 4, 5, 7, 7, 3, 7, 5, 7, 7, 7, 3, 5, 7, 1, 1, 6, 2, 5, 0, 1, 2, 5, 6, 5, 6, 4, 6, 5, 4, 2, 3, 5, 4, 2],
                [5, 5, 9, 5, 7, 8, 5, 2, 4, 1, 2, 3, 10, 2, 2, 10, 9, 4, 9, 3, 1, 8, 4, 3, 8, 5, 10, 4, 2, 7, 10, 8, 7, 5, 10, 9, 9, 7, 3, 3, 6, 2, 2, 7, 8, 9, 10, 5, 4, 4, 10, 1]
            ],
            [
                [9, 9, 6, 3, 11, 11, 8, 9, 4, 5, 6, 7, 6, 6, 6, 10, 9, 3, 4, 4, 10, 5, 4, 9, 4, 12, 9, 4, 4, 3, 12, 7, 10, 4, 7, 5, 5, 8, 3, 12, 6, 10, 9, 9, 9, 5, 11, 7, 7, 7, 3, 10],
                [9, 7, 7, 9, 5, 4, 9, 6, 6, 8, 4, 4, 5, 5, 6, 4, 9, 5, 5, 5, 8, 8, 4, 6, 7, 5, 6, 6, 8, 7, 7, 8, 6, 8, 6, 4, 5, 4, 9, 6, 9, 4, 6, 9, 7, 6, 9, 9, 8, 4, 4, 7],
                [7, 7, 3, 6, 6, 5, 7, 5, 3, 7, 5, 7, 5, 6, 6, 6, 4, 7, 7, 5, 4, 3, 3, 5, 3, 3, 7, 3, 5, 6, 5, 3, 4, 7, 7, 7, 6, 3, 6, 5, 3, 3, 4, 3, 5, 3, 4, 7, 4, 7, 7, 4]
            ],
            [
                [6, 3, 3, 8, 8, 7, 3, 6, 5, 4, 6, 6, 4, 5, 3, 5, 5, 4, 4, 4, 7, 3, 3, 6, 7, 5, 7, 5, 8, 6, 4, 8, 4, 3, 5, 5, 5, 4, 3, 7, 5, 4, 3, 3, 8, 7, 8, 8, 3, 4, 6, 6],
                [6, 8, 6, 3, 9, 7, 3, 7, 7, 6, 3, 3, 5, 9, 9, 10, 4, 8, 1, 2, 7, 2, 10, 10, 3, 8, 4, 7, 1, 10, 1, 5, 7, 2, 7, 6, 3, 2, 3, 1, 5, 7, 4, 5, 1, 7, 1, 10, 1, 9, 5, 4],
                [5, 2, 5, 4, 3, 2, 2, 4, 5, 3, 2, 4, 3, 4, 4, 4, 2, 3, 5, 1, 5, 3, 5, 5, 1, 6, 1, 1, 1, 3, 5, 2, 3, 2, 4, 6, 6, 5, 6, 5, 3, 5, 6, 5, 3, 1, 3, 3, 4, 2, 2, 3]
            ],
            [
                [2, 3, 8, 1, 1, 9, 4, 10, 8, 2, 3, 1, 1, 4, 7, 9, 2, 5, 7, 2, 2, 2, 9, 4, 3, 4, 2, 8, 5, 8, 2, 4, 8, 5, 7, 4, 2, 3, 2, 8, 1, 9, 8, 8, 9, 5, 6, 2, 4, 10, 6, 10],
                [9, 2, 10, 3, 8, 11, 9, 2, 5, 4, 6, 4, 9, 3, 4, 10, 10, 7, 6, 4, 5, 11, 4, 4, 10, 10, 2, 7, 4, 10, 2, 4, 3, 6, 11, 8, 9, 5, 9, 9, 3, 5, 3, 4, 8, 2, 2, 7, 7, 10, 8, 9],
                [8, 4, 4, 7, 6, 8, 2, 6, 4, 10, 5, 5, 10, 10, 1, 4, 10, 4, 5, 7, 6, 4, 2, 7, 3, 6, 6, 6, 8, 10, 8, 7, 3, 7, 3, 4, 7, 3, 3, 1, 5, 9, 1, 1, 2, 9, 3, 6, 4, 7, 1, 5]
            ],
            [
                [1, 10, 2, 6, 10, 4, 6, 7, 10, 5, 7, 4, 1, 1, 7, 6, 10, 7, 6, 10, 5, 5, 2, 2, 1, 2, 8, 8, 3, 10, 4, 8, 5, 3, 10, 9, 8, 4, 5, 2, 10, 2, 4, 1, 9, 8, 6, 5, 9, 9, 6, 9],
                [2, 4, 5, 4, 10, 3, 7, 10, 10, 7, 4, 4, 2, 3, 7, 6, 8, 4, 3, 6, 10, 1, 6, 9, 9, 1, 4, 3, 6, 7, 2, 9, 10, 7, 1, 9, 4, 7, 6, 8, 5, 5, 4, 5, 6, 9, 6, 4, 6, 4, 6, 10],
                [6, 9, 8, 5, 7, 7, 9, 8, 8, 9, 5, 5, 5, 5, 8, 7, 9, 8, 8, 5, 6, 6, 4, 8, 8, 5, 7, 6, 4, 6, 4, 8, 7, 5, 7, 6, 8, 5, 8, 4, 5, 8, 8, 7, 7, 5, 9, 8, 7, 8, 4, 9]
            ],
            [
                [5, 1, 9, 8, 10, 4, 3, 8, 1, 5, 2, 7, 2, 3, 8, 10, 4, 8, 3, 10, 8, 8, 1, 3, 10, 5, 8, 2, 10, 4, 9, 7, 7, 10, 1, 8, 1, 1, 8, 4, 7, 10, 7, 1, 8, 2, 10, 5, 7, 10, 10, 8],
                [1, 3, 2, 0, 1, 6, 0, 2, 4, 7, 2, 3, 6, 6, 4, 0, 2, 2, 3, 6, 1, 1, 7, 0, 1, 7, 7, 1, 1, 4, 4, 3, 7, 0, 1, 0, 2, 0, 2, 0, 7, 1, 2, 6, 5, 0, 0, 0, 2, 6, 2, 2],
                [3, 10, 4, 5, 5, 1, 10, 7, 6, 6, 7, 5, 1, 6, 4, 4, 5, 6, 4, 8, 4, 1, 7, 10, 8, 7, 9, 10, 9, 3, 6, 6, 3, 2, 9, 4, 10, 1, 2, 6, 10, 7, 9, 5, 6, 10, 4, 10, 6, 3, 5, 8]
            ],
            [
                [4, 4, 7, 6, 5, 7, 3, 3, 4, 2, 2, 2, 4, 6, 3, 4, 2, 7, 7, 4, 6, 6, 7, 6, 6, 4, 4, 4, 7, 6, 2, 4, 6, 3, 5, 5, 6, 7, 4, 3, 6, 7, 7, 5, 6, 5, 6, 3, 7, 7, 6, 3],
                [1, 2, 5, 4, 2, 2, 4, 1, 4, 4, 4, 2, 1, 2, 5, 4, 1, 4, 1, 5, 3, 4, 3, 1, 2, 1, 1, 3, 5, 3, 4, 3, 3, 2, 5, 2, 5, 4, 5, 1, 3, 3, 5, 2, 1, 1, 2, 2, 2, 1, 5, 3],
                [7, 7, 5, 8, 6, 2, 7, 9, 5, 9, 2, 6, 2, 4, 10, 10, 9, 5, 9, 8, 6, 10, 6, 8, 3, 7, 7, 4, 6, 4, 4, 10, 10, 8, 10, 3, 7, 5, 5, 4, 3, 7, 10, 5, 7, 10, 4, 10, 7, 4, 9, 8]
            ],
            [
                [4, 3, 5, 6, 7, 6, 7, 7, 5, 5, 3, 4, 6, 3, 6, 4, 4, 6, 6, 7, 3, 4, 5, 6, 4, 3, 6, 4, 6, 4, 6, 6, 5, 6, 4, 5, 3, 5, 7, 6, 6, 4, 4, 3, 7, 7, 3, 5, 6, 7, 6, 4],
                [2, 6, 4, 6, 6, 6, 4, 6, 8, 5, 8, 5, 4, 6, 7, 5, 3, 6, 2, 6, 6, 7, 6, 4, 7, 5, 4, 8, 8, 8, 8, 3, 2, 8, 6, 7, 7, 6, 8, 5, 5, 2, 3, 3, 2, 8, 2, 6, 5, 2, 5, 6],
                [5, 4, 5, 5, 3, 3, 6, 7, 6, 3, 7, 3, 6, 6, 6, 6, 6, 4, 3, 5, 6, 7, 5, 6, 4, 3, 3, 5, 6, 7, 6, 7, 5, 3, 7, 4, 4, 3, 7, 5, 7, 4, 3, 4, 7, 4, 6, 7, 5, 7, 4, 6]
            ],
            [
                [5, 6, 7, 4, 7, 8, 9, 6, 7, 8, 7, 5, 4, 6, 6, 4, 6, 8, 6, 3, 4, 9, 3, 5, 6, 7, 7, 6, 8, 7, 5, 6, 3, 6, 9, 7, 4, 9, 7, 7, 7, 6, 3, 9, 5, 8, 9, 3, 7, 3, 7, 5],
                [6, 6, 6, 4, 5, 2, 6, 9, 7, 5, 3, 3, 4, 5, 5, 6, 4, 7, 2, 3, 2, 7, 3, 7, 5, 5, 2, 9, 9, 8, 3, 2, 9, 4, 2, 2, 3, 4, 6, 5, 7, 7, 8, 6, 8, 5, 8, 2, 9, 5, 2, 7],
                [9, 4, 5, 5, 10, 6, 6, 7, 7, 4, 7, 5, 7, 9, 8, 7, 9, 4, 9, 9, 6, 8, 6, 6, 7, 5, 4, 7, 9, 5, 7, 7, 9, 8, 10, 8, 5, 8, 10, 4, 9, 5, 8, 7, 9, 6, 9, 5, 6, 4, 9, 7]
            ],
            [
                [1, 5, 8, 10, 5, 3, 3, 6, 2, 1, 8, 5, 7, 2, 10, 7, 4, 8, 2, 6, 1, 6, 4, 2, 6, 8, 6, 4, 5, 10, 7, 10, 1, 9, 8, 1, 9, 10, 4, 8, 6, 10, 3, 6, 4, 3, 6, 7, 4, 6, 1, 3],
                [7, 6, 8, 7, 4, 3, 1, 2, 6, 3, 4, 4, 10, 5, 4, 8, 1, 8, 3, 9, 4, 7, 5, 3, 1, 9, 5, 10, 4, 4, 1, 9, 8, 2, 1, 1, 7, 1, 9, 8, 10, 9, 9, 7, 10, 9, 6, 1, 9, 10, 4, 5],
                [8, 2, 9, 4, 5, 7, 4, 7, 9, 3, 1, 7, 5, 9, 4, 4, 2, 9, 5, 7, 9, 3, 4, 7, 1, 1, 4, 6, 3, 2, 6, 2, 1, 3, 1, 8, 2, 7, 5, 8, 2, 3, 9, 4, 8, 3, 2, 3, 7, 9, 3, 9]
            ]
        ]

    def get_options(self):
        return {
            'responsive': True,
            'legend': {
                'position': 'top',
            },
            'title': {
                'display': True,
                'text': 'Box Plot Chart'
            }
        }
