from abc import ABC, abstractmethod
from typing import Optional

class INetworkService(ABC):
    """Interface for network service layer"""
    
    @abstractmethod
    def start_game(self, player_id: str) -> bool:
        """Start a new network game.
        
        Args:
            player_id (str): The ID of the player.

        Returns:
            bool: True if game started successfully, False otherwise.
        """
        pass

    @abstractmethod
    def make_move(self, value: str) -> Optional[str]:
        """Make a move in the current network game.
        
        Args:
            value (str): The move value.

        Returns:
            Optional[str]: The result of the move, or None if failed.
            
        Raises:
            ValueError: If there is no active game.
        """
        pass