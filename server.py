from flask import Flask, request, jsonify
from ast import literal_eval
import subprocess
from argparse import ArgumentParser
from Core import Base64Engine
import json

app = Flask("qrt_rental_compagny_server")
config = {}

def get_inputs() -> str:

    inputs = ""
    is_ok = True

    try:
        inputs = request.args["contracts"]    
    except Exception as error:
        inputs = r"{'error' : 'Key \'contracts\' is missing on your payload'}"
        is_ok = False

    return literal_eval(inputs), is_ok


@app.route("/spaceship/optimize", methods=["POST", "GET"])
def optimize():

    result = {}
    raw_list_of_contracts, get_inputs_ok = get_inputs()

    if get_inputs_ok is True:

        raw_list_of_contracts_b64 = Base64Engine.encode(raw_list_of_contracts)

        target_script = config.get("target_script")
        target_script_config = config.get("target_script_config")

        subprocess_result = subprocess.check_output(f"python {target_script} --config {target_script_config} --contracts {raw_list_of_contracts_b64}")
        result = literal_eval(subprocess_result.decode('utf8'))

    else:
        result = raw_list_of_contracts

    return jsonify(result)

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--config", help="Configuration path use by Main.py" ,type=str, default="")
    parser.add_argument("--verbose", help="Display details if true. False otherwise.", action='store_true')
    parser.add_argument("--debug", help="Display more details if true. False otherwise.", action='store_true')
    parser.add_argument("--formated", help="Format displayed messges if true. False otherwise.", action='store_true')
    parser.add_argument("--host", help="Host where run the applicaton", type=str, default="127.0.0.1")
    parser.add_argument("--port", help="Listening port", type=int, default=8080)

    args = parser.parse_args()

    config_path = args.config.strip()
    host = args.host.strip()
    port = args.port
    verbose = args.verbose
    debug = args.debug
    formated = args.formated

    with open(config_path, 'r', encoding="utf8") as f:
        config = json.load(f)
        f.close()

    app.run(debug=True, host="127.0.0.1", port=8080)