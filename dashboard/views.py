from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from helpers.DashboardChartsProcessing import DashboardChartsProcessing

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def get_dashboard_data(request):
    try:
        charts = DashboardChartsProcessing(user=request.user, ticker=None, subtract_dividends_from_contribution=False)
        context = {
            'performance_data': charts.get_performance_chart_data(),
            'category_data': charts.get_category_data(),
            'asset_data': charts.get_asset_data(),
            'cards_data': charts.get_cards_data(),
        }
        return JsonResponse(context)

    except ValueError as e:
        return JsonResponse({'Erro': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'Erro': str(e)}, status=500)
