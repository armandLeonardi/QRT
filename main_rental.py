from Solver import Solver

class Main:

    def __init__(self, list_of_contract: list = []):
        self.__version__ = "1.0.0"
        self.list_of_contract = []
        self.solver = None

    def run(self):

        out = {}

        if self.list_of_contract != []:
            self.solver = Solver(list_of_contracts=self.list_of_contract)

            selected_contracts = self.solver.maximize_price()

            out = self.format_result(selected_contracts)

        else:

            out = {"empty list of contracts"}

        return out

    def format_result(self, selected_contracts: list):

        out = {"income": str(selected_contracts["price"].sum()), "path": list(selected_contracts["name"])}

        return out

if __name__ == '__main__':

    print("Main rental")
