"""network service module for handling game server communication."""

import logging
from typing import Optional

from src.network.http_handler import HttpHandler
from src.network.i_network_service import INetworkService


class NetworkService(INetworkService):
    """Handles network communication for online gameplay.

    This class manages the connection to the game server and handles
    game-related network operations like starting games and making moves.

    Attributes:
        http_handler: Handler for HTTP requests to the server
        current_game_id: ID of the current game session
        current_player_id: ID of the current player
        positions: Number of positions in the game
        colors: Number of colors available in the game
    """

    def __init__(self: "NetworkService", server_ip: str, server_port: int) -> None:
        """Initialize the NetworkService with server connection details.

        Args:
            server_ip: The IP address of the game server
            server_port: The port number of the game server
        """
        self.http_handler = HttpHandler(server_ip, server_port)
        self.current_game_id: Optional[int] = None
        self.current_player_id: Optional[str] = None
        self.positions: int = 0
        self.colors: int = 0

    def configure(self: "NetworkService", positions: int, colors: int) -> None:
        """Configure game parameters.

        Args:
            positions: Number of positions in the code
            colors: Number of available colors
        """
        self.positions = positions
        self.colors = colors

    def start_game(self: "NetworkService", player_id: str) -> bool:
        """Start a new game for the given player.

        Args:
            player_id: The ID of the player

        Returns:
            bool: True if game started successfully, False otherwise
        """
        try:
            self.current_player_id = player_id
            self.current_game_id = self.http_handler.start_new_game(
                player_id, self.positions, self.colors
            )
            return True
        except Exception as e:
            logging.error(f"Failed to start game: {e}")
            return False

    def make_move(self: "NetworkService", value: str) -> Optional[str]:
        """Make a move in the current game.

        Args:
            value: The move value

        Returns:
            Optional[str]: The result of the move, or None if failed

        Raises:
            ValueError: If there is no active game
        """
        if not self.current_game_id or not self.current_player_id:
            raise ValueError("No active game")

        try:
            response = self.http_handler.make_move(  # Speichere Response in Variable
                self.current_game_id,
                self.current_player_id,
                self.positions,
                self.colors,
                value,
            )
            if isinstance(response, dict) and "error" in response:
                logging.error(f"Network error: {response['error']}")
                return f"error:{response['error']}"
            return response  # Return am Ende
        except Exception as e:
            logging.error(f"Failed to make move: {e}")
            return "error:unexpected_error"
