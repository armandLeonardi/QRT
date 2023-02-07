"""
This script is a part of small rental compagny simulation ask by QRT for application process.
This script containt classes:
    - Main (Core heritate): work on contracts list given, call a Solver and return a correct formated result.

Ael - 06FEB23
"""
from Solver import Solver
from Core import Core


class Main(Core):
    """Python class interface between main_rental script and Solver.
    Manage bad contracts list formating and format income/path result.

    Args:
        Core (class): heritate class.
    """

    def __init__(self, path_config: str = "", verbose: bool = False, debug: bool = False, formated: bool = False) -> None:
        """Main constructor.

        Args:
            path_config (str, optional): configuration path. Defaults to "".
            verbose (bool, optional): true if you want to display details. False otherwise. Defaults to False.
            debug (bool, optional): true if you want to display more details. Fale otherwise. Defaults to False.
            formated (bool, optional): true if you want a formated display message. Defaults to False.
        """
        super().__init__(path_config=path_config, verbose=verbose, debug=debug, formated=formated, cls=self.__class__.__name__)
        self.__version__ = "1.0.0"
        self.solver = None
        self.windows = -1

    def run(self, list_of_contracts: list = []) -> dict:
        """Main method of Main class.
        Instance a Solver and try to maximize the income.

        Args:
            list_of_contracts (list, optional): list of dictionaries contening contracts. Defaults to [].

        Returns:
            dict: the result as asked format
        """

        self.info("launch run method")  # do not forget, this line display and write on a log the input message

        out = {}

        # if list of contract was not empty
        if list_of_contracts != []:

            self.info(f"nb of contracts {len(list_of_contracts)}")

            # instance the solver
            self.solver = Solver(list_of_contracts=list_of_contracts, windows=self.windows, verbose=self._verbose, debug=self._debug, formated=self.formated)
            self.solver.set_logger(self)  # set the current openend logger to Solver child object. See xxxx.set_logger documentation.

            self.solver.maximize_price()  # call the main method of the solver and get result

            out = self.solver.result

            self.info(f"result: {out}")

        else:

            self.warning("empty list of contracts")
            out = {"empty list of contracts"}

        return out

    def format_result(self, selected_contracts: list) -> dict:
        """Format selected list of contracts as asked format.

        Args:
            selected_contracts (list): selected contracts was maximizing the income

        Returns:
            dict: a dict like {"income": xxx, "path": [xxx, yyy, ...]}
        """
        out = {"income": str(selected_contracts["price"].sum()), "path": list(selected_contracts["name"])}

        return out
