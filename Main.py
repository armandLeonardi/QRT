from Solver import Solver
from Core import Core

class Main(Core):

    def __init__(self, path_config: str = "", verbose: bool = False, debug: bool = False, formated: bool = False):
        super().__init__(path_config=path_config, verbose=verbose, debug=debug, formated=formated, cls=self.__class__.__name__)
        self.__version__ = "1.0.0"
        self.solver = None

    def run(self, list_of_contracts: list = []):

        self.info("launch run method")

        out = {}

        if list_of_contracts != []:

            self.info(f"nb of contracts {len(list_of_contracts)}")

            self.solver = Solver(list_of_contracts=list_of_contracts, verbose=self._verbose, debug=self._debug, formated=self.formated)
            self.solver.set_logger(self)

            selected_contracts = self.solver.maximize_price()

            out = self.format_result(selected_contracts)

            self.info(f"result: {out}")

        else:

            self.warning("empty list of contracts")
            out = {"empty list of contracts"}

        return out

    def format_result(self, selected_contracts: list):

        out = {"income": str(selected_contracts["price"].sum()), "path": list(selected_contracts["name"])}

        return out
