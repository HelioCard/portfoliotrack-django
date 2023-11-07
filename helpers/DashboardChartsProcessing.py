from portfolio.models import Transactions
from .TransactionsFromFile import TransactionsFromFile
from datetime import date as dt
import numpy as np

class DashboardChartsProcessing(TransactionsFromFile):
    def __init__(self, user, ticker=None, interval='1mo'):
        super().__init__()
        self.user = user
        self.ticker = ticker
        self.interval = interval

        self.transactions_list = self._get_transactions_list()
        self.tickers_list = self.extract_tickers_list(self.transactions_list)
        self.portfolio_balance = self.calculate_portfolio_balance_and_asset_history(self.transactions_list, self.tickers_list) # -> portfolio e asset_history
        self.portfolio = self.portfolio_balance[0] # Index 0 -> somente portfolio
        self.asset_history = self.portfolio_balance[1] # Index 1 -> somente asset_history
        self.first_transaction_date = self._get_first_transaction_date()
        self.history_data = self.load_history_data_of_tickers_list(list_of_tickers=self.tickers_list, initial_date=self.first_transaction_date, interval=self.interval)
    
    def _get_transactions_list(self):
        if self.ticker is None:
            result = Transactions.objects.filter(portfolio__user=self.user)
            list_result = list(result.values())
            return self.list_of_dicts_order_by(list_result, ['date', 'ticker', 'operation'])
        else:
            result = Transactions.objects.filter(portfolio__user=self.user, ticker=self.ticker)
            list_result = list(result.values())
            return self.list_of_dicts_order_by(list_result, ['date', 'ticker', 'operation'])
    
    def _get_first_transaction_date(self):
        result = min(self.transactions_list, key=lambda x: x['date'])
        return result['date']

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

    def get_performance_chart_data(self):

        # Cria um dicionário que conterá o histórico de data, aportes acumulados, patrimônio e dividendos acumulados ao longo do tempo. Tudo isso de cada ativo:
        performance_data = {
            ticker: {
                'date': [],
                'contribution': [],
                'equity': [],
                'dividends': [],    
            } for ticker in self.history_data.keys()
        }
        
        # Percorre a lista de tickers
        for ticker in self.tickers_list:
            dividends = 0
            # Percorre os dados históricos de cada ticker:
            for data in self.history_data[ticker]:

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
                    values = self.get_values_in_a_date(data['date'], self.asset_history[ticker])
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

        # Inicializa o dicionário com todas as datas do histórico e com os valores zerados:
        for key, values in performance_data.items():
            final_performance_data['date'] = values['date']
            final_performance_data['contribution'] = [0.0] * len(values['contribution'])
            final_performance_data['equity'] = [0.0] * len(values['equity'])
            final_performance_data['dividends'] = [0.0] * len(values['dividends'])
        
        # Consolida os valores da lista somando por data
        for key, values in performance_data.items():
            for key2 in ['contribution', 'equity', 'dividends']:
                final_performance_data[key2] = [round(x + y, 2) for x, y in zip(final_performance_data[key2], values[key2])]
                
        return final_performance_data

        