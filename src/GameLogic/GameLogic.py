from typing import List

from src.GameLogic.Coder.ComputerCoder import ComputerCoder
from src.GameLogic.Coder.PlayerCoder import PlayerCoder
from src.GameLogic.GameState import GameState
from src.GameLogic.GameTurn import GameTurn
from src.GameLogic.Guesser.ComputerGuesser import ComputerGuesser
from src.GameLogic.Guesser.PlayerGuesser import PlayerGuesser
from src.GameLogic.IGameLogic import IGameLogic
from src.util.ColorCode import ColorCode


class GameLogic(IGameLogic):
    def __init__(self):
        self.player_guesser = PlayerGuesser()
        self.player_coder = PlayerCoder()
        self.computer_guesser = ComputerGuesser()
        self.computer_coder = ComputerCoder()

        self.game_state = None
        self.max_round = 12

    def startgame(self, playerRole: str) -> str:
        if playerRole == "guesser":
            return self.start_as_guesser()
        elif playerRole == "coder":
            return self.start_as_coder()

    def start_as_coder(self) -> str:
        return "need_code_input"

    def start_as_guesser(self) -> str:
        return "need_guess_input"

    def set_secret_code(self, code_list: List[ColorCode]) -> str:
        try:
            self.game_state = GameState(code_list, self.max_round)
            return "wait_for_computer_guess"
        except ValueError:
            return "need_code_input"

    def make_computer_guess(self) -> str:
        guess = self.computer_guesser.make_guess()

        turn = GameTurn(guess, [])
        self.game_state.add_turn(turn)
        return "show_computer_guess"

    def get_game_state(self) -> GameState:
        return self.game_state