from django.shortcuts import render
from helpers.DashboardChartsProcessing import DashboardChartsProcessing
from django.http import JsonResponse

# Create your views here.
def history(request):
    return render(request, 'incomes/history.html')

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
