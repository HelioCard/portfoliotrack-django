from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
import json

from portfolio.models import PortfolioItems
from helpers.DashboardChartsProcessing import DashboardChartsProcessing

# Create your views here.
@login_required(login_url='login')
def summary(request):
    return render(request, 'portfolio/portfolioSummary.html')

@login_required(login_url='login')
def get_portfolio_summary(request, subtract_dividends):
    try:        
        processor = DashboardChartsProcessing(user=request.user, ticker=None, subtract_dividends_from_contribution=subtract_dividends)
        summary_data = processor.get_portfolio_summary()
        context = {
            'summary_data': summary_data,
        }
        return JsonResponse(context)
    except ValueError as e:
        return JsonResponse({'Erro': str(e)}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'Erro': str(e)}, status=500)
    
@login_required(login_url='login')
def balance(request):
    return render(request, 'portfolio/balance.html')

@login_required(login_url='login')
def get_balance_data(request):
    try:        
        processor = DashboardChartsProcessing(user=request.user, ticker=None, subtract_dividends_from_contribution='N')
        balance_data = processor.get_balance_data()
        context = {
            'balance_data': balance_data,
        }
        return JsonResponse(context)
    except ValueError as e:
        return JsonResponse({'Erro': str(e)}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'Erro': str(e)}, status=500)

@login_required(login_url='login')
def update_balance(request, new_weights):
    if request.method == 'POST':
        try:
            weights = json.loads(new_weights)
            objects = PortfolioItems.objects.filter(ticker__in=weights.keys())
            for obj in objects:
                obj.portfolio_weight = weights[obj.ticker]            
            PortfolioItems.objects.bulk_update(objects, ['portfolio_weight'])
            messages.success(request, 'Pesos atualizados com sucesso!')
        except Exception as e:
            print(e)
            messages.error(request, f'Erro: {e}')
    return redirect('balance')