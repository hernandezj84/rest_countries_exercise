"""Rest api server that returns information about the borders of a given country"""
from flask import Flask, jsonify, make_response
import requests

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

NOT_FOUND_STATUS = 404
OK_STATUS = 200
COUNTRY_NAME_URL = "https://restcountries.eu/rest/v2/name/{}"
COUNTRY_CODE_URL = "https://restcountries.eu/rest/v2/alpha/{}"
POPULATION_BASE = 5000000


def json_response_map(attribute, json_response):
    """Returns the value of the restcountries.eu responses

    Args:
        attribute (str): Value that wants to be found
        json_response (dict): Map of the restcountries.eu responses

    Returns:
        str: The value of the the json_response keys
    """
    currency_code = ""
    response_dict = {}
    if 'population' in json_response:
        if json_response["population"] > POPULATION_BASE:
            currency_code = caesar_cipher(
                json_response["currencies"][0]["code"], 1)
        else:
            currency_code = json_response["currencies"][0]["code"]

        response_dict = {
            "borders_object": {
                "name": json_response["name"],
                "capital": json_response["capital"],
                "currency_code": currency_code
            }
        }
    else:
        response_dict = {
            "country_name": json_response[0]["name"],
            "borders": json_response[0]["borders"],

        }

    return response_dict[attribute]


def get_request(url):
    """Makes a http [GET] request to a server

    Args:
        url (str): Url involved in the request

    Returns:
        Response: Response object with the request status and the json data
    """
    request = requests.get(url)
    return request


def caesar_cipher(text, shift):
    """Creates the Caesar cipher ciphered of the given text and shift positions

    Args:
        text (str): Text that is going to be ciphered
        shift (int): Number of shifting spaces over letters

    Returns:
        str: The caesar ciphered text
    """
    ciphered_text = ""
    for index, _ in enumerate(text):
        char = text[index]
        ciphered_text += chr((ord(char) + shift - 65) % 26 + 65)

    return ciphered_text


@app.route("/name/<country_name>")
def get_borders_of_country(country_name):
    """Exposes a http [GET] method that finds the borders of a given country

    Args:
        country_name (str): Name of the country which borders has to be found

    Returns:
        make_response: Function that handles the response json object
        and the status of the [GET] request
    """
    status = NOT_FOUND_STATUS
    response_data = {"status": status, "message": "Not Found"}
    request = get_request(COUNTRY_NAME_URL.format(country_name))
    if request.status_code == OK_STATUS:
        json_response = request.json()
        country_name = json_response_map("country_name", json_response)
        borders = []
        for border in json_response_map("borders", json_response):
            border_request = get_request(COUNTRY_CODE_URL.format(border))
            if border_request.status_code == OK_STATUS:
                border_json_response = border_request.json()
                borders.append(json_response_map(
                    "borders_object", border_json_response))

        response_data = {
            "name": country_name,
            "borders": borders
        }
        status = OK_STATUS

    return make_response(jsonify(response_data), status)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
