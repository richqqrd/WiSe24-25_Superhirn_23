import os
from src.GameLogic.GameState import GameState
from src.GameLogic.Guesser.ComputerGuesser import ComputerGuesser
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode
from typing import List, Union

from src.util.translations import translations


class GameRenderer:
    def __init__(self, language: str = "en"):
        self.language = language

    def set_language(self, language: str) -> None:
        if language in translations:
            self.language = language

    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def colorize(self, pins: List[Union[ColorCode, FeedbackColorCode]], width: int = 15) -> str:
        """Format and colorize pins with consistent width"""
        if not pins:
            return " " * width

        colored_pins = [pin.get_ansi_code() + str(pin.value) + "\033[0m" for pin in pins]
        pin_str = " ".join(colored_pins)

        visible_length = len(" ".join(str(pin.value) for pin in pins))
        padding = (width - visible_length) // 2

        return " " * padding + pin_str + " " * (width - visible_length - padding)

    def render_game_state(self, game_state: GameState) -> None:
        self.clear_screen()

        if game_state is None:
            return

        print("\n" + "=" * 40)
        print(f"{translations[self.language]['game_title'].center(40)}")
        print("=" * 40)

        print(f"\n{translations[self.language]['player_label']} {game_state.player_name}")
        print(f"{translations[self.language]['settings_label']} " +
              translations[self.language]['settings_format'].format(
                  game_state.positions,
                  game_state.colors,
                  game_state.max_rounds
              ))
        print("\n" + "-" * 40)

        if game_state.secret_code is not None and isinstance(game_state.current_guesser, ComputerGuesser):
            secret_code_str = self.colorize(game_state.secret_code)
            print(f"\n{translations[self.language]['secret_code']}:  {secret_code_str}")

        round_width = 8
        feedback_width = 15
        guess_width = 15

        print(f"\n{translations[self.language]['round']:^{round_width}} | " +
              f"{translations[self.language]['feedback']:^{feedback_width}} | " +
              f"{translations[self.language]['guess']:^{guess_width}}")
        print("-" * (round_width + feedback_width + guess_width + 4))  # +4 für die Trennzeichen

        for round_num, turn in enumerate(game_state.get_turns(), 1):
            feedback_str = self.colorize(turn.feedback, width=feedback_width)
            guess_str = self.colorize(turn.guesses, width=guess_width)
            print(f"{round_num:^{round_width}} | {feedback_str} | {guess_str}")
            print("-" * (round_width + feedback_width + guess_width + 4))

    def render_message(self, message: str) -> None:
        print("\n" + "-" * 40)
        print(f"{message.center(40)}")
        print("-" * 40)

    def render_warning(self, warning: str) -> None:
        print("\n" + "!" * 40)
        print(f"WARNING: {warning.center(30)}")
        print("!" * 40 + "\n")
