from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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