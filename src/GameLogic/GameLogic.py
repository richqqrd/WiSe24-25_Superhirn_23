from typing import List
from src.GameLogic.Coder.ComputerCoder import ComputerCoder
from src.GameLogic.Coder.PlayerCoder import PlayerCoder
from src.GameLogic.GameState import GameState
from src.GameLogic.GameTurn import GameTurn
from src.GameLogic.Guesser.ComputerGuesser import ComputerGuesser
from src.GameLogic.Guesser.PlayerGuesser import PlayerGuesser
from src.GameLogic.IGameLogic import IGameLogic
from src.Network.network_service import NetworkService
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


# asd
class GameLogic(IGameLogic):
    def __init__(self):
        self.player_guesser = PlayerGuesser()
        self.player_coder = PlayerCoder()
        self.computer_guesser = ComputerGuesser()
        self.computer_coder = ComputerCoder()
        self.network_service = None
        self.game_state = None
        self.max_round = 12
        self.persistenceManager = PersistenceManager()

    def startgame(self, playerRole: str) -> str:
        if playerRole == "guesser":
            return self.start_as_guesser()
        elif playerRole == "coder":
            return self.start_as_coder()
        elif playerRole == "online_guesser":
            return "need_server_connection"
        return "invalid_role"

    def start_as_online_guesser(self, server_ip: str, server_port: int) -> str:
        self.network_service = NetworkService(server_ip, server_port)
        if self.network_service.start_game("player1"):
            self.game_state = GameState(None, self.max_round, self.player_guesser)
            return "need_server_connection"
        return "error"

    def make_guess(self, guess_list: List[ColorCode]) -> str:
        self.player_guesser.set_guess(guess_list)
        guess = self.player_guesser.make_guess()
        turn = GameTurn(guess_list, [])
        self.game_state.add_turn(turn)

        if self.network_service:
            guess_str = "".join(str(color.value) for color in guess_list)
            feedback_str = self.network_service.make_move(guess_str)
            if feedback_str is None:
                return "error"
            feedback_list = [
                FeedbackColorCode.BLACK if c == "8" else FeedbackColorCode.WHITE
                for c in feedback_str
            ]
            turn.feedback = feedback_list
            return self.is_game_over(feedback_list)
        else:
            feedback = self.computer_coder.give_feedback(guess)
            turn.feedback = feedback
            return self.is_game_over(feedback)

    def is_game_over(self, feedback_list: List[FeedbackColorCode]) -> str:
        if len(feedback_list) == 5 and all(
            [f == FeedbackColorCode.BLACK for f in feedback_list]
        ):
            return "game_over"

        if len(self.game_state.get_turns()) >= self.max_round:
            return "game_over"

        if isinstance(self.game_state.current_guesser, PlayerGuesser):
            return "need_guess_input"
        else:
            return "wait_for_computer_guess"

    def set_feedback(self, feedback_list: List[FeedbackColorCode]) -> str:
        try:
            current_turn = self.game_state.get_turns()[-1]
            current_turn.feedback = feedback_list

            if isinstance(self.game_state.current_guesser, ComputerGuesser):
                self.game_state.current_guesser.process_feedback(feedback_list)

            return self.is_game_over(feedback_list)
        except (IndexError, ValueError):
            return "need_feedback_input"

    def start_as_coder(self) -> str:
        return "need_code_input"

    def start_as_guesser(self) -> str:
        try:
            secret_code = self.computer_coder.generate_code()
            self.game_state = GameState(
                secret_code, self.max_round, self.player_guesser
            )
            return "need_guess_input"
        except ValueError:
            return "need_guess_input"

    def set_secret_code(self, code_list: List[ColorCode]) -> str:
        try:
            self.game_state = GameState(
                code_list, self.max_round, self.computer_guesser
            )
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

    def save_game_state(self):
        """
        Save the current game state to a file.
        """
        self.persistenceManager.save_game_state(self.game_state)
        return "game_saved"

    def load_game_state(self):
        """
        Load the game state from a file.
        """
        self.game_state = self.persistenceManager.load_game_state()
        return "game_loaded"
