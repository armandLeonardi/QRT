"""
This script is a part of small rental compagny simulation ask by QRT for application process.
This script allow to launch the Main.py script from a console.

Ael - 06FEB23
"""

from Main import Main
from argparse import ArgumentParser # parse the inputs arguements
from Core import Base64Engine
from ast import literal_eval
import json

def open_contracts_file(contracts_file_path: str) -> dict:
    """Load the contracts json file.

    Args:
        contracts_file_path (str): full path of json file

    Returns:
        dict: list of contracts as dictionary
    """
    data = []

    # no try/except is set here we consider ans error at this point as critical
    with open(contracts_file_path, 'r', encoding="utf8") as f:
        data = json.load(f)
        f.close()
    
    return literal_eval(data)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--config", help="Configuration path use by Main.py" ,type=str, default="")
    parser.add_argument("--contracts", help="List of contracts (in base64)", type=str, default="")
    parser.add_argument("--verbose", help="Display details if true. False otherwise.", action='store_true')
    parser.add_argument("--debug", help="Display more details if true. False otherwise.", action='store_true')
    parser.add_argument("--formated", help="Format displayed messges if true. False otherwise.", action='store_true')
    
    args = parser.parse_args()

    # set arguments to local variables
    config = args.config.strip()
    contracts = args.contracts.strip() # path of contracts json file
    verbose = args.verbose
    debug = args.debug
    formated = args.formated

    # instance the Main object
    current_main = Main(path_config=config, verbose=verbose, debug=debug, formated=formated)

    # load the configuration
    current_main.load_config()

    # open the log file
    current_main.open_log_file()

    # load the json file given in inputs
    contracts = open_contracts_file(contracts_file_path=contracts)

    # launch the main method (optimize the contracts path)
    result = current_main.run(list_of_contracts=contracts)

    # close current log file
    current_main.close_log()

    # return on standard output the optimized result
    print(result)
    exit(0)