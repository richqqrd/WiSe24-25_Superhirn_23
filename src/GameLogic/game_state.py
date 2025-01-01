# src/util/game_state.py

from typing import List
from src.GameLogic.game_turn import GameTurn
from src.GameLogic.Guesser.i_guesser import IGuesser
from src.util.color_code import ColorCode


class GameState:
    """
    Represents the state of the game.

    Attributes:
        secret_code (List[ColorCode]): The secret code that needs to be guessed.
        turns (List[GameTurn]): The list of turns taken in the game.
        max_rounds (int): The maximum number of rounds allowed in the game.
    """

    def __init__(
        self,
        secret_code: List[ColorCode],
        max_rounds: int,
        positions: int,
        colors: int,
        player_name: str,
        current_guesser: IGuesser = None,
    ):
        """
        Initializes the GameState with a secret code and maximum rounds.

        Args:
            secret_code (List[ColorCode]): The secret code that needs to be guessed.
            max_rounds (int): The maximum number of rounds allowed in the game.
        """
        self.secret_code: List[ColorCode] = secret_code
        self.turns: List[GameTurn] = []  # Empty list of turns
        self.max_rounds = max_rounds
        self.current_guesser = current_guesser
        self.positions = positions
        self.colors = colors
        self.player_name = player_name

    def add_turn(self, turn: GameTurn) -> None:
        """
        Adds a turn to the game state.

        Args:
            turn (GameTurn): The turn to be added.

        Raises:
            ValueError: If the maximum number of turns is reached.
        """
        if len(self.turns) >= self.max_rounds:
            raise ValueError("Max number of turns reached")
        if len(turn.guesses) != self.positions:
            raise ValueError(f"Guess must have {self.positions} positions")
        self.turns.append(turn)

    def get_secret_code(self) -> List[ColorCode]:
        """
        Returns the secret code.

        Returns:
            List[ColorCode]: The secret code.
        """
        return self.secret_code

    def get_turns(self) -> List[GameTurn]:
        """
        Returns the list of turns.

        Returns:
            List[GameTurn]: The list of turns.
        """
        return self.turns

    def __repr__(self):
        """
        Returns the string representation of the game state.

        Returns:
            str: The string representation of the game state.
        """
        return (
            f"GameState(secret_code={self.secret_code}, "
            f"turns={self.turns}, max_rounds={self.max_rounds})"
        )
