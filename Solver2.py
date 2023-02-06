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

    def __init__(self, list_of_contracts: list, verbose: bool = False, debug: bool = False, formated: bool = False):
        """_summary_

        Args:
            list_of_contracts (list): list of contracts to optimize
            verbose (bool, optional): true if you want to display details. False otherwise. Defaults to False.
            debug (bool, optional): true if you want to display more details. Fale otherwise. Defaults to False.
            formated (bool, optional): true if you want a formated display message. Defaults to False.
        """

        super().__init__(verbose=verbose, debug=debug, formated=formated, cls=self.__class__.__name__)
        self.__version__ = "1.0.0"
        self.list_of_contracts = pd.DataFrame(list_of_contracts) # load the list of contracts as pandas Dataframe
        self.is_ended = False

    def _concat(self, A: pd.DataFrame, B: pd.DataFrame) -> pd.DataFrame:
        """Concatenate the two dataframe in inputs.
        Row concatenation.

        Args:
            A (pd.DataFrame): head dataframe
            B (pd.DataFrame): foot dataframe

        Returns:
            pd.DataFrame: concatenate pandas Dataframe
        """

        if B is not None:
            C = pd.concat([A, B])
        else:
            C = A
        return C

    def maximize_price(self) -> list:
        """Maximize algorithm. Main part of the project.

        Returns:
            list: of contract whoose optimize the income
        """

        self.debug("search for the most optimized contracts path")

        out_list = pd.DataFrame()

        # ge the closet contract
        current_contract = self.get_start_contract()

        out_list = self._concat(out_list, current_contract)

        while self.is_ended is False:

            self.debug(f"current contract {current_contract.to_json()}, remaining contracts {len(self.list_of_contracts)}")

            # remove selected contract
            self.drop_contracts(current_contract)

            # get next contract in order to maximize the price
            current_contract = self.get_next_contract(current_contract)

            # add the selected contract to the result
            out_list = self._concat(out_list, current_contract)

        return out_list

    def get_start_contract(self) -> pd.DataFrame:
        """Return the contract with the smallest start date.

        Returns:
            pd.DataFrame: a contract as Dataframe type.
        """

        sub_list = self.list_of_contracts[self.list_of_contracts['start'] == self.list_of_contracts['start'].min()]

        sub_list['ratio'] = sub_list['price'] / (sub_list['duration'] - sub_list['start'])
        first_contract = sub_list[sub_list['ratio'] == sub_list['ratio'].max()]

        return first_contract[['name', 'start', 'duration', 'price']]

    def drop_contracts(self, current_contract: pd.DataFrame):
        """Remove the contract in input of the list_of_contracts attribute.

        Args:
            current_contract (pd.DataFrame): contract to remove
        """

        current_time = current_contract['start'] + current_contract['duration']
        ended_contracts = self.list_of_contracts[self.list_of_contracts['start'] < current_time.values[0]]
        self.list_of_contracts = self.list_of_contracts.drop(ended_contracts.index)


    def get_next_contract(self, current_contract: pd.DataFrame) -> pd.DataFrame:
        """Select the next contract in the list_of_contract in order to maximize the income.

        Method:
        - set the current time (by extracting the duraction of current contract)
        - select the list of possible contracts by only selecting contract with a start date greater of egal of the current time
        - select the contract on this list with return the higher price
          Continue this selection while the next contracts list was emty

        Args:
            current_contract (pd.DataFrame): juste finished contract

        Returns:
            pd.DataFrame: next selected contract
        """

        next_contract = None

        #current_time = current_contract["start"] + current_contract["duration"]
        next_possible_contracts = self.list_of_contracts[self.list_of_contracts['start'] == self.list_of_contracts['start'].min()]

        self.debug(f"List of next possibles contracts {next_possible_contracts.to_json()}")

        if next_possible_contracts.empty is False:

            next_possible_contracts['ratio'] = next_possible_contracts['price'] / next_possible_contracts['duration']
            next_contract = next_possible_contracts[next_possible_contracts['ratio'] == next_possible_contracts['ratio'].max()]

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


    import pandas as pd

    df = pd.DataFrame(list_of_contracts)

    subdf = df[df['start'] == df['start'].min()]

    r = subdf['price'] / (subdf['duration'] - subdf['start'])
    idx = r.idxmax()
    subdf.iloc[idx]
