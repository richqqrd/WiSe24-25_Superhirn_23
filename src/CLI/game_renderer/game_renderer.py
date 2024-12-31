import os
from src.GameLogic.GameState import GameState
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
        if not pins:
            return " " * width
        pin_str = " ".join([pin.get_ansi_code() + str(pin.value) + "\033[0m" for pin in pins])
        return f"{pin_str:^{width}}"

    def render_game_state(self, game_state: GameState) -> None:
        self.clear_screen()
        secret_code_str = self.colorize(game_state.secret_code)
        print(f"\n{translations[self.language]['secret_code']}:  {secret_code_str}")
        print("\n" + "=" * 40)
        print(f"{translations[self.language]['game_title'].center(40)}")
        print("=" * 40)
        print(
            f"\n{translations[self.language]['round']:^8} | {translations[self.language]['feedback']:^15} | {translations[self.language]['guess']:^15}"
        )
        print("-" * 40)

        for round_num, turn in enumerate(game_state.get_turns(), 1):
            feedback_str = self.colorize(turn.feedback, width=15)
            guess_str = self.colorize(turn.guesses, width=15)
            print(f" {round_num:^8} | {feedback_str} | {guess_str}")
            print("-" * 40)

    def render_message(self, message: str) -> None:
        print("\n" + "-" * 40)
        print(f"{message.center(40)}")
        print("-" * 40)

    def render_warning(self, warning: str) -> None:
        print("\n" + "!" * 40)
        print(f"WARNING: {warning.center(30)}")
        print("!" * 40 + "\n")
