from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from portfolio.models import Transactions, Portfolio
from helpers.DashboardChartsProcessing import DashboardChartsProcessing

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def get_dashboard_data(request):
    
    performance_data = DashboardChartsProcessing().get_performance_chart_data(request.user)
       

    performance_options = {
        'title': {
            'text': 'Aportes Acum. x Patrimônio x Dividendos Acum.',
            'left': 'center',
        },
        'tooltip': {
            'trigger': 'axis'
        },
        'legend': {
            'data': ['Aportes Acumulados', 'Patrimônio', 'Dividendos Acumulados'],
            'top': 30,
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '3%',
            'containLabel': True
        },
    
        'xAxis': {
            'type': 'category',
            'data': performance_data['date'],
        },
        'yAxis': {
            'type': 'value'
        },
        'series': [
            
            {
                'name': 'Aportes Acumulados',
                'type': 'line',
                'data': performance_data['contribution'],
                'smooth': False,
                'step': 'end',
                # 'itemStyle': {
                #     'barBorderRadius': [4,4,0,0],
                    
                # },
            },
        
            {
                'name': 'Patrimônio',
                'type': 'line',
                'yAxisIndex': 0,
                'data': performance_data['equity'],
                'smooth': True,  
            },
            {
                'name': 'Dividendos Acumulados',
                'type': 'line',
                'step': 'end',
                'yAxisIndex': 0,
                'data': performance_data['dividends'],
                'smooth': False,  
            }
        ]
    }

    category_data = {
        'title': {
            'text': 'Exposição por Categorias',
            'left': 'center'
        },
        'tooltip': {
            'trigger': 'item',
            'formatter': '{a} <br/>{b}: {c} ({d}%)'
        },
        
        'series': [
            {
                'name': 'Portifolio por Categoria',
                'type': 'pie',
                'radius': ['40%', '60%'],
                'avoidLabelOverlap': False,
                'itemStyle': {
                    'borderJoin': 'round',
                    'borderRadius': '5%',
                    'borderCap': 'round',
                    'borderWidth': 2,
                    'borderColor': '#ffffff',
                },
                'label': {
                    'show': True,
                    'position': 'outside',
                    'formatter': '{b}: {d}%',
                },
                'emphasis': {
                    'label': {
                        'show': True,
                        'fontWeight': 'bold'
                    }
                },
                'labelLine': {
                    'show': True,
                },
                'data': [
                    {'value': 335, 'name': 'Tes. Direto'},
                    {'value': 310, 'name': 'Ações'},
                    {'value': 234, 'name': 'Fundos Imobil.'},
                ]
            }
        ]
    }
    
    asset_data = {
        'title': {
            'text': 'Exposição por Ativos',
            'left': 'center'
        },
        'tooltip': {
            'trigger': 'item',
            'formatter': '{a} <br/>{b}: {c} ({d}%)'
        },
        
        
        'series': [
            {
                'name': 'Portifolio por Ativos',
                'type': 'pie',
                'radius': ['40%', '60%'],
                'avoidLabelOverlap': False,
                'itemStyle': {
                    'borderJoin': 'round',
                    'borderRadius': '5%',
                    'borderCap': 'round',
                    'borderWidth': 2,
                    'borderColor': '#ffffff',
                },
                'label': {
                    'show': True,
                    'position': 'outside',
                    'formatter': '{b}: {d}%',
                },
                'emphasis': {
                    'label': {
                        'show': True,
                        'fontWeight': 'bold'
                    }
                },
                'labelLine': {
                    'show': True,
                },
                'data': [
                    {'value': 335, 'name': 'TRPL4'},
                    {'value': 310, 'name': 'KLBN11'},
                    {'value': 234, 'name': 'JALL3'},
                    {'value': 135, 'name': 'NINJ3'},
                    {'value': 438, 'name': 'TAEE11'},
                    {'value': 256, 'name': 'SORT6'},
                    {'value': 512, 'name': 'BUND9'},
                    {'value': 700, 'name': 'CUCU2'},
                    {'value': 1548, 'name': 'CHAN5'}
                ]
            }
        ]
    }
    context = {
        'performance_data': performance_options,
        'category_data': category_data,
        'asset_data': asset_data,
    }
    return JsonResponse(context)

    