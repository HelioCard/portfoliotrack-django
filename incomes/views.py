from django.shortcuts import render
from helpers.DashboardChartsProcessing import DashboardChartsProcessing
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def history(request):
    return render(request, 'incomes/history.html')

@login_required(login_url='login')
def get_incomes_history(request):
    try:
        incomes_history = DashboardChartsProcessing(user=request.user, ticker=None, subtract_dividends_from_contribution='N')
        context = {
            'incomes_history': incomes_history.get_incomes_history()
        }
        return JsonResponse(context)
    except ValueError as e:
        return JsonResponse({'Erro': str(e)}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'Erro': str(e)}, status=500)

@login_required(login_url='login')
def evolution(request):
    return render(request, 'incomes/evolution.html')

@login_required(login_url='login')
def get_incomes_evolution(request):
    return JsonResponse({
        'incomes_evolution_chart_data': ['data1', 'data2'],
        'incomes_cards_data': {
            'data1': 'data1',
            'data2': 'data2',
            'data3': 'data3',
        }
    })
