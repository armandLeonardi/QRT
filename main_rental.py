from Main import Main
from argparse import ArgumentParser
from Core import Base64Engine

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--config", help="Configuration path use by Main.py" ,type=str, default="")
    parser.add_argument("--contracts", help="List of contracts (in base64)", type=str, default="")
    parser.add_argument("--verbose", help="Display details if true. False otherwise.", type=bool,  action='store_true')
    parser.add_argument("--debug", help="Display more details if true. False otherwise.", type=bool,  action='store_true')
    parser.add_argument("--formated", help="Format displayed messges if true. False otherwise.", type=bool,  action='store_true')
    
    args = parser.parse_args()

    config = args.config.strip()
    contracts = Base64Engine.decode(args.contracts)
    verbose = args.verbose
    debug = args.debug
    formated = args.formated

    current_main = Main(path_config=config, verbose=verbose, debug=debug, formated=formated)

    result = current_main.run(list_of_contracts=contracts)

    print(result)
    exit(0)