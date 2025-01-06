"""Module for rendering game states and UI elements."""

import os
from typing import List, Union

from src.business_logic.game_state import GameState # noqa
from src.business_logic.guesser.computer_guesser import ComputerGuesser # noqa
from src.util.color_code import ColorCode # noqa
from src.util.feedback_color_code import FeedbackColorCode # noqa

from src.util.translations import translations


class GameRenderer:
    """Game state and UI renderer.

    This class handles rendering the game state and UI elements with
    proper formatting and translations.

    Attributes:
        language: Current language code for translations
    """

    def __init__(self: "GameRenderer", language: str = "en") -> None:
        """Initialize the renderer with a language.

        Args:
            language: Language code, defaults to 'en'
        """
        self.language = language

    def set_language(self: "GameRenderer", language: str) -> None:
        """Set the display language.

        Args:
            language: Language code to switch to
        """
        if language in translations:
            self.language = language

    def clear_screen(self: "GameRenderer") -> None:
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def colorize(
        self: "GameRenderer",
        pins: List[Union[ColorCode, FeedbackColorCode]],
        width: int = 15,
    ) -> str:
        """Format and colorize pins with consistent width.

        Args:
            pins: List of pins to colorize
            width: Total width for output formatting, defaults to 15

        Returns:
            str: Formatted and colorized string with padding
        """
        if not pins:
            return " " * width

        colored_pins = [
            pin.get_ansi_code() + str(pin.value) + "\033[0m" for pin in pins
        ]
        pin_str = " ".join(colored_pins)

        visible_length = len(" ".join(str(pin.value) for pin in pins))
        padding = (width - visible_length) // 2

        return " " * padding + pin_str + " " * (width - visible_length - padding)

    def render_game_state(self: "GameRenderer", game_state: GameState) -> None:
        """Render the current game state to the console.

        Displays game title, player info, settings, secret code (if applicable),
        and all game turns with their feedback.

        Args:
            game_state: Current game state to render
        """
        self.clear_screen()

        if game_state is None:
            return

        print(f"{os.linesep}" + "=" * 40)
        print(f"{translations[self.language]['game_title'].center(40)}")
        print("=" * 40)

        print(
            f"{os.linesep}{translations[self.language]['player_label']}"
            f"{game_state.player_name}"
        )
        print(
            f"{translations[self.language]['settings_label']} "
            + translations[self.language]["settings_format"].format(
                game_state.positions, game_state.colors, game_state.max_rounds
            )
        )
        print(f"{os.linesep}" + "-" * 40)

        if game_state.secret_code is not None and isinstance(
            game_state.current_guesser, ComputerGuesser
        ):
            secret_code_str = self.colorize(game_state.secret_code)
            print(
                f"{os.linesep}{translations[self.language]['secret_code']}: "
                f"{secret_code_str}"
            )

        round_width = 8
        feedback_width = 15
        guess_width = 15

        print(
            f"{os.linesep}{translations[self.language]['round']:^{round_width}} | "
            + f"{translations[self.language]['feedback']:^{feedback_width}} | "
            + f"{translations[self.language]['guess']:^{guess_width}}"
        )
        print(
            "-" * (round_width + feedback_width + guess_width + 4)
        )  # +4 für die Trennzeichen

        for round_num, turn in enumerate(game_state.get_turns(), 1):
            feedback_str = self.colorize(turn.feedback, width=feedback_width)
            guess_str = self.colorize(turn.guesses, width=guess_width)
            print(f"{round_num:^{round_width}} | {feedback_str} | {guess_str}")
            print("-" * (round_width + feedback_width + guess_width + 4))
        print(f"{os.linesep}{translations[self.language]['menu_hint']}")

    def render_message(self: "GameRenderer", message: str) -> None:
        """Render a centered message with decorative borders.

        Args:
            message: The message text to display
        """
        print(f"{os.linesep}" + "-" * 40)
        print(f"{message.center(40)}")
        print("-" * 40)

    def render_warning(self: "GameRenderer", warning: str) -> None:
        """Render a warning message with prominent borders.

        Args:
            warning: The warning text to display
        """
        print(f"{os.linesep}" + "!" * 40)
        print(f"WARNING: {warning.center(30)}")
        print("!" * 40 + f"{os.linesep}")
        print("Going back to main menu in 10 seconds...")
