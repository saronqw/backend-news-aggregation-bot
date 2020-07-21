from chartjs.views.lines import BaseLineOptionsChartView
from django.http import HttpResponse
from django.template import loader

from rest_api.models import NewsItem


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def index(request):
    template = loader.get_template('analyzer/index.html')
    return HttpResponse(template.render(request=request))


class LineChartJSONView(BaseLineOptionsChartView):

    def get_dataset_options(self, index, color):
        return []

    def get_labels(self):
        return [
            ['Big', 'Data'],
            ['Носки с', 'сандалиями'],
            ['Искусственный', 'интеллект'],
            ['Разумное', 'потребление'],
            ['5G', 'internet'],
            ['Пустые', 'города'],
            ['Last Of', 'Us 2'],
            'LGBT',
            'BTS',
            'COVID19'
        ]

    def get_data(self):
        return [[16, 32, 64, 128, 256, 277, 325, 433, 629, 666]]

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
                'text': 'Chart of university tags',
                'fontSize': 32
            },
            'animation': {
                'duration': 1600,
                'easing': 'easeOutSine'
            }
        }
