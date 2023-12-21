import numpy as np
from datetime import date
import datetime as dt
import yfinance as yf
from .Cache.cache import session
import inspect

class DataFromYFinance:
    
    #########################################################
    #### SORT A LIST OF LISTS BASED ON A LIST OF INDEXES ####
    #########################################################

    def list_of_lists_order_by(self, list_of_lists, indexes, reversed_output=False):
        """
        Ordena uma lista de listas com base em uma lista de índices fornecidos.

        Args:
            list_of_lists (list): A lista de listas a ser ordenada.
            indexes (list): A lista de índices para a ordem de classificação.
            reversed (bool, optional): Se True, a lista será ordenada em ordem reversa. Padrão é False.

        Returns:
            list: A lista de listas ordenada.
        """
        
        def sort_key(item):
            """
            Função de chave personalizada para ordenação.
            Exemplo de retorno: (item[0], item[1], item[2]) ... etc
            """
            i = tuple(item[index] for index in indexes)
            return i

        # Ordenar a lista de listas com base na data
        ordered_list = sorted(list_of_lists, key=sort_key, reverse=reversed_output)
        return ordered_list







    #########################################################
    #### SORT A LIST OF DICTS BASED ON A LIST OF KEYS    ####
    #########################################################

    def list_of_dicts_order_by(self, list_of_dicts, sort_keys, reversed_output=False):
        def sort_keys_(item):
            return [item.get(key, None) for key in sort_keys]

        sorted_list_of_dicts = sorted(list_of_dicts, key=sort_keys_, reverse=reversed_output)
        return sorted_list_of_dicts






    ####################################
    ###### GET SPLITS/GROUPMENTS  ######
    ####################################

    def _get_splits_groupments(self, ticker):
        try:
            assets = yf.Ticker(ticker, session=session)
            dict_result = assets.splits.to_dict()

            list_of_splits = []
            for date, ratio in dict_result.items():
                if ticker == 'B3SA3.SA' and date.date() == dt.date(2021, 5, 6): # Correção manual de um erro da api, que inclui um evento de split inexistente no dia 06/05/2021 para o ticker B3SA3.SA
                    continue
                
                try:
                    date.date()
                    float(ratio)
                except Exception as e:
                    print(f'Erro: {e}. Dados perdidos: {ticker[:-3]}: data {date}, ratio {ratio}')
                    continue

                temp_dict = {
                    'date': date.date(),
                    'ratio': ratio,
                    'ticker': ticker[:-3],
                }
                list_of_splits.append(temp_dict)
            return list_of_splits
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def load_splits_groupments(self, ticker):
        ticker = ticker.upper() + '.SA'
        return self._get_splits_groupments(ticker)





    
    ###################################
    ###### GET DIVIDENDS         ######
    ###################################

    def _get_dividends(self, ticker):
        try:
            assets = yf.Ticker(ticker, session=session)
            dict_result = assets.dividends.to_dict()

            list_of_splits = []
            for date, value in dict_result.items():
                temp_dict = {
                    'date': date.date(),
                    'value': value,
                    'ticker': ticker[:-3],
                }
                list_of_splits.append(temp_dict)
            return list_of_splits
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def load_dividends(self, ticker):
        ticker = ticker.upper() + '.SA'
        return self._get_dividends(ticker.upper())
    







    #################################################
    ###### GET DIVIDENDS OF A LIST OF TICKERS  ######
    #################################################

    def _get_dividends_of_tickers_list(self, list_of_tickers):
        try:
            raw_data = yf.Tickers(list_of_tickers, session=session)
  
            final_dict: dict = {}
            for ticker in list_of_tickers:
                dict_result = raw_data.tickers[ticker].dividends.to_dict()
   
                for date, value in dict_result.items():
                    temp_dict = {
                        'ticker': ticker[:-3],
                        'date': date.date(),
                        'value': value,
                    }
                    
                    if ticker[:-3] not in final_dict:
                        final_dict[ticker[:-3]] = []
                    final_dict[ticker[:-3]].append(temp_dict)

            return final_dict

        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def load_dividends_of_tickers_list(self, list_of_tickers=list):
        list_of_tickers = [ticker.upper() + '.SA' for ticker in list_of_tickers]
        return self._get_dividends_of_tickers_list(list_of_tickers)







    #########################################################
    ###### GET SPLITS/GROUPMENTS OF A LIST OF TICKERS  ######
    #########################################################

    def _get_splits_groupments_of_tickers_list(self, list_of_tickers):
        try:
            raw_data = yf.Tickers(list_of_tickers, session=session)
  
            final_dict: dict = {}
            for ticker in list_of_tickers:
                dict_result = raw_data.tickers[ticker].splits.to_dict()
   
                for date, value in dict_result.items():
                    if ticker == 'B3SA3.SA' and date.date() == dt.date(2021, 5, 6): # correção manual de um evento (dia 06/05/2021) inexistente de split adicionado para o ticker 'B3SA3.SA'
                        continue
                    temp_dict = {
                        'ticker': ticker[:-3],
                        'date': date.date(),
                        'value': value,
                    }
                    
                    if ticker[:-3] not in final_dict:
                        final_dict[ticker[:-3]] = []
                    final_dict[ticker[:-3]].append(temp_dict)

            return final_dict

        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def load_splits_groupments_of_tickers_list(self, list_of_tickers=list):
        list_of_tickers = [ticker.upper() + '.SA' for ticker in list_of_tickers]
        return self._get_splits_groupments_of_tickers_list(list_of_tickers)




    


    ################################
    ###### GET HISTORY DATA   ######
    ################################

    def _get_history_data(self, list_of_tickers, initial_date, ending_date, interval):
        try:
            raw_data = yf.download(list_of_tickers, start=initial_date, end=ending_date, group_by='ticker', interval=interval, repair=False, actions=True, session=session)
            
            final_dict: dict = {}
            for ticker in list_of_tickers: # Percorre a lista de tickers

                # Obtem os dados referente ao ticker, no formato dicionário
                temp_result = raw_data[ticker] if len(list_of_tickers) > 1 else raw_data
                temp_result.reset_index(inplace=True) # Nivela o index de todas as colunas do df
                selected_data = temp_result[['Date', 'Close', 'Dividends', 'Stock Splits']].values.tolist()

                for data in selected_data:
                    try:
                        data[0].date()
                        float(data[1])
                        float(data[2])
                        float(data[3])
                    except Exception as e:
                        print(f'Erro: {e}. Dados perdidos: {ticker}: data: {data[0]}, close: {data[1]}, dividends: {data[2]}')
                        continue

                    temp_dict = {
                        'ticker': ticker[:-3],
                        'date': data[0].date(),
                        'close': data[1],
                        'dividends': data[2],
                        'split_groupment': data[3],
                    }

                    # correção manual de um evento
                    # (dia 06/05/2021 no intervalo '1d' )
                    # (dia 03/05/2021 no intervalo '1wk' )
                    # (dia 01/05/2021 no intervalo '1mo' )
                    # inexistente de split adicionado para o ticker 'B3SA3.SA':
                    if ticker == 'B3SA3.SA':
                        if interval=='1d':
                            if data[0].date() == dt.date(2021, 5, 6):
                                temp_dict['split_groupment'] = 0.0
                        elif interval == '1wk':
                            if data[0].date() == dt.date(2021, 5, 3):
                                temp_dict['split_groupment'] = 0.0
                        elif interval == '1mo':
                            if data[0].date() == dt.date(2021, 5, 1):
                                temp_dict['split_groupment'] = 3.0


                    if ticker[:-3] not in final_dict:
                        final_dict[ticker[:-3]] = []
                    final_dict[ticker[:-3]].append(temp_dict)

            return final_dict

        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def load_history_data_of_tickers_list(self, list_of_tickers: list, initial_date: date, ending_date: date=None, interval='1d'):
        if ending_date is None: ending_date = date.today()
        list_of_tickers = [ticker.upper() + '.SA' for ticker in list_of_tickers]
        return self._get_history_data(list_of_tickers, initial_date, ending_date, interval)





    ##############################################################
    ###### CALCULATE AVERAGE DIVIDEND ANNUALY DATA - MANNUALY ######
    ##############################################################

    def _calculate_average_dividend_data(self, list_of_tickers, initial_date, ending_date, interval, period):
        try:
            TWELVE_MONTHS = 12
            if (ending_date - initial_date).days < 180:
                raise ValueError('Datas inicial e final inválidas. Período mínimo permitido: 180 dias atrás')
            raw_data = yf.download(list_of_tickers, start=initial_date, end=ending_date, group_by='ticker', interval=interval, repair=True, actions=True, session=session)

            final_dict: dict = {}
            for ticker in list_of_tickers: # Percorre a lista de tickers

                # Obtem os dados referente ao ticker, no formato dicionário
                temp_result = raw_data[ticker] if len(list_of_tickers) > 1 else raw_data
                temp_result.reset_index(inplace=True) # Nivela o index de todas as colunas do df
                selected_data = temp_result[['Dividends', 'Close']].values.tolist()
                
                accumulated_dividends = 0.0
                average_dividend = 0.0
                months = 0
                for data in selected_data:
                    try:
                        float(data[0])
                    except Exception as e:
                        print(f'Erro: {e}. Dados perdidos: {ticker}: data: {data[0]}, close: {data[1]}, dividends: {data[2]}')
                        continue
                    if not np.isnan(data[0]):
                        accumulated_dividends += data[0]
                        months += 1

                average_dividend = accumulated_dividends / months
                if period == 'yearly':
                    average_dividend = average_dividend * TWELVE_MONTHS
                
                temp_dict = {
                    'ticker': ticker[:-3],
                    'average_dividend': average_dividend,
                    'period': period,
                    'last_price': selected_data[-1][1] # Último item da lista é o último preço. Posição 0 do index é o dividendo. Posição 1 do index é o da cotação
                }

                final_dict[ticker[:-3]] = temp_dict
            return final_dict
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def calculate_average_dividend_of_tickers_list(self, list_of_tickers: list, initial_date: date, ending_date: date=None, interval='1d', period='monthly'):
        if ending_date is None: ending_date = date.today()
        list_of_tickers = [ticker.upper() + '.SA' for ticker in list_of_tickers]
        return self._calculate_average_dividend_data(list_of_tickers, initial_date, ending_date, interval, period=period)





    #############################################
    ###### GET AVERAGE DIVIDEND YIELD DATA ######
    #############################################

    def _get_average_dividend_data(self, list_of_tickers):
        try:
            raw_data = yf.Tickers(list_of_tickers, session=session)
            final_dict: dict = {}
            for ticker in list_of_tickers: # Percorre a lista de tickers 
                try:
                    average_dividend = float(raw_data.tickers[ticker].info['trailingAnnualDividendRate'])
                except:
                    average_dividend = 0.0
                temp_dict = {
                    'ticker': ticker[:-3],
                    'average_dividend': average_dividend,
                }
                final_dict[ticker[:-3]] = temp_dict
            return final_dict
        except Exception as e:
            class_ = self.__class__.__name__
            method_ = inspect.currentframe().f_code.co_name
            raise ValueError(f'Classe: {class_} => Método: {method_} => {e}')

    def get_average_dividend_of_tickers_list(self, list_of_tickers: list):
        list_of_tickers = [ticker.upper() + '.SA' for ticker in list_of_tickers]
        return self._get_average_dividend_data(list_of_tickers)