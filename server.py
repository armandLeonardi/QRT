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
from datetime import datetime
import json
import os

app = Flask("qrt_rental_compagny_server")
config = {}
route = "/"


def save_inputs_as_json(inputs: dict) -> str:
    """Save as json file the contracts list.

    Args:
        inputs (dict): the list of dictionaries (list of contracts)

    Returns:
        str: the full path of the json
    """

    # we supose the temporary json file is the system current time
    now = datetime.now().strftime("%d%m%y%H%M%S")
    local_filename = f"{now}.json"
    with open(local_filename, 'w', encoding="utf8") as f:
        json.dump(inputs, f)
        f.close()

    return os.path.abspath(local_filename)  # return the absolute path depending of the current host


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--config", help="Configuration path use by Main.py", type=str, default="")
    parser.add_argument("--verbose", help="Display details if true. False otherwise.", action='store_true')
    parser.add_argument("--debug", help="Display more details if true. False otherwise.", action='store_true')
    parser.add_argument("--formated", help="Format displayed messges if true. False otherwise.", action='store_true')

    # parsing
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
            inputs = save_inputs_as_json(inputs)

        except Exception as error:
            inputs = literal_eval(r"{'error' : 'Key \'contracts\' is missing on your payload'}")  # return an error message to user the contracts list is empty
            is_ok = False

        return inputs, is_ok

    @app.route(f"{route}", methods=["POST", "GET"])
    def optimize():

        result = {}
        local_input_file, get_inputs_ok = get_inputs()  # get inputs from POST request

        if get_inputs_ok is True:

            # get target script and script config path from server configuration
            target_script = config.get("target_script")
            target_script_config = config.get("target_script_config")

            # launch as command the Main.py script with configuration and contracts list file name full path
            subprocess_result = subprocess.run(f"python {target_script} --config {target_script_config} --contracts {local_input_file}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            result = literal_eval(subprocess_result.stdout.decode('utf8'))  # get the result

            # remove the temporary file containing all files
            os.remove(local_input_file)

        else:
            result = local_input_file

        return jsonify(result)  # display the result to user as json format

    # launch the web server
    app.run(debug=True, host=host, port=port)
