"""Module for managing game state."""

from typing import List
from src.game_logic.game_turn import GameTurn
from src.game_logic.guesser.i_guesser import IGuesser
from src.util.color_code import ColorCode


class GameState:
    """Represents the state of the game.

    This class maintains the current state of a game including secret code,
    game turns, and configuration settings.

    Attributes:
        secret_code: The secret code that needs to be guessed
        turns: The list of turns taken in the game
        max_rounds: The maximum number of rounds allowed
        current_guesser: The current guesser (player or computer)
        positions: Number of positions in the code
        colors: Number of available colors
        player_name: Name of the player
    """

    def __init__(
        self: "GameState",
        secret_code: List[ColorCode],
        max_rounds: int,
        positions: int,
        colors: int,
        player_name: str,
        current_guesser: IGuesser = None,
    ) -> None:
        """Initialize the game state.

        Args:
            secret_code: The secret code that needs to be guessed
            max_rounds: The maximum number of rounds allowed
            positions: Number of positions in the code
            colors: Number of available colors
            player_name: Name of the player
            current_guesser: The current guesser (player or computer)
        """
        self.secret_code: List[ColorCode] = secret_code
        self.turns: List[GameTurn] = []
        self.max_rounds = max_rounds
        self.current_guesser = current_guesser
        self.positions = positions
        self.colors = colors
        self.player_name = player_name

    def add_turn(self: "GameState", turn: GameTurn) -> None:
        """Add a turn to the game state.

        Args:
            turn: The turn to be added

        Raises:
            ValueError: If the maximum number of turns is reached
        """
        if len(self.turns) >= self.max_rounds:
            raise ValueError("Max number of turns reached")
        if len(turn.guesses) != self.positions:
            raise ValueError(f"Guess must have {self.positions} positions")
        self.turns.append(turn)

    def get_secret_code(self: "GameState") -> List[ColorCode]:
        """
        Returns the secret code.

        Returns:
            List[ColorCode]: The secret code.
        """
        return self.secret_code

    def get_turns(self: "GameState") -> List[GameTurn]:
        """Get all turns taken in the game.

        Returns:
            List of all game turns
        """
        return self.turns

    def __repr__(self: "GameState"):
        """Return string representation of the GameState.

        This method provides a detailed string representation of the game state
        including secret code, turns, and max rounds for debugging and development.

        Returns:
            str: String representation in format
                'GameState(secret_code=X, turns=Y, max_rounds=Z)'
        """
        return (
            f"GameState(secret_code={self.secret_code}, "
            f"turns={self.turns}, max_rounds={self.max_rounds})"
        )
