import logging
from typing import Optional

from src.Network.HttpHandler import HTTPHandler


class NetworkService:
    def __init__(self, server_ip: str, server_port: int):
        self.http_handler = HTTPHandler(server_ip, server_port)
        self.current_game_id: Optional[int] = None
        self.current_player_id: Optional[str] = None
        self.positions: int = 5
        self.colors: int = 8

    def start_game(self, player_id: str)-> bool:
        try:
            self.current_player_id = player_id
            self.current_game_id = self.http_handler.start_new_game(
                player_id,
                self.positions,
                self.colors
            )
            return True
        except Exception as e:
            logging.error(f"Failed to start game: {e}")
            return False

    def make_move(self, value: str)-> Optional[str]:
        if not self.current_game_id or not self.current_player_id:
            raise ValueError("No active game")

        try:
            return self.http_handler.make_move(
                self.current_game_id,
                self.current_player_id,
                self.positions,
                self.colors,
                value
            )
        except Exception as e:
            logging.error(f"Failed to make move: {e}")
            return None
