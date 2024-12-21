import os

from src.GameLogic.GameState import GameState
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode
from typing import List, Dict, Tuple, Union


class GameRenderer:
    """
    Responsible for rendering the game state and feedback in the CLI.
    """

    def clear_screen(self) -> None:
        """
        Clears the console screen.
        """
        os.system("cls" if os.name == "nt" else "clear")

    def colorize(self, pins: List[Union[ColorCode, FeedbackColorCode]]) -> str:
        """
        Converts a list of ColorCode or FeedbackColorCode enums
        into a string with colored digits.

        :param pins: List of ColorCode or FeedbackColorCode enums.
        :return: Colored string representation of the code.
        """
        return "".join(
            [pin.get_ansi_code() + str(pin.value) + "\033[0m" for pin in pins]
        )

    def render_game_state(self, game_state: GameState) -> None:
        """
        Renders the game state, showing round number, feedback, and guesses.

        :param game_state: Dict with round number as key and a tuple of lists
        (guesses, feedback).
        """
        self.clear_screen()
        secret_code_str = self.colorize(game_state.secret_code)
        print(f"Secret Code: {secret_code_str}")
        print("Super Superhirn")
        print("=================")
        print("Round | Feedback | Guess")
        print("--------------------------")

        for round_num, turn in enumerate(game_state.get_turns(), 1):
            feedback_str = self.colorize(turn.feedback) if turn.feedback else " " * 5
            guess_str = self.colorize(turn.guesses)
            print(f" {round_num:<5} | {feedback_str:<10} | {guess_str}")

    def render_message(self, message: str) -> None:
        """
        Renders a general message to the user.

        :param message: The message to display.
        """
        print(f"\n{message}\n")

    def render_warning(self, warning: str) -> None:
        """
        Renders a warning message to the user.

        :param warning: The warning message to display.
        """
        print(f"WARNING: {warning}\n")
