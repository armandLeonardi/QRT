"""
This script is a part of small rental compagny simulation ask by QRT for application process.
This script allow to launch the web server from a console.
Set also parameters from given configuration.

Ael - 06FEB23
"""
from flask import Flask, request, jsonify
from ast import literal_eval
import subprocess
from argparse import ArgumentParser
from Core import Base64Engine
import json

app = Flask("qrt_rental_compagny_server")
config = {}
route = "/"

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--config", help="Configuration path use by Main.py" ,type=str, default="")
    parser.add_argument("--verbose", help="Display details if true. False otherwise.", action='store_true')
    parser.add_argument("--debug", help="Display more details if true. False otherwise.", action='store_true')
    parser.add_argument("--formated", help="Format displayed messges if true. False otherwise.", action='store_true')

    args = parser.parse_args()

    # set local variables from script inputs
    config_path = args.config.strip()
    verbose = args.verbose
    debug = args.debug
    formated = args.formated

    # open configuration (not try expcet are set, we consider an error at this point as an critical error.)
    with open(config_path, 'r', encoding="utf8") as f:
        config = json.load(f)
        f.close()

    route = config.get("route", "/")
    host = config.get("host", "127.0.0.1")
    port = config.get("port", 8080)

    # get inputs from request args
    def get_inputs() -> str:

        inputs = ""
        is_ok = True

        try:
            inputs = request.args["contracts"]    
        except Exception as error:
            inputs = r"{'error' : 'Key \'contracts\' is missing on your payload'}" # return an error message to user the contracts list is empty
            is_ok = False

        return literal_eval(inputs), is_ok


    @app.route(f"{route}", methods=["POST", "GET"])
    def optimize():

        result = {}
        raw_list_of_contracts, get_inputs_ok = get_inputs() # get inputs from url

        if get_inputs_ok is True:

            raw_list_of_contracts_b64 = Base64Engine.encode(raw_list_of_contracts) # encode the list of contract on base64

            # get target script and script config path from server configuration
            target_script = config.get("target_script")
            target_script_config = config.get("target_script_config")

            # launch as command the Main.py script with configuration and contracts list (base64 encoded) 
            subprocess_result = subprocess.check_output(f"python {target_script} --config {target_script_config} --contracts {raw_list_of_contracts_b64}")
            result = literal_eval(subprocess_result.decode('utf8')) # get the result

        else:
            result = raw_list_of_contracts

        return jsonify(result) # display the result to user as json format

    # launch the web server
    app.run(debug=True, host=host, port=port)
