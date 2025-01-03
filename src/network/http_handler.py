"""Module for handling HTTP communication with the game server."""

import os
from typing import Dict, Any
from src.network.http_client import HttpClient
from src.network.json_validator import JsonValidator


class HttpHandler:
    """Handler for HTTP communication with the game server.

    This class manages HTTP requests to the game server including starting new games
    and making moves.

    Attributes:
        base_url: Base URL of the game server
        http_client: Client for making HTTP requests
        validate: JSON schema validator
    """

    def __init__(self: "HttpHandler", server_ip: str, server_port: int) -> None:
        """Initialize the HttpHandler with server IP and port.

        Args:
            server_ip: The IP address of the game server
            server_port: The port number of the game server
        """
        self.base_url = f"http://{server_ip}:{server_port}"
        self.http_client = HttpClient(self.base_url)

        schema_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../util/schema.json")
        )
        self.validate = JsonValidator(schema_path)

    def send_json_via_post(
        self: "HttpHandler", json_data: Dict[str, Any]
    ) -> [Dict[str, Any]]:
        """Send the given JSON data via a POST request.

        Args:
            json_data: The JSON data to send

        Returns:
            Dict[str, Any]: The server's response as JSON

        Raises:
            ValueError: If the JSON data is invalid
        """
        if not self.validate.validate(json_data):
            raise ValueError("Invalid JSON data.")
        return self.http_client.post("", json_data)

    def start_new_game(
        self: "HttpHandler", gameid: str, positions: int, colors: int
    ) -> int:
        """Start a new game with the given parameters.

        Args:
            gameid: The ID for the new game
            positions: Number of positions in the game
            colors: Number of available colors

        Returns:
            int: The assigned game ID from the server
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
        self: "HttpHandler",
        gameid: int,
        gamerid: str,
        positions: int,
        colors: int,
        value: str,
    ) -> str:
        """Make a move in an existing game.

        Args:
            gameid: The ID of the game
            gamerid: The ID of the player
            positions: Number of positions in the game
            colors: Number of available colors
            value: The move value

        Returns:
            str: The server's response
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
