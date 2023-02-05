import pandas as pd

class Solver:

    def __init__(self, list_of_contracts):
        self.__version__ = "1.0.0"
        self.list_of_contracts = pd.DataFrame(list_of_contracts)
        self.is_ended = False

    def maximize_price(self) -> list:

        out_list = []

        current_contract = self.get_start_contract()

        out_list.append(current_contract)

        while self.is_ended is False:

            self.drop_contract(current_contract)

            current_contract = self.get_next_contract(current_contract)

            if current_contract is not None:
                out_list.append(current_contract)

        return out_list

    def get_start_contract(self):
        return self.list_of_contracts[self.list_of_contracts['start'] == self.list_of_contracts['start'].min()]

    def drop_contract(self, current_contract):

        current_contract_index = current_contract.index[0]
        self.list_of_contracts = self.list_of_contracts.drop(current_contract_index)


    def get_next_contract(self, current_contract):

        next_contract = None

        next_start = current_contract["duration"].values[0]
        next_possible_contracts = self.list_of_contracts[self.list_of_contracts['start'] >= next_start]

        if next_possible_contracts.empty is False:

            next_contract = next_possible_contracts[next_possible_contracts['price'] == next_possible_contracts['price'].max()]

        else:

            self.is_ended = True

        return next_contract

if __name__ == "__main__":

    list_of_contracts = [
    {"name": "Contract1", "start": 0, "duration": 5, "price": 10},
    {"name": "Contract2", "start": 3, "duration": 7, "price": 14},
    {"name": "Contract3", "start": 5, "duration": 9, "price": 8},
    {"name": "Contract4", "start": 5, "duration": 9, "price": 7}
    ]


    S = Solver(list_of_contracts=list_of_contracts)

    result = S.maximize_price()

    print(result)
