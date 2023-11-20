import pandas as pd
import datetime

from .DataFromYFinance import DataFromYFinance

class TransactionsFromFile(DataFromYFinance):
        
    #########################################################
    #### LOADS EXCEL FILE, PROCESS DATA ADDING THE       ####
    #### SPLITS/GROUPMENTS TRANSACTIONS. RETURNS A       ####
    #### PORTIFOLIO LIST AND A TRANSACTIONS LIST.        ####
    #########################################################

    def load_file(self, file):
        df = pd.read_excel(file)
        columns = []
        for i in range(len(df.columns)):
            columns.append(df.columns[i].title().lower())

        initial_list = []
        for index, row in df.iterrows():
            temp_dict = {
                column: row[column] for column in columns
            }
            initial_list.append(temp_dict)
        
        if initial_list:
            return initial_list
        else:
            raise ValueError('Nenhum dado foi lido. Planilha vazia?')

    def _validate_trasactions_data(self, data_list):
        for i, data in enumerate(data_list):
            
            # Valida a coluna "Data"
            try:
                data['date'] = data['date'].date() # Converte timestamp em objeto datetime
            except:
                raise ValueError('Dados corrompidos na coluna "Data". Verifique se há valores inválidos de data.')
            
            # Valida a coluna "Ticker"
            try:
                data['ticker'] = data['ticker'].upper() # Tickers em letras maiúsculas
            except:
                raise ValueError(f'Dados corrompidos na coluna "Ticker", Linha {i+2}: {data["ticker"]}.')
                

            # Valida a coluna "Operações"
            try:
                data['operation'] = data['operation'].upper()
                if data['operation'] not in ['C', 'V', 'A']:
                    raise ValueError(f'Dados corrompidos na coluna "Operações", Linha {i+2}: {data["operation"]} não é uma operação aceita. (Use "C", "V" ou "A")')
            except Exception as e:
                raise ValueError(e) from e
            
            # Valida a coluna "Quantidade"
            try:
                if not isinstance(data['quantity'], int) or int(data['quantity']) < 0:
                    raise ValueError(f'Dados corrompidos na coluna "Quantidade", Linha {i+2}: {data["quantity"]}. Os valores de quantidade devem ser do tipo inteiro e maiores ou iguais a 0.')
            except Exception as e:
                raise ValueError(e) from e
            
            # Valida a coluna "Valor Unitário"
            try:
                data['unit_price'] = round(float(data['unit_price']), 2)
                if data['unit_price'] <= 0:
                    raise ValueError(f'Dados corrompidos na coluna "Valor Unitário", Linha {i+2}: {data["unit_price"]}. Os valores devem ser do tipo flutuante e maiores que 0,00.')
            except:
                raise ValueError(f'Dados corrompidos na coluna "Valor Unitário", Linha {i+2}: {data["unit_price"]}. Os valores devem ser do tipo flutuante e maiores que 0,00.')
            
            # Valida a coluna "Tipo"
            try:
                data['sort_of'] = data['sort_of'].upper()
                if data['sort_of'] not in ['AÇÕES', 'FIIS', 'SPLIT/AGRUP']:
                    raise ValueError(f'Dados corrompidos na coluna "Tipo", Linha {i+2}: {data["sort_of"]}.')
            except Exception as e:
                raise ValueError(e) from e

        return data_list

    def extract_tickers_list(self, transactions_list):
        tickers_set = {transaction['ticker'] for transaction in transactions_list}
        return tickers_set

    def _add_splits_transactions(self, transactions_list, tickers_list, existing_events_list):
        try:
            transactions_list_added_splits_bonus = transactions_list
            for ticker in tickers_list:
                print(f'Analizing {ticker}')
                
                splits_bonus = self.load_splits_groupments(ticker)
                
                # Filtra os dados de transação do ticker:
                transactions_of_ticker = [transaction for transaction in transactions_list if transaction['ticker'] == ticker]
                
                # Captura a operação mais antiga
                first_transaction = min(transactions_of_ticker, key=lambda x: x['date'])

                # Verifica erro no ticker:
                if not isinstance(splits_bonus, list):
                    raise Exception('Ticker inválido ou não listado!')

                # Se houver dados de splits:
                if splits_bonus:
                    for split_bonus in splits_bonus:
                        
                        # Verifica se a transação já existe:
                        event_exists = False
                        for event in existing_events_list:
                            if (event['date'] == split_bonus['date'] and
                                event['ticker'] == split_bonus['ticker'] and
                                event['unit_price'] == split_bonus['ratio'] and
                                event['operation'] == 'A'
                            ):
                                event_exists = True
                                break
                        
                        # Se a transação já existe, não cadastra e pula para o próximo evento:
                        if event_exists:
                            print(f'Evento já cadastrado: {split_bonus}')
                            continue

                        # Se a data da primeira transação no ativo for mais velha que a data do split:
                        if split_bonus['date'] > first_transaction['date']:
                            transactions_list_added_splits_bonus.append(
                                {
                                    'date': split_bonus['date'],
                                    'ticker': ticker,
                                    'operation': 'A',
                                    'quantity': 0,
                                    'unit_price': split_bonus['ratio'],
                                    'sort_of': 'SPLIT/AGRUP',
                                }
                            )
                            print(f'{ticker} splits/groupments added')
                
                
                        
            return transactions_list_added_splits_bonus
        except Exception as e:
            print(f'Erro ao adicionar as transações de splits/agrupamentos: {e}')
            raise Exception(e)
    
    def calculate_portfolio_balance_and_asset_history(self, transactions_list, tickers_list):
        
        # Inicialize o portfólio com todos os tickers e valores iniciais para serem rastreados
        portfolio = {
            ticker: {'ticker': ticker, 'quantity': 0, 'average_price': 0.0, 'sort_of': ''} for ticker in tickers_list
        }

        asset_history = {
            ticker: [] for ticker in tickers_list
        }

        for transaction in transactions_list:
            ticker = transaction['ticker']
            portfolio[ticker]['sort_of'] = transaction['sort_of']
            operation = transaction['operation']
            quantity = transaction['quantity']
            unit_price = transaction['unit_price']

            if operation == 'C':
                # Compra: atualiza a quantidade e o preço médio
                portfolio[ticker]['quantity'] += quantity
                portfolio[ticker]['average_price'] = (
                    portfolio[ticker]['average_price'] * (portfolio[ticker]['quantity'] - quantity) +
                    unit_price * quantity
                ) / portfolio[ticker]['quantity']

            elif operation == 'V':
                # Venda: atualiza a quantidade
                portfolio[ticker]['quantity'] -= quantity

            elif operation == 'A':
                # Ação: multiplique a quantidade pelo fator de split/agrupamento/bonificação
                portfolio[ticker]['quantity'] = int(portfolio[ticker]['quantity'] * unit_price) # Neste caso a variavel unit_price recebe o 'ratio'
                portfolio[ticker]['average_price'] = portfolio[ticker]['average_price'] / unit_price

            # Cria um histórico de quantidade e preço médio de ativos ao longo das datas das operações referente ao ativo:
            """ Por exemplo: na data 01/mm/YYYY havia x quantidade com y preço médio
                             na data 10/mm/YYYY havia z quantidade com t preço médio"""
            temp_dict = {
                'ticker': ticker,
                'date': transaction['date'],
                'quantity': portfolio[ticker]['quantity'],
                'average_price': portfolio[ticker]['average_price'],
            }
            asset_history[ticker].append(temp_dict)
        
        return portfolio, asset_history

    def process_raw_transactions(self, raw_transactions, existing_events_list=[]) -> list:
        print('Processing...')
        print()

        try:
            print('Validating data...')
            transactions_list = self._validate_trasactions_data(raw_transactions)
            print()
            
            print('Extracting tickers list...')
            tickers_list = self.extract_tickers_list(transactions_list)
            print()

            print('Adding splits/groupments transactions...')
            transactions_list = self._add_splits_transactions(transactions_list, tickers_list, existing_events_list)
            print()
            
            print('Sorting by date, ticker and operation...')
            transactions_list = self.list_of_dicts_order_by(list_of_dicts=transactions_list, sort_keys=['date', 'ticker', 'operation'], reversed_output=False)
            print()

            print('Done')
            return transactions_list
        except Exception as e:
            return e


    ##############################
    ## Carrega dados de Aportes ##
    ##############################

    def _validate_contributions_data(self, fulldata):
        for i, data in enumerate(fulldata):
            try:
                data['date'] = data['date'].to_pydatetime().date()
            except:
                raise ValueError('Dados corrompidos na coluna "date". Verifique se há valores inválidos de data.')
            
            try:
                data['value'] = float(data['value'])
            except:
                raise ValueError(f'Dados corrompidos na coluna "value", linha {i+2}: {data["value"]}')
        
        return fulldata

    def load_contributions_from_excel(self, file):
        fulldata = self.load_file(file)
        validated_data = self._validate_contributions_data(fulldata)
        return self.list_of_dicts_order_by(list_of_dicts=validated_data, sort_keys=['date'])
