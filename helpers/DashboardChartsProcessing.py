from portfolio.models import Transactions
from .TransactionsFromFile import TransactionsFromFile
from datetime import date as dt

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

    def get_performance_chart_data(self, user):
        transactions = Transactions.objects.filter(portfolio__user=user, ticker='RANI3')
        # transactions = Transactions.objects.all()
        
        transactions_list = list(transactions.values())
        transactions_list = TransactionsFromFile().list_of_dicts_order_by(transactions_list, ['date', 'ticker', 'operation'])
        tickers_list = TransactionsFromFile().extract_tickers_list(transactions_list)
        portfolio_balance, asset_history = TransactionsFromFile().calculate_portfolio_balance_and_asset_history(transactions_list, tickers_list)
        print(asset_history)
        print()

        first_transaction = min(transactions_list, key=lambda x: x['date'])
        first_transaction_date = first_transaction['date']

        history_data = TransactionsFromFile().load_history_data_of_tickers_list(list_of_tickers=tickers_list, initial_date=first_transaction_date, interval='1mo')
        

        performance_data = {
            'date': [],
            'contribution': [],
            'equity': [],
        }
        for ticker, fulldata in history_data.items():
            for data in fulldata:
                
                values = self.get_values_in_a_date(data['date'], asset_history[ticker])
                date = dt.strftime(data['date'], '%d/%m/%Y')
                contribution = values['quantity'] * values['average_price']
                equity = values['quantity'] * data['close']

                performance_data['date'].append(date)
                performance_data['contribution'].append(contribution)
                performance_data['equity'].append(equity)

                # Se houver splits ou grupamentos, atualiza o valor do patrimonio porque o preço de fechamento está ajustado 
                # e não reflete o preço real da época:
                if data['split_groupment'] > 0.0: 
                    for i, equity_value in enumerate(performance_data['equity']):
                        performance_data['equity'][i] *= data['split_groupment']

        print(performance_data)
        return performance_data

        
        
    