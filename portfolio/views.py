from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import json
import locale

from portfolio.models import PortfolioItems, Portfolio
from.forms import UpdatePortfolioDividendsTarget
from helpers.DashboardChartsProcessing import DashboardChartsProcessing

# Create your views here.
@login_required(login_url='login')
def summary(request):
    url = request.path
    context = {
        'url': url,
    }
    return render(request, 'portfolio/portfolioSummary.html', context)

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
    url = request.path
    context = {
        'url': url,
    }
    return render(request, 'portfolio/balance.html', context)

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
            objects = PortfolioItems.objects.filter(portfolio__user=request.user, ticker__in=weights.keys())
            for obj in objects:
                obj.portfolio_weight = weights[obj.ticker]            
            PortfolioItems.objects.bulk_update(objects, ['portfolio_weight'])
            messages.success(request, 'Pesos atualizados com sucesso!')
        except Exception as e:
            print(e)
            messages.error(request, f'Erro: {e}')
    return redirect('balance')

@login_required(login_url='login')
def target(request):
    url = request.path
    if request.method == 'POST':
        form = UpdatePortfolioDividendsTarget(request.POST)
        if form.is_valid():
            try:
                portfolio = Portfolio.objects.get(user=request.user)
                new_value = float(request.POST['dividends_target'])
                portfolio.dividends_target = new_value
                locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
                new_value = locale.currency(new_value, grouping=True, symbol=True)
                portfolio.save()
                messages.success(request, f'Meta atualizada com sucesso. Novo valor: {new_value}')
            except ObjectDoesNotExist as e:
                messages.error(request, f'Erro: {str(e)}')
                return redirect('target')
        else:
            messages.error(request, form.errors['__all__'])
        return redirect('target')
    
    update_dividends_target_form = UpdatePortfolioDividendsTarget()
    context = {
        'update_dividends_target_form': update_dividends_target_form,
        'url': url,
    }
    return render(request, 'portfolio/target.html', context)

@login_required(login_url='login')
def get_target_data(request):
    try:        
        processor = DashboardChartsProcessing(user=request.user, ticker=None, subtract_dividends_from_contribution='N')
        target_data, cards_data = processor.get_target_data()
        context = {
            'target_data': target_data,
            'cards_data': cards_data,
        }
        return JsonResponse(context)
    except ValueError as e:
        return JsonResponse({'Erro': str(e)}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'Erro': str(e)}, status=500)

@login_required(login_url='login')
def asset(request, ticker):
    url = '/portfolio/asset/'
    context = {
        'ticker': ticker,
        'url': url,
    }
    return render(request, 'portfolio/asset.html', context)

@login_required(login_url='login')
def get_asset_data(request, ticker, subtract_dividends):
    try:        
        processor = DashboardChartsProcessing(
            user=request.user,
            ticker=ticker,
            subtract_dividends_from_contribution=subtract_dividends,
            accumulate_dividends_throughout_history=True,
        )
        context = {
            'performance_data': processor.get_performance_chart_data(),
            'cards_data': processor.get_cards_data(),
            'contribution_data': processor.get_contributions_over_time(show_months_without_contribution=True),
            'dividend_evolution_data': processor.get_incomes_evolution(hide_zero_dividends_months=False),
        }
        return JsonResponse(context)
    except ValueError as e:
        return JsonResponse({'Erro': str(e)}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'Erro': str(e)}, status=500)