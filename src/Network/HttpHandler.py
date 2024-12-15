import json
import os
import logging
import requests
import jsonschema
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate


class HTTPHandler:
    def __init__(self, server_ip, server_port):
        """
        Initialize the HTTPHandler with server IP and port.
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.base_url = f'http://{self.server_ip}:{self.server_port}'
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'util', 'schema.json')
        self.schema = self.load_schema(schema_path)

    def load_schema(self, schema_path):
        """
        Load the JSON schema from the given file path.
        """
        with open(schema_path) as file:
            schema = json.load(file)
            return schema

    def validate_json(self, data):
        """
        Validate the given JSON data against the loaded schema.
        """
        try:
            validate(instance=data, schema=self.schema)
            logging.info("JSON validation successful.")
            return True
        except ValidationError as err:
            logging.error(f"Validation error: {err.message}")
            logging.error(f"Validation details: {err}")
            return false

    def send_json_via_post(self, url, json_data):
        """
        Send the given JSON data via a POST request to the specified URL.
        """
        if not self.validate_json(json_data):
            logging.error("Invalid JSON data. Aborting POST request.")
            return None

        url = f"{self.base_url}"
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(url, headers=headers, json=json_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err}")
            raise
        except requests.exceptions.RequestException as err:
            logging.error(f"Request error occurred: {err}")
            raise

    def start_new_game(self, gamerid, positions, colors):
        """
        Start a new game with the given gamer ID, positions, and colors.
        """
        json_data = {
            "gameid": 0,
            "gamerid": gamerid,
            "positions": positions,
            "colors": colors,
            "value": ""
        }
        return self.send_json_via_post(self.base_url, json_data)

    def make_move(self, gameid, gamerid, positions, colors, value):
        """
        Make a move in the game with the given game ID, gamer ID, positions, colors, and value.
        """
        json_data = {
            "gameid": gameid,
            "gamerid": gamerid,
            "positions": positions,
            "colors": colors,
            "value": value
        }
        return self.send_json_via_post(self.base_url, json_data)