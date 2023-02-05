import pandas as pd
from Core import Core

class Solver(Core):

    def __init__(self, list_of_contracts, verbose: bool = False, debug: bool = False, formated: bool = False):
        super().__init__(verbose=verbose, debug=debug, formated=formated, cls=self.__class__.__name__)
        self.__version__ = "1.0.0"
        self.list_of_contracts = pd.DataFrame(list_of_contracts)
        self.is_ended = False

    def _concat(self, A: pd.DataFrame, B: pd.DataFrame):

        if B is not None:
            C = pd.concat([A, B])
        else:
            C = A
        return C

    def maximize_price(self) -> list:

        self.debug("search for the most optimized contracts path")

        out_list = pd.DataFrame()

        current_contract = self.get_start_contract()

        out_list = self._concat(out_list, current_contract)

        while self.is_ended is False:

            self.debug(f"current contract {current_contract.to_json()}, remaining contracts {len(self.list_of_contracts)}")

            self.drop_contract(current_contract)

            current_contract = self.get_next_contract(current_contract)

            out_list = self._concat(out_list, current_contract)

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

        self.debug(f"List of next possibles contracts {next_possible_contracts.to_json()}")

        if next_possible_contracts.empty is False:

            next_contract = next_possible_contracts[next_possible_contracts['price'] == next_possible_contracts['price'].max()]

            self.debug(f"Selected next contract {next_contract.to_json()}")

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

    S = Solver(list_of_contracts=list_of_contracts, debug=True, verbose=True, formated=True)

    result = S.maximize_price()

    print(result)
