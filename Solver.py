
class Solver:

    def __init__(self, list_of_contracts):
        self.__version__ = "1.0.0"
        self.list_of_contracts = pd.DataFrame(list_of_contracts)

    def maximize(list_of_contracts: list) -> list:

        out_list = []


    def get_start_contract(self):
        return self.list_of_contracts[list_of_contracts['start'] == list_of_contracts['start'].min()]

    def drop_contract(self, current_contract):

        current_contract_index = current_contract.index[0]
        self.list_of_contracts = self.list_of_contracts.drop(current_contract_index)


    def get_next_contract(self, current_contract):

        next_start = current_contract["duration"].values[0]
        next_possible_contracts = self.list_of_contracts[self.list_of_contracts['start'] >= next_start]

        next_contract = next_possible_contracts[next_possible_contracts['price'] == next_possible_contracts['price'].max()]
        
        return next_contract

list_of_contracts = [
{"name": "Contract1", "start": 0, "duration": 5, "price": 10},
{"name": "Contract2", "start": 3, "duration": 7, "price": 14},
{"name": "Contract3", "start": 5, "duration": 9, "price": 8},
{"name": "Contract4", "start": 5, "duration": 9, "price": 7}
]






current = min(list_of_contracts, key=lambda x:  x['start'])

list_of_contracts.index(current)
list_of_contracts.pop(0)

next_start = current["duration"]

min(list_of_contracts, key=lambda x:  x['start'] > next_start)


import pandas as pd

df = pd.DataFrame(list_of_contracts)

current = df[df['start'] == df['start'].min()]

current.index.values

next_start = current["duration"].values[0]

df = df.drop(index=0)

sub_df = df[df['start'] >= next_start] 

sub_df[sub_df['price'] == sub_df['price'].max()]

