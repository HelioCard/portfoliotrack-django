from portfolio.models import Transactions
from .TransactionsFromFile import TransactionsFromFile
from datetime import date as dt
import numpy as np

class DashboardChartsProcessing(TransactionsFromFile):
    def __init__(self):
        super().__init__()
    
    def get_values_in_a_date(self, date, asset_history):
        
        # Classifica a lista de dicionários com base na data
        asset_history.sort(key=lambda x: x["date"])

        # Inicialize a quantidade com 0 (caso a data de entrada seja anterior à primeira data na lista)
        values = {'quantity': 0, 'average_price': 0.0}

        # Itere sobre os dicionários para encontrar a quantidade correspondente à data de entrada
        for data in asset_history:
            if data["date"] <= date:
                values['quantity'] = data["quantity"]
                values['average_price'] = data['average_price']
            else:
                break

        return values

    def get_performance_chart_data(self, user, ticker=None):
        # Extrai as transações do usuário. Pode ser um ticker específico ou todas elas:
        if ticker is None:
            transactions = Transactions.objects.filter(portfolio__user=user)
        else:
            transactions = Transactions.objects.filter(portfolio__user=user, ticker=ticker)
        
        # Processa as transações convertendo-as em listas e ordenando-as por data, ticker e operação
        transactions_list = list(transactions.values())
        transactions_list = TransactionsFromFile().list_of_dicts_order_by(transactions_list, ['date', 'ticker', 'operation'])

        # Extrai a lista de tickers das transações e extrai o histórico de quantidade e preço médio ao longo do tempo:
        tickers_list = TransactionsFromFile().extract_tickers_list(transactions_list)
        portfolio_balance, asset_history = TransactionsFromFile().calculate_portfolio_balance_and_asset_history(transactions_list, tickers_list)
        
        # Extrai a data da transação mais antiga:
        first_transaction = min(transactions_list, key=lambda x: x['date'])
        first_transaction_date = first_transaction['date']

        # Extrai o histórico de cotações no intervalo mensal de cada ativo:
        history_data = TransactionsFromFile().load_history_data_of_tickers_list(list_of_tickers=tickers_list, initial_date=first_transaction_date, interval='1mo')
        
        # Cria um dicionário que conterá o histórico de data, aportes acumulados, patrimônio e dividendos acumulados ao longo do tempo. Tudo isso de cada ativo:
        performance_data = {
            ticker: {
                'date': [],
                'contribution': [],
                'equity': [],
                'dividends': [],    
            } for ticker in history_data.keys()
        }
        
        # Percorre a lista de tickers
        for ticker in tickers_list:
            dividends = 0
            # Percorre os dados históricos de cada ticker:
            for data in history_data[ticker]:

                # Se não houver dados na data especificada, preencha os dados com a data e valores = 0.0
                '''Se houver dados:
                    primeiro extrai a quantidade e o preço médio do ticker na data do dado atual;
                    depois obtem os valores de data, aportes (multiplicando o preço médio pela qtdade),
                    de patrimônio (multiplicando o fechamento pela quantidade) e de dividendos (multipli
                    cando o valor do dividendo pela quantidade - os valores de dividendos são acumulatórios)
                  '''
                if np.isnan(data['close']):
                    date = dt.strftime(data['date'], '%d/%m/%Y')
                    contribution = 0.
                    equity = 0.0
                    dividends = 0.0
                else:
                    values = self.get_values_in_a_date(data['date'], asset_history[ticker])
                    date = dt.strftime(data['date'], '%d/%m/%Y')
                    contribution = values['quantity'] * values['average_price']
                    equity = values['quantity'] * data['close']
                    dividends = dividends + values['quantity'] * data['dividends']

                # Atualiza o dicionário com o ticker e os dados obtidos acima:
                performance_data[ticker]['date'].append(date)
                performance_data[ticker]['contribution'].append(contribution)
                performance_data[ticker]['equity'].append(equity)
                performance_data[ticker]['dividends'].append(dividends)

                '''Se houver splits ou grupamentos, atualiza o valor da lista de patrimonios obtidos até o momento,
                porque o preço de fechamento (que vem do yfinance) está ajustado e não reflete o preço real da época:'''
                if data['split_groupment'] > 0.0: 
                    for i, equity_value in enumerate(performance_data[ticker]['equity']):
                        performance_data[ticker]['equity'][i] *= data['split_groupment']

        # Cria um dicionário que conterá os dados consolidados de todos os ativos:
        final_performance_data = {
            'date': [],
            'contribution': [],
            'equity': [],
            'dividends': [],    
        }
        for key, values in performance_data.items():
            final_performance_data['date'] = values['date']
            final_performance_data['contribution'] = [0.0] * len(values['contribution'])
            final_performance_data['equity'] = [0.0] * len(values['equity'])
            final_performance_data['dividends'] = [0.0] * len(values['dividends'])
        
        for key, values in performance_data.items():
            for key2 in ['contribution', 'equity', 'dividends']:
                final_performance_data[key2] = [round(x + y, 2) for x, y in zip(final_performance_data[key2], values[key2])]
                
  
        return final_performance_data

        
        
    