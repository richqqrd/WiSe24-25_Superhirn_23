# src/CLI/game_renderer/game_renderer.py
import os
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode

class GameRenderer:
    """
    Responsible for rendering the game state and feedback in the CLI.
    """

    def __init__(self):
        pass

    def clear_screen(self):
        """
        Clears the console screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def colorize(self, pins):
        """
        Converts a list of ColorCode or FeedbackColorCode enums into a string with colored digits.

        :param pins: List of ColorCode or FeedbackColorCode enums.
        :return: Colored string representation of the code.
        """
        return ''.join([pin.get_ansi_code() + str(pin.value) + '\033[0m' for pin in pins])

    def render_game_state(self, game_state):
        """
        Renders the game state, showing round number, feedback, and guesses.

        :param game_state: Dictionary with round number as key and a tuple of lists (guesses, feedback) as value.
        """
        print("Super Superhirn")
        print("=================")
        print("Round | Feedback | Guess")
        print("--------------------------")

        for round_number, (guesses, feedback) in game_state.items():
            feedback_str = self.colorize(feedback)  # Feedback pins in black/white
            guess_str = self.colorize(guesses)  # Guess pins in colors
            print(f" {round_number:<5} | {feedback_str:<10} | {guess_str}")

    def render_message(self, message):
        """
        Renders a general message to the user.

        :param message: The message to display.
        """
        print(f"\n{message}\n")

    def render_warning(self, warning):
        """
        Renders a warning message to the user.

        :param warning: The warning message to display.
        """
        print(f"WARNING: {warning}\n")

# Example usage
if __name__ == "__main__":
    renderer = GameRenderer()
    renderer.clear_screen()
    game_state = {
        1: ([ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE], [FeedbackColorCode.BLACK, FeedbackColorCode.WHITE]),
        2: ([ColorCode.YELLOW, ColorCode.ORANGE, ColorCode.BROWN], [FeedbackColorCode.WHITE, FeedbackColorCode.BLACK])
    }
    renderer.render_game_state(game_state)
    renderer.render_message("Test Message")
    renderer.render_warning("Test Warning")