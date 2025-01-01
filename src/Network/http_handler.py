import os
from typing import Dict, Any
from src.Network.http_client import HttpClient
from src.Network.json_validator import JsonValidator


class HTTPHandler:
    def __init__(self, server_ip: str, server_port: int):
        """
        Initialize the HTTPHandler with server IP and port.
        """
        self.base_url = f"http://{server_ip}:{server_port}"
        self.http_client = HttpClient(self.base_url)

        schema_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../util/schema.json")
        )
        self.validate = JsonValidator(schema_path)

    def send_json_via_post(self, json_data: Dict[str, Any]) -> [Dict[str, Any]]:
        """
        Send the given JSON data via a POST request to the specified URL.
        """
        if not self.validate.validate(json_data):
            raise ValueError("Invalid JSON data.")
        return self.http_client.post("", json_data)

    def start_new_game(self, gameid: str, positions: int, colors: int) -> int:
        """
        Start a new game with the given game ID, positions, and colors.
        """
        json_data = {
            "gameid": 0,
            "gamerid": gameid,
            "positions": positions,
            "colors": colors,
            "value": "",
        }
        response = self.send_json_via_post(json_data)
        return response["gameid"]

    def make_move(
        self, gameid: int, gamerid: str, positions: int, colors: int, value: str
    ) -> str:
        """
        Make a move in the game with the given game ID,
        gamer ID, positions, colors, and value.
        """
        json_data = {
            "gameid": gameid,
            "gamerid": gamerid,
            "positions": positions,
            "colors": colors,
            "value": value,
        }
        response = self.send_json_via_post(json_data)
        return response["value"]
