import math

from chartjs.views.lines import BaseLineOptionsChartView
from django.http import HttpResponse
from django.template import loader

max_line = 0


def index(request):
    template = loader.get_template('analyzer/index.html')
    return HttpResponse(template.render(request=request))


class LineChartJSONView(BaseLineOptionsChartView):

    def get_dataset_options(self, index, color):
        return []

    def get_labels(self):
        labels = [
            'Empty cities',
            'Last Of Us 2',
            'LGBT',
            'BTS',
            'COVID19'
        ]
        labels.reverse()
        return labels

    def get_data(self):
        data = [
            277,
            325,
            433,
            541,
            666]
        data.reverse()
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
            'TSU',
            'Harvard',
            'NSU',
            'ITMO',
            'Cambridge'
        ]
        return labels

    def get_data(self):
        data = [
            66,
            54,
            11,
            78,
            32
        ]
        # [ [] ]
        return [data]

    def get_options(self):
        return {
            'plugins': {
                'colorschemes': {
                    'scheme': 'office.Story6'
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
                'text': 'Chart.js Doughnut Chart',
            },
            'animation': {
                'duration': 1500
            },

            'circumference': math.pi,
            'rotation': math.pi
        }


class NewsPerWeekChartJSONView(BaseLineOptionsChartView):

    def get_providers(self):
        return ['TPU', 'Harvard', 'NSU', 'TSU', 'Cambridge']

    def get_dataset_options(self, index, color):
        return {
            'backgroundColor': 'rgba(0, 255, 0, 0)',
            'fill': False,
            'lineTension': 0
        }

    def get_labels(self):
        return [
            '27.03',
            '04.05',
            '11.05',
            '18.05',
            '25.05',
            '01.06',
            '08.06',
            '15.06',
            '22.06',
            '29.06',
            '06.07',
            '13.07',
            '20.07'
        ]

    def get_data(self):
        data1 = [1, 8, 4, 6, 7, 4, 4, 6, 8, 7, 2, 8, 3]
        data2 = [5, 2, 4, 7, 6, 3, 5, 2, 3, 8, 7, 4, 4]
        data3 = [8, 8, 3, 6, 8, 2, 3, 2, 2, 2, 3, 5, 2]
        data4 = [4, 5, 7, 2, 2, 2, 1, 7, 8, 3, 8, 1, 6]
        data5 = [3, 5, 8, 5, 2, 3, 8, 3, 7, 1, 2, 2, 6]
        one_date = data1 + data2 + data3 + data4 + data5
        one_date.sort()
        global max_line
        max_line = one_date[-1]
        return [data1, data2, data3, data4, data5]

        # dataset1 = {
        #     'label': 'TPU',
        #     'data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        #     'backgroundColor': 'rgba(0, 255, 0, 0)',
        #     'fill': False,
        #     'lineTension': 0
        # }
        #
        # data = [
        #     dataset1,
        # ]
        #
        # return data

    def get_options(self):
        return {
            'plugins': {
                'colorschemes': {
                    'scheme': 'office.Story6'
                }
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
                        'suggestedMax': max_line + 1
                    }
                }]
            }
        }
