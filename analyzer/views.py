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
        labels = [
            # ['Big', 'Data'],
            # ['Носки с', 'сандалиями'],
            # ['Искусственный', 'интеллект'],
            # ['Разумное', 'потребление'],
            # ['5G', 'internet'],
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
            # 16,
            # 32,
            # 64,
            # 128,
            # 256,
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
                'text': 'Chart of university tags',
                'fontSize': 36
            },
            'animation': {
                'duration': 1600,
                'easing': 'easeOutSine'
            }
        }
