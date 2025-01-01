"""Interface module for network service layer."""

from abc import ABC, abstractmethod
from typing import Optional


class INetworkService(ABC):
    """Interface for network service layer.
    
    This interface defines the contract for network communication 
    used in online gameplay.

    Provides methods for:
        - Starting network games
        - Making moves in network games
    """

    @abstractmethod
    def start_game(self: "INetworkService", player_id: str) -> bool:
        """Start a new network game.

        Args:
            player_id: The ID of the player

        Returns:
            bool: True if game started successfully, False otherwise
        """
        pass

    @abstractmethod
    def make_move(self: "INetworkService", value: str) -> Optional[str]:
        """Make a move in the current network game.

        Args:
            value: The move value

        Returns:
            Optional[str]: The result of the move, or None if failed

        Raises:
            ValueError: If there is no active game
        """
        pass
