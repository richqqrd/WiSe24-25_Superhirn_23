import logging
from typing import Optional

from src.Network.HttpHandler import HTTPHandler
from src.Network.INetworkService import INetworkService


class NetworkService(INetworkService):
    def __init__(self, server_ip: str, server_port: int):
        """
        Initialize the NetworkService with server IP and port.

        Args:
            server_ip (str): The IP address of the server.
            server_port (int): The port number of the server.
        """
        self.http_handler = HTTPHandler(server_ip, server_port)
        self.current_game_id: Optional[int] = None
        self.current_player_id: Optional[str] = None
        self.positions: int = 5
        self.colors: int = 8

    def start_game(self, player_id: str) -> bool:
        """
        Start a new game for the given player.

        Args:
            player_id (str): The ID of the player.

        Returns:
            bool: True if the game started successfully, False otherwise.
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

    def make_move(self, value: str) -> Optional[str]:
        """
        Make a move in the current game.

        Args:
            value (str): The move value.

        Returns:
            Optional[str]: The result of the move, or None if the move failed.

        Raises:
            ValueError: If there is no active game.
        """
        if not self.current_game_id or not self.current_player_id:
            raise ValueError("No active game")

        try:
            return self.http_handler.make_move(
                self.current_game_id,
                self.current_player_id,
                self.positions,
                self.colors,
                value,
            )
        except Exception as e:
            logging.error(f"Failed to make move: {e}")
            return None
