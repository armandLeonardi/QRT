"""
This script is a part of small rental compagny simulation ask by QRT for application process.
This script containt classes:
    - Solver (heritate of Core): containt the optimization algorithm

You can check on the '__main__' part to see how to use thoose classes
Ael - 06FEB23
"""

import pandas as pd
from Core import Core
import warnings
warnings.filterwarnings('ignore')


class Solver(Core):

    def __init__(self, list_of_contracts: list, windows: int, verbose: bool = False, debug: bool = False, formated: bool = False):
        """_summary_

        Args:
            list_of_contracts (list): list of contracts to optimize
            windows (int): the considered time windows of contracts
            verbose (bool, optional): true if you want to display details. False otherwise. Defaults to False.
            debug (bool, optional): true if you want to display more details. Fale otherwise. Defaults to False.
            formated (bool, optional): true if you want a formated display message. Defaults to False.
        """

        super().__init__(verbose=verbose, debug=debug, formated=formated, cls=self.__class__.__name__)
        self.__version__ = "1.0.0"
        self.list_of_contracts = pd.DataFrame(list_of_contracts) # load the list of contracts as pandas Dataframe
        self.is_ended = False
        self.result = {"income": 0, "path": []}
        self.start = -1
        self.duration = -1
        self.windows = windows

    def maximize_price(self) -> list:
        """Maximize algorithm. Main part of the project.

        Returns:
            list: of contract whoose optimize the income
        """

        self.debug("search for the most optimized contracts path")

        while self.is_ended is False:

            # get next contract in order to maximize the price
            self.get_next_contract()

            # remove selected contract
            self.drop_contracts()

    def update_result(self, contract: pd.DataFrame) -> None:

        self.result["income"] += contract["price"].values[0]
        self.result["path"].append(contract["name"].values[0])

    def drop_contracts(self) -> None:
        """Remove contracts which are too old to be accepted.
        And then became useless.
        """

        current_time = self.start + self.duration
        ended_contracts = self.list_of_contracts[self.list_of_contracts['start'] < current_time.values[0]]
        self.list_of_contracts = self.list_of_contracts.drop(ended_contracts.index)


    def get_next_contract(self):
        """Select the next contract in the list_of_contract in order to maximize the income.
            Add it name and price to result attribute.

        Method:
        - select the list of possible contracts on given windows.
        - select the contract on this list with return the higher price
          Continue this selection while the next contracts list was emty
        """

        next_contract = None

        # made a selection of possible contract with a given windows
        next_possible_contracts = self.list_of_contracts[self.list_of_contracts['start'] <= self.list_of_contracts['start'].min() + self.windows]

        self.debug(f"List of next possibles contracts {next_possible_contracts.to_json()}")

        if next_possible_contracts.empty is False:

            # compute the profitable ratio price / duration ($/h for example)
            next_possible_contracts['ratio'] = next_possible_contracts['price'] / next_possible_contracts['duration']

            # select next contract with higher ratio
            next_contract = next_possible_contracts[next_possible_contracts['ratio'] == next_possible_contracts['ratio'].max()]

            # if there more than 1 contract with the equal higher ratio then select the closest
            if next_contract.shape[0] > 1:
                next_contract = next_contract[next_contract['start'] == next_contract['start'].min()]

            # extract contract name and inform user
            contract_name = next_contract["name"].values[0]
            self.info(f"current contract {contract_name}, remaining contracts {len(self.list_of_contracts)}")

            # update start and duration (in order to compute next current time)
            self.start = next_contract["start"]
            self.duration = next_contract["duration"]

            # update returned result
            self.update_result(next_contract)

        else:

            self.is_ended = True

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
