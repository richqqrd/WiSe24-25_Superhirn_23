import os
from src.util.ColorCode import ColorCode

class GameRenderer:
    """
    Responsible for rendering the game state and feedback in the CLI.
    """

    COLORS = {
        ColorCode.RED.value: '\033[31m',  # Red
        ColorCode.GREEN.value: '\033[32m',  # Green
        ColorCode.YELLOW.value: '\033[33m',  # Yellow
        ColorCode.BLUE.value: '\033[34m',  # Blue
        ColorCode.ORANGE.value: '\033[38;5;214m',  # Orange
        ColorCode.BROWN.value: '\033[38;5;94m',  # Brown
        ColorCode.WHITE.value: '\033[97m',  # Bright White
        ColorCode.BLACK.value: '\033[90m',  # Bright Black
        'reset': '\033[0m'  # Reset
    }

    def __init__(self):
        pass

    def clear_screen(self):
        """
        Clears the console screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def colorize(self, pins):
        """
        Converts a numeric code into a string with colored digits.

        :param pins: String representing the code or guess.
        :return: Colored string representation of the code.
        """
        return ''.join([self.COLORS.get(int(char), self.COLORS['reset']) + char + self.COLORS['reset'] for char in pins])

    def render_game_state(self, round_number, guesses, feedback):
        """
        Renders the game state, showing round number, feedback, and guesses.

        :param round_number: Current round number.
        :param guesses: List of guesses made by the player.
        :param feedback: List of feedback corresponding to each guess.
        """
        print("Super Superhirn")
        print("=================")
        print("Round | Feedback | Guess")
        print("--------------------------")

        for rnd, guess, fb in zip(range(1, round_number + 1), guesses, feedback):
            feedback_str = self.colorize(fb)  # Feedback pins in black/white
            guess_str = self.colorize(guess)  # Guess pins in colors
            print(f" {rnd:<5} | {feedback_str:<10} | {guess_str}")

        print("\nMake your next guess!")

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
    renderer.render_game_state(3, ["12345", "56781", "23456"], ["887", "888", "8888"])
    renderer.render_message("Test Message")
    renderer.render_warning("Test Warning")