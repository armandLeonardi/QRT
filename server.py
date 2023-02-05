from flask import Flask, request, jsonify
from main_rental import Main
from ast import literal_eval

app = Flask("qrt_rental_compagny_server")
main = Main()

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

        main.list_of_contract = raw_list_of_contracts

        result = main.run()

    else:
        result = raw_list_of_contracts

    return jsonify(result)


if __name__ == "__main__":

    app.run(debug=True, host="127.0.0.1", port=8080)