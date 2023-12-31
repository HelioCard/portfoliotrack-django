from transactions.models import Transactions
from portfolio.models import PortfolioItems, Portfolio
from .TransactionsFromFile import TransactionsFromFile
from datetime import date as dt
from datetime import datetime, timedelta
import numpy as np
import inspect
import locale
from collections import defaultdict
from datetime import datetime

class DashboardChartsProcessing(TransactionsFromFile):
    def __init__(self, user, ticker=None, subtract_dividends_from_contribution: str='N', accumulate_dividends_throughout_history: bool=True):
        super().__init__()
        self.user = user
        self.ticker = ticker.upper() if ticker else None
        self.subtract_dividends_from_contribution = subtract_dividends_from_contribution.upper()
        self.accumulate_dividends_throughout_history = accumulate_dividends_throughout_history

        self.transactions_list = self._get_transactions_list()
        if not self.transactions_list:
            raise ValueError('No data')
        self.tickers_list = self.extract_tickers_list(self.transactions_list)
        self.portfolio_items, self.asset_history = self.calculate_portfolio_balance_and_asset_history(self.transactions_list, self.tickers_list)
        self.first_transaction_date = self._get_first_transaction_date()
        self.interval = self._get_interval()
        
        self.active_tickers_list = None
        self.sum_of_weights = None
        self.weights = None
        self._get_active_tickers_list_weights_and_sum_of_weights()
        if not self.active_tickers_list:
            raise ValueError('No data')

        self.history_data = None # Dados históricos de fechamento, dividendos e splits/agrupamentos
        self.individual_performance_data = None # Dados de performance de cada ativo individualmente
        self.performance_data = None # Dados de performance consolidados (todos os ativos do portfolio)
        self.average_dividend = None
    
    def _get_interval(self):
        try:
            time_elapsed = dt.today() - self.first_transaction_date
            if time_elapsed.days < 90:
                return '1d'
            else:
                return '1mo'
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _get_transactions_list(self):
        try:
            if self.ticker is None:
                result = Transactions.objects.filter(portfolio__user=self.user)
            else:
                result = Transactions.objects.filter(portfolio__user=self.user, ticker=self.ticker)
            list_result = list(result.values())
            return self.list_of_dicts_order_by(list_result, ['date', 'ticker', 'operation'])
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')
    
    def _get_first_transaction_date(self):
        try:
            result = min(self.transactions_list, key=lambda x: x['date'])
            return result['date']
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _get_active_tickers_list_weights_and_sum_of_weights(self):
        try:
            active_tickers_list = []
            sum_of_weights = 0.0
            weights = {}
            portfolio_items = PortfolioItems.objects.filter(portfolio__user=self.user, is_active=True)
            for item in portfolio_items:
                active_tickers_list.append(item.ticker)
                sum_of_weights += item.portfolio_weight
                weights[item.ticker] = item.portfolio_weight
            self.active_tickers_list = active_tickers_list
            self.sum_of_weights = sum_of_weights
            self.weights = weights
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _load_history_data(self):
        self.history_data = self.load_history_data_of_tickers_list(list_of_tickers=self.tickers_list, initial_date=self.first_transaction_date, interval='1d')

    def _get_values_in_a_date(self, date, asset_history):
        try:
            # Classifica a lista de dicionários com base na data
            asset_history.sort(key=lambda x: x["date"])

            # Inicialize a quantidade com 0 (caso a data de entrada seja anterior à primeira data na lista)
            values = {'quantity': 0, 'average_price': 0.0}

            # Itera sobre os dicionários para encontrar a quantidade correspondente à data de entrada
            for data in asset_history:
                if data["date"] <= date:
                    values['quantity'] = data["quantity"]
                    values['average_price'] = data['average_price']
                else:
                    break

            return values
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _format_date(self, date):
        try:
            if isinstance(date, dt):
                return dt.strftime(date, '%d/%m/%Y')
            if isinstance(date, str):
                return datetime.strptime(date, '%d/%m/%Y').date()
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _older_and_newer_indexes_by_month(self, list_of_dates: list):
        # Dicionário para armazenar os índices da data mais velha e mais nova para cada mês
        indexes_by_months = defaultdict(lambda: {'older': None, 'newer': None})
        
        for i, date_ in enumerate(list_of_dates):
            _, month, year = date_.split('/')
            year_month = f'{year}/{month}'
            
            # Se não houver data mais velha registrada ou a data atual for mais antiga
            if indexes_by_months[year_month]['older'] is None or list_of_dates[indexes_by_months[year_month]['older']] > date_:
                indexes_by_months[year_month]['older'] = i
            
            # Se não houver data mais nova registrada ou a data atual for mais recente
            if indexes_by_months[year_month]['newer'] is None or list_of_dates[indexes_by_months[year_month]['newer']] < date_:
                indexes_by_months[year_month]['newer'] = i
        
        return indexes_by_months

    def _join_by_months(self, fulldata):
        try:
            joined_data:dict = {}
            for ticker, data in fulldata.items():
                # Inicia um dicionário de dicionário com o conteúdo vazio:
                joined_data[ticker] = {
                    'date': [],
                    'contribution': [],
                    'equity': [],
                    'dividends': [],
                }
                
                # Extrai da lista de datas o índice da data mais velha e o índice da data mais nova de cada mês:
                older_and_newer_indexes_by_month = self._older_and_newer_indexes_by_month(data['date'])

                # Percorre o dicionário de indices (da data mais velha e mais nova de cada mês)
                # No dados da data, adiciona o ano/mês
                # Nos dados de aportes, adiciona o dado do último dia de negociação - índice da data mais nova
                # Nos dados de patrimônio, adiciona o dado do último dia de negociação - índice da data mais nova
                # Nos dados de dividendos: se a classe estiver configurada para acumular os dividendos, adiciona o dado do
                # último dia de negociação. Se a configuração for para não acumular os dividendos, adiciona a soma do seguinte intervalo
                # de dividendos: da data mais velha até a data mais nova (índice older até índice newer):
                for year_month, indexes in older_and_newer_indexes_by_month.items():
                    joined_data[ticker]['date'].append(year_month)
                    joined_data[ticker]['contribution'].append(data['contribution'][indexes['newer']])
                    joined_data[ticker]['equity'].append(data['equity'][indexes['newer']])
                    if self.accumulate_dividends_throughout_history:
                        joined_data[ticker]['dividends'].append(data['dividends'][indexes['newer']])
                    else:
                        sum_of_dividends = sum(data['dividends'][indexes['older']:indexes['newer']+1])
                        joined_data[ticker]['dividends'].append(sum_of_dividends)

            return joined_data
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _calculate_individual_performance_data(self):
        if not self.history_data:
            self._load_history_data()
        
        try:
            # Cria um dicionário que conterá o histórico de data, aportes acumulados, patrimônio e dividendos acumulados ao longo do tempo. Tudo isso de cada ativo:
            individual_performance_data = {
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

                    '''Se houver splits ou grupamentos, atualiza o valor da lista de patrimonios obtidos até o momento,
                    porque o preço de fechamento (que vem do yfinance) está ajustado e não reflete o preço real da época:'''
                    if data['split_groupment'] > 0.0:
                        for i, equity_value in enumerate(individual_performance_data[ticker]['equity']):
                            individual_performance_data[ticker]['equity'][i] *= data['split_groupment']

                    # Se não houver dados na data especificada, preencha os dados com a data específica e os valores = 0.0
                    '''Se houver dados:
                        primeiro extrai a quantidade e o preço médio do ticker na data do dado atual;
                        depois obtem os valores de data, aportes (multiplicando o preço médio pela qtdade),
                        de patrimônio (multiplicando o fechamento pela quantidade) e de dividendos (multipli
                        cando o valor do dividendo pela quantidade - os valores de dividendos são acumulatórios)
                    '''
                    date = self._format_date(data['date'])
                    if np.isnan(data['close']):
                        acum_contribution = 0.0
                        equity = 0.0
                        dividends = 0.0
                    else:
                        values = self._get_values_in_a_date(data['date'], self.asset_history[ticker])
                        acum_contribution = values['quantity'] * values['average_price']
                        equity = values['quantity'] * data['close']
                        
                        # Condição para acumular dividendos ao longo do histórico ou não:
                        if self.accumulate_dividends_throughout_history:
                            dividends = dividends + (values['quantity'] * data['dividends'])
                        else:
                            dividends = values['quantity'] * data['dividends']
                        
                        # Subtrai os dividendos recebidos do valor dos aportes:
                        if self.subtract_dividends_from_contribution == 'Y':
                            acum_contribution = acum_contribution - dividends if (acum_contribution - dividends) > 0 else 0.0

                    # Atualiza o dicionário com o ticker e os dados obtidos acima:
                    individual_performance_data[ticker]['date'].append(date)
                    individual_performance_data[ticker]['contribution'].append(acum_contribution)
                    individual_performance_data[ticker]['equity'].append(equity)
                    individual_performance_data[ticker]['dividends'].append(dividends)

                    
            self.individual_performance_data = dict(sorted(individual_performance_data.items()))
            if self.interval == '1mo':
                joined_by_months = self._join_by_months(self.individual_performance_data)
                self.individual_performance_data = joined_by_months
            return self.individual_performance_data
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _calculate_performance_data(self):
        try:
            if self.individual_performance_data is None:
                self._calculate_individual_performance_data()

            # Cria um dicionário que conterá os dados consolidados de todos os ativos:
            performance_data = {
                'date': [],
                'contribution': [],
                'equity': [],
                'dividends': [],    
            }

            # Inicializa o dicionário com todas as datas do histórico e com os valores correspondentes zerados:
            for key, values in self.individual_performance_data.items():
                performance_data['date'] = values['date']
                performance_data['contribution'] = [0.0] * len(values['contribution'])
                performance_data['equity'] = [0.0] * len(values['equity'])
                performance_data['dividends'] = [0.0] * len(values['dividends'])
            
            # Consolida os valores da lista somando por data
            for _, values in self.individual_performance_data.items():
                for key in ['contribution', 'equity', 'dividends']:
                    performance_data[key] = list(np.round(np.add(performance_data[key], values[key]), 2))
                    # final_performance_data[key] = [round(x + y, 2) for x, y in zip(final_performance_data[key], values[key])]
            self.performance_data = performance_data
            return self.performance_data
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _calculate_percent(self, value, total): 
        try:
            if total == 0:
                return 0.0
            else:
                return value / total
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _format_float(self, value):
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            return locale.currency(value, grouping=True, symbol=False)
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_performance_chart_data(self):
        try:
            return self.performance_data if self.performance_data is not None else self._calculate_performance_data()
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_category_data(self):
        if not self.history_data:
            self._load_history_data()
        try:
            categories_set = {asset['sort_of'] for asset in self.portfolio_items.values()}
            category_data = []

            # Percorre a lista de categorias
            for category in categories_set:
                value = 0
                # Percorre todos os itens do portfolio:
                for ticker, asset in self.portfolio_items.items():
                    # Se a categoria do item do portfolio for a mesma categoria do loop inicial
                    # inclui o valor do patrimonio atual daquele ativo
                    if asset['sort_of'] == category:
                        value += asset['quantity'] * self.history_data[ticker][-1]['close'] # Obtem o último fechamento do histórico de preços

                category_data.append(
                    {
                        'value': round(value, 2),
                        'name': category,
                    }
                )
            return self.list_of_dicts_order_by(category_data, ['values',], reversed_output=True)
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_asset_data(self):
        if not self.history_data:
            self._load_history_data()
        try:
            asset_data = []
            for ticker, asset in self.portfolio_items.items():
                if asset['quantity'] > 0:
                    asset_data.append(
                        {
                            'name': ticker,
                            'value': round(asset['quantity'] * self.history_data[ticker][-1]['close'], 2)
                        }
                    )
            return self.list_of_dicts_order_by(asset_data, ['value',], reversed_output=True)
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_cards_data(self):
        try:
            # Se os dados de performance ainda não foram calculados, executa o cálculo:
            if not self.performance_data:
                self._calculate_performance_data()

            equity_data: dict = {}
            contribution_data : dict = {}
            dividends_data: dict = {}

            time_periods = {
                '1d': ['0d', '1d', '2d', '3d', '4d', '5d', '6d'],
                '1mo': ['0m', '1m', '2m', '3m', '4m', '5m', '6m'],
            }
            periods = time_periods[self.interval]
            
            iter_range = len(periods)
            for _ in range(iter_range):
                if len(self.performance_data['date']) >= len(periods):
                    for i, period in enumerate(periods):
                        equity_data[period] = self.performance_data['equity'][-(i+1)]
                        contribution_data[period] = self.performance_data['contribution'][-(i+1)]
                        dividends_data[period] = self.performance_data['dividends'][-(i+1)]
                    break
                else:
                    periods.pop()
            
            # Cálculos relacionados aos Aportes:
            current_contribution = contribution_data[periods[0]]
            initial_contribution = contribution_data[periods[-1]]
            contribution_in_period = current_contribution - initial_contribution
            contribution_change = self._calculate_percent(contribution_in_period, initial_contribution)
            contribution = {'value': current_contribution, 'period': periods[-1], 'change': contribution_change}

            # Cálculo relacionado ao Patrimônio
            current_equity = equity_data[periods[0]]
            initial_equity = equity_data[periods[-1]]
            result_in_period = current_equity - initial_equity
            equity_change = self._calculate_percent(result_in_period, initial_equity)
            equity = {'value': current_equity, 'period': periods[-1], 'change': equity_change}

            yield_ = round(current_equity - current_contribution, 2)

            # Cálculos relacionados aos Resultados (em porcentagem):
            current_result = current_equity - current_contribution
            current_result_percent = self._calculate_percent(current_result, current_contribution)
            initial_result = initial_equity - initial_contribution
            initial_result_percent = self._calculate_percent(initial_result, initial_contribution)
            result_change = current_result_percent - initial_result_percent
            result = {
                # Se o valor dos aportes for 0 e o patrimônio maior que 0 -> Investimento recuperado:
                'value': 1 if current_equity > 0 and current_contribution == 0 else current_result_percent,
                'period': periods[-1],
                'change': 0 if current_equity > 0 and current_contribution == 0 else result_change,
            }

            # Cálculo relacionados ao Yield on Cost:
            current_dividends = dividends_data[periods[0]]
            initial_dividends = dividends_data[periods[-1]]
            current_yield_on_cost = self._calculate_percent(current_dividends, current_contribution)
            initial_yield_on_cost = self._calculate_percent(initial_dividends, initial_contribution)
            yield_on_cost_change = current_yield_on_cost - initial_yield_on_cost
            yield_on_coast = {
                # Se o valor dos aportes for 0 e o patrimônio maior que 0 -> Investimento recuperado:
                'value': 1 if current_equity > 0 and current_contribution == 0 else current_yield_on_cost,
                'period': periods[-1],
                'change': 1 if current_equity > 0 and current_contribution == 0 else yield_on_cost_change
            }

            # Cálculo da recordista de dividendos:
            highest_dividend = 0.0
            ticker_of_highest_dividend = "Não há pagamentos"
            for ticker, data in self.individual_performance_data.items():
                if data['dividends'][-1] > highest_dividend:
                    highest_dividend = data['dividends'][-1]
                    ticker_of_highest_dividend = ticker

            cards_data = {
                'contribution': contribution,
                'equity': equity,
                'result': result,
                'yield_on_cost': yield_on_coast,
                'yield': yield_,
                'dividends': current_dividends,
                'highest_dividend': highest_dividend,
                'ticker_of_highest_dividend': ticker_of_highest_dividend,
            }

            return cards_data
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_contributions_over_time(self, show_months_without_contribution=False):
        try: 
            contribution_over_time:dict = {}

            final_contribution_over_time = {
                'date': [],
                'contribution': [],
            }
            
            # Percorre a lista de transações. 
            for transaction in self.transactions_list:
                # Se a operação não for de compra, pula para a próxima
                if transaction['operation'] != 'C':
                    continue
                # Obtêm o mes/ano da operação. Se o mes/ano já se encontrar na variável 'contribution_over_time' adiciona o valor total da transação
                # Se o mes/ano não for encontrado na referida variável, cria um novo par key/value
                month_year = f"{transaction['date'].year}/{transaction['date'].month}"
                if contribution_over_time.get(month_year):
                    contribution_over_time[month_year] += transaction['quantity'] * transaction['unit_price']
                else:
                    contribution_over_time[month_year] = transaction['quantity'] * transaction['unit_price']

            # Se verdadeiro, prossegue para adicionar os meses com zero contribuição.
            # Se falso, retorna o resultado
            if not show_months_without_contribution:
                for month_year, contribution in contribution_over_time.items():
                    final_contribution_over_time['date'].append(month_year)
                    final_contribution_over_time['contribution'].append(contribution)
                return final_contribution_over_time

            # Caso ainda não tenha sido calculada a performance, calcula
            if self.performance_data is None:
                self._calculate_performance_data()

            # Percorre as datas dos dados de performance
            for date_ in self.performance_data['date']:
                # Obtêm o mes/ano destas datas
                if self.interval == '1d':
                    formatted_date = self._format_date(date_)
                    month_year = f"{formatted_date.year}/{formatted_date.month}"
                else:
                    month_year = date_
                # Se o mes/ano obtido não for encontrado nos dados de aportes calculados acima, significa que não houve aportes no referido mes/ano
                # Então adiciona a data com o valor de aporte = 0.0 à variável 'contribution_over_time'
                if not contribution_over_time.get(month_year):
                    contribution_over_time[month_year] = 0.0

            # Extrai a lista de mes/ano ordenada do mais velho para a mais novo
            def extract_month_year(key):
                return datetime.strptime(key, '%Y/%m')
            list_of_months_years = sorted(contribution_over_time.keys(), key=extract_month_year)
            
            # Percorre a lista de mes/ano e adiciona um por um, na chave 'date' e na chave 'contribution'
            for month_year in list_of_months_years:
                final_contribution_over_time['date'].append(month_year)
                final_contribution_over_time['contribution'].append(contribution_over_time.get(month_year))
            
            return final_contribution_over_time
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_asset_variation_chart_data(self):
        try:
            # Cria um dicionário contendo todos os tickers com valores de variação = 0.0:
            asset_variation_data = {
                'ticker': [],
                'variation': [],
            }

            # Se ainda não foi calculada a performance individual dos ativos, calcula:
            if self.individual_performance_data is None:
                self._calculate_individual_performance_data()
            
            #Percorre os dados de performance individual de cada ativo:
            for ticker, data in self.individual_performance_data.items():
                equity = data['equity'][-1] # Obtêm o valor do patrimônio atual do ativo (último item da lista)
                if equity <= 0: # Se não houver patrimônio, ou seja, se a quantidade = 0, pula para próxima
                    continue
                contribution = data['contribution'][-1] # Obtêm o valor acumulado de aportes do ativo (último item da lista)
                income = equity - contribution # Calcula o lucro ou prejuízo do período
                variation = 1 if equity > 0 and contribution == 0 else self._calculate_percent(income, contribution) # Calcula a porcentagem do lucro ou prejuízo. Se aportes = 0, então o investimento já se pagou
                asset_variation_data['ticker'].append(ticker)
                asset_variation_data['variation'].append(round(variation * 100, 2))
            
            return asset_variation_data
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_portfolio_summary(self):
        try:
            PERCENT = 100
            if self.individual_performance_data is None:
                self._calculate_individual_performance_data()
            summary_data = []
            for ticker, data in self.portfolio_items.items():
                if data['quantity'] <= 0: # Se a posição foi fechada, não exibe.
                    continue
                last_price = self.history_data[ticker][-1]['close']
                contribution = self.individual_performance_data[ticker]['contribution'][-1]
                equity = self.individual_performance_data[ticker]['equity'][-1]
                dividends = self.individual_performance_data[ticker]['dividends'][-1]
                yield_ = equity - contribution
                result = self._calculate_percent(yield_, contribution) * PERCENT
                yield_on_cost = self._calculate_percent(dividends, contribution) * PERCENT
                temp_dict = {
                    'asset': ticker,
                    'sort_of': data['sort_of'],
                    'quantity': data['quantity'],
                    'average_price': self._format_float(data['average_price']),
                    'last_price': self._format_float(last_price),
                    'contribution': self._format_float(contribution),
                    'equity': self._format_float(equity),
                    'earnings': self._format_float(dividends),
                    'yield': self._format_float(yield_),
                    'result': self._format_float(result),
                    'yield_on_cost': self._format_float(yield_on_cost),
                }
                summary_data.append(temp_dict)
            return self.list_of_dicts_order_by(summary_data, sort_keys=['asset'], reversed_output=False)
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _adjust_asset_percent(self, total_equity, ideal_percentage, current_equity, tolerance=50.00):
        try:
            adjust = 0
            final_adjust = 0
            while abs( current_equity - (ideal_percentage * total_equity) ) > tolerance:
                adjust = ideal_percentage * total_equity - current_equity
                current_equity += adjust
                total_equity += adjust
                final_adjust += adjust
            return final_adjust
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _calculate_balance(self, temp_balance_data, total_equity, total_weight):
        try:
            PERCENT = 100
            balance_data = temp_balance_data
            for data in balance_data:
                current_percentage = self._calculate_percent(value=data['equity'], total=total_equity) * PERCENT
                ideal_percentage = self._calculate_percent(value=data['weight'], total=total_weight)
                # adjust_value =  (ideal_percentage * total_equity) - data['equity']
                adjust_value = self._adjust_asset_percent(total_equity=total_equity, ideal_percentage=ideal_percentage, current_equity=data['equity'])
                adjust_of_quotas = adjust_value / data['last_price'] if data['last_price'] != 0 else 0.0
                signal = '+' if adjust_value > 0 else ''
                
                data['last_price'] = self._format_float(data['last_price'])
                data['equity'] = self._format_float(data['equity'])
                data['current_percentage'] = self._format_float(current_percentage)
                data['ideal_percentage'] = self._format_float(ideal_percentage * PERCENT)
                data['to_balance'] = f'{signal}{int(adjust_of_quotas)} cotas: {signal}{self._format_float(adjust_value)}'
            return balance_data
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def _get_average_dividend(self, years):
        try:
            days = years * 365
            initial_date = dt.today() - timedelta(days=days)
            self.average_dividend = self.calculate_average_dividend_of_tickers_list(list_of_tickers=self.active_tickers_list, initial_date=initial_date, interval='1mo', period='yearly')
            # self.average_dividend = self.get_average_dividend_of_tickers_list(list_of_tickers=self.tickers_list)
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_balance_data(self):
        try:
            if self.individual_performance_data is None:
                self._calculate_individual_performance_data()
            if self.weights is None:
                self._get_active_tickers_list_weights_and_sum_of_weights()
            temp_balance_data = []
            total_equity = 0.0
            for ticker, data in self.portfolio_items.items():
                if data['quantity'] <= 0: # Se a posição foi fechada, não exibe.
                    continue
                last_price = self.history_data[ticker][-1]['close']
                equity = self.individual_performance_data[ticker]['equity'][-1]
                total_equity += equity
                temp_dict = {
                    'asset': ticker,
                    'quantity': data['quantity'],
                    'last_price': last_price,
                    'equity': equity,
                    'weight': self.weights[ticker],
                    'current_percentage': 0.0,
                    'ideal_percentage': 0.0,
                    'to_balance': '',
                }
                temp_balance_data.append(temp_dict)
            balance_data = self._calculate_balance(temp_balance_data=temp_balance_data, total_equity=total_equity, total_weight=self.sum_of_weights)
            return self.list_of_dicts_order_by(balance_data, sort_keys=['asset'], reversed_output=False)
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_target_data(self):
        try:
            PERCENT = 100
            if self.average_dividend is None:
                self._get_average_dividend(years=4)

            obj = Portfolio.objects.get(user=self.user)
            total_dividends_target = obj.dividends_target
            
            total_average_dividend = 0.0
            target_data = []
            
            sum_of_yield = 0.0
            for ticker in self.active_tickers_list:
                weight = self.weights[ticker]
                fraction = self._calculate_percent(value=weight, total=self.sum_of_weights)
                quantity = self.portfolio_items[ticker]['quantity']
                average_dividend = self.average_dividend[ticker]['average_dividend']
                sum_of_yield += self._calculate_percent(average_dividend, self.average_dividend[ticker]['last_price']) * PERCENT
                yearly_dividend = quantity * average_dividend
                target_yearly_dividend = total_dividends_target * fraction
                quantity_target = int(target_yearly_dividend / average_dividend) if average_dividend != 0.0 else 0
                difference = quantity_target - quantity if quantity_target != 0 and quantity < quantity_target else 0
                accomplished = self._calculate_percent(value=quantity, total=quantity_target) * PERCENT
                if accomplished > 100:
                    accomplished = 100.00
                total_average_dividend += yearly_dividend
                
                temp_dict = {
                    'ticker': ticker,
                    'quantity': quantity,
                    'quantity_target': quantity_target if quantity_target != 0 else '0',
                    'difference': difference if difference != 0 else '0',
                    'accomplished': round(accomplished, 2) if accomplished != 0 else 0.0,
                    'yearly_dividend': self._format_float(yearly_dividend),
                    'target_yearly_dividend': self._format_float(target_yearly_dividend),
                    'average_dividend': self._format_float(average_dividend),
                }
                target_data.append(temp_dict)

            average_yield = round(sum_of_yield / len(self.tickers_list), 2) if len(self.tickers_list) > 0 else 0.0
            # Valor faltante de aportes para alcançar a meta:
            missing_value = total_dividends_target - total_average_dividend if total_average_dividend < total_dividends_target else 0.0
            missing_contribution = missing_value / average_yield * PERCENT if average_yield > 0 else 0.0
            concluded = self._calculate_percent(total_average_dividend, total_dividends_target) * PERCENT
            cards_data = {
                'total_dividends_target': self._format_float(total_dividends_target),
                'total_average_dividend': self._format_float(total_average_dividend),
                'average_yield': average_yield,
                'missing_contribution': self._format_float(missing_contribution),
                'concluded': round(concluded, 2)
            }

            return self.list_of_dicts_order_by(list_of_dicts=target_data, sort_keys=['ticker'], reversed_output=False), cards_data
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_incomes_history(self):
        try:
            PERCENT = 100
            if self.history_data is None:
                self._load_history_data()
            
            incomes_history = []
            for ticker, history in self.history_data.items():
                for data in history:
                    result = self._get_values_in_a_date(data['date'], self.asset_history[ticker])
                    # Verifica a quantidade de cotas na data do anúncio. Se for 0, pula a iteração:
                    if result['quantity'] <= 0:
                        continue
                    if data['dividends'] > 0.0:
                        temp_dict = {
                            'ticker': ticker,
                            'date': data['date'],
                            'value': self._format_float(data['dividends']) if not np.isnan(data['dividends']) else 'Dados Corrompidos',
                            'dividend_yield': self._calculate_percent(data['dividends'], data['close']) * PERCENT,
                        }
                        incomes_history.append(temp_dict)
            
            return self.list_of_dicts_order_by(list_of_dicts=incomes_history, sort_keys=['date',], reversed_output=True)
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_incomes_evolution(self, hide_zero_dividends_months=False):
        try:
            PERCENT = 100
            
            # Evolução dos dividendos não precisa de acumulação dos dividendos
            # Recalcula os dados sem acumulação dos dividendos:
            self.accumulate_dividends_throughout_history = False
            self._calculate_individual_performance_data()
            self._calculate_performance_data()

            incomes_evolution: dict = {
                'date': [],
                'dividends': [],
                'yield_on_cost': [],
            }
            
            for i, _ in enumerate(self.performance_data['date']):
                dividends = self.performance_data['dividends'][i]
                if hide_zero_dividends_months:
                    if dividends <= 0:
                        continue
                date_ = self.performance_data['date'][i]
                contribution = self.performance_data['contribution'][i]
                yield_on_cost = self._calculate_percent(value=dividends, total=contribution) * PERCENT

                incomes_evolution['date'].append(date_)
                incomes_evolution['dividends'].append(dividends)
                incomes_evolution['yield_on_cost'].append(round(yield_on_cost, 2))

            return incomes_evolution
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_incomes_cards_data(self):
        try:
            PERCENT = 100
            if self.performance_data is None:
                self._calculate_performance_data()
            
            # Total de Dividendos e Yield on Cost:
            total_dividends = sum(self.performance_data['dividends'])
            total_contribution = self.performance_data['contribution'][-1]
            total_yield_on_cost = self._calculate_percent(value=total_dividends, total=total_contribution) * PERCENT

            # Cálculo da média de dividendos dos últimos meses
            # Se não houver, calcula com a quantidade de períodos disponíveis:
            dividends_data: dict = {}

            # quantidade de perídos a serem analisadas(0m, 0wk, 0d: último período. Os demais são os seis anteriores que serão usados no cálculo da média)
            time_periods = {
                '1d': ['0d', '1d', '2d', '3d', '4d', '5d', '6d'],
                '1mo': ['0m', '1m', '2m', '3m', '4m', '5m', '6m'],
            }
            # Obtem o período (diário, semanal ou mensal):
            periods = time_periods[self.interval]
            
            # Verifica se há no mínimo seis periodos para cálculo:
            iter_range = len(periods)
            for _ in range(iter_range):
                if len(self.performance_data['date']) >= len(periods):
                    for i, period in enumerate(periods):
                        dividends_data[period] = self.performance_data['dividends'][-(i+1)]
                    break
                else:
                    periods.pop()

            periods_list = list(dividends_data.keys())
            dividends_list = list(dividends_data.values())
            calculated_period = periods_list[-1] # ùltimo item da lista se refere ao período mais velho (máximo de 6)
            dividends_in_period = sum(dividends_list[1:]) # Exclui o primeiro item, que se refere ao mês/semana/dia atual
            periods_quantity = len(dividends_list[1:]) # Exclui o primeiro item, que se refere ao mês/semana/dia atual
            average_dividend = dividends_in_period / periods_quantity if periods_quantity > 0 else 0.0
            
            incomes_card_data = {
                'total_dividends': self._format_float(total_dividends),
                'total_yield_on_cost': self._format_float(total_yield_on_cost),
                'calculated_period': calculated_period,
                'average_dividend': self._format_float(average_dividend),
            }
            
            return incomes_card_data
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

