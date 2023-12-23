from django.shortcuts import render
from helpers.DashboardChartsProcessing import DashboardChartsProcessing
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def history(request):
    url = request.path
    context = {
        'url': url,
    }
    return render(request, 'incomes/history.html', context)

@login_required(login_url='login')
def get_incomes_history(request):
    try:
        processor = DashboardChartsProcessing(user=request.user, ticker=None, subtract_dividends_from_contribution='N')
        context = {
            'incomes_history': processor.get_incomes_history()
        }
        return JsonResponse(context)
    except ValueError as e:
        return JsonResponse({'Erro': str(e)}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'Erro': str(e)}, status=500)

@login_required(login_url='login')
def evolution(request):
    url = request.path
    context = {
        'url': url,
    }
    return render(request, 'incomes/evolution.html', context)

@login_required(login_url='login')
def get_incomes_evolution(request):
    try:
        processor = DashboardChartsProcessing(
            user=request.user,
            ticker=None,
            subtract_dividends_from_contribution='N',
            accumulate_dividends_throughout_history=False,
        )
        context = {
            'incomes_evolution': processor.get_incomes_evolution(hide_zero_dividends_months=False),
            'incomes_cards': processor.get_incomes_cards_data(),
        }
        return JsonResponse(context)
    except ValueError as e:
        return JsonResponse({'Erro': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'Erro': str(e)}, status=500)
