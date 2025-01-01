"""Module for core game logic implementation."""

from typing import List
from src.GameLogic.Coder.computer_coder import ComputerCoder
from src.GameLogic.Coder.player_coder import PlayerCoder
from src.GameLogic.game_state import GameState
from src.GameLogic.game_turn import GameTurn
from src.GameLogic.Guesser.computer_guesser import ComputerGuesser
from src.GameLogic.Guesser.player_guesser import PlayerGuesser
from src.GameLogic.i_game_logic import IGameLogic
from src.Network.network_service import NetworkService
from src.Persistence.i_persistence_manager import IPersistenceManager
from src.Persistence.persistence_manager import PersistenceManager
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class GameLogic(IGameLogic):
    """Core game logic implementation.

    This class implements the game mechanics including:
        - Game state management
        - Player/Computer moves
        - Win/loss conditions
        - Network gameplay
        - Game persistence

    Attributes:
        player_guesser: Player instance for guessing role
        player_coder: Player instance for coding role
        computer_guesser: Computer instance for guessing role
        computer_coder: Computer instance for coding role
        network_service: Service for online gameplay
        game_state: Current state of the game
        max_round: Maximum number of rounds allowed
        player_name: Name of the player
        colors: Number of available colors
        positions: Number of positions in the code
        persistence_manager: Manager for saving/loading games
    """

    def __init__(self: "GameLogic", persistence_manager: IPersistenceManager) -> None:
        """Initialize GameLogic with persistence manager.

        Args:
            persistence_manager: Manager for saving/loading game states
        """
        self.player_guesser = PlayerGuesser()
        self.player_coder = PlayerCoder()
        self.computer_guesser = None
        self.computer_coder = None
        self.network_service = None
        self.game_state = None
        self.max_round = 12
        self.player_name = "player1"
        self.colors = 8
        self.positions = 5
        self.persistence_manager = persistence_manager

    def startgame(self: "GameLogic", role: str) -> str:
        if role == "guesser":
            return self.start_as_guesser()
        elif role == "coder":
            return self.start_as_coder()
        elif role == "online_guesser":
            return "need_server_connection"
        return "invalid_role"

    def make_guess(self: "GameLogic", guess_list: List[ColorCode]) -> str:
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

    def is_game_over(self: "GameLogic", feedback_list: List[FeedbackColorCode]) -> str:
        if len(feedback_list) == self.positions and all(
            [f == FeedbackColorCode.BLACK for f in feedback_list]
        ):
            if isinstance(self.game_state.current_guesser, PlayerGuesser):
                return "game_won"
            else:
                return "game_lost"

        if len(self.game_state.get_turns()) >= self.max_round:
            if isinstance(self.game_state.current_guesser, PlayerGuesser):
                return "game_lost"  # Spieler hat verloren
            else:
                return "game_won"

        if isinstance(self.game_state.current_guesser, PlayerGuesser):
            return "need_guess_input"
        else:
            return "wait_for_computer_guess"

    def set_feedback(self: "GameLogic", feedback_list: List[FeedbackColorCode]) -> str:
        try:
            current_turn = self.game_state.get_turns()[-1]
            current_turn.feedback = feedback_list

            if isinstance(self.game_state.current_guesser, ComputerGuesser):
                self.game_state.current_guesser.process_feedback(feedback_list)

            return self.is_game_over(feedback_list)
        except (IndexError, ValueError):
            return "need_feedback_input"

    def set_secret_code(self: "GameLogic", code_list: List[ColorCode]) -> str:
        try:
            self.game_state = GameState(
                code_list,
                self.max_round,
                self.positions,
                self.colors,
                self.player_name,
                self.computer_guesser,
            )
            return "wait_for_computer_guess"
        except ValueError:
            return "need_code_input"

    def make_computer_guess(self: "GameLogic") -> str:
        try:
            guess = self.computer_guesser.make_guess()
            turn = GameTurn(guess, [])
            self.game_state.add_turn(turn)
            return "need_feedback_input"
        except ValueError as e:
            if str(e) == "CHEATING_DETECTED":
                return "cheating_detected"
            return "error"

    def get_game_state(self: "GameLogic") -> GameState:
        return self.game_state

    def save_game_state(self: "GameLogic") -> str:
        self.persistence_manager.save_game_state(self.game_state)
        return "game_saved"

    def load_game_state(self: "GameLogic") -> str:
        self.game_state = self.persistence_manager.load_game_state()

        self.computer_coder = ComputerCoder(
            self.game_state.positions, self.game_state.colors
        )
        self.computer_guesser = ComputerGuesser(
            self.game_state.positions, self.game_state.colors
        )

        self.computer_coder.secret_code = self.game_state.secret_code

        for turn in self.game_state.get_turns():
            if isinstance(self.game_state.current_guesser, PlayerGuesser):
                # Player is guesser, recalculate computer feedback
                feedback = self.computer_coder.give_feedback(turn.guesses)
                turn.feedback = feedback
            else:
                # Computer is guesser, replay computer guesses and feedback
                self.computer_guesser.last_guess = turn.guesses
                if turn.feedback:
                    self.computer_guesser.process_feedback(turn.feedback)

        return "game_loaded"

    def configure_game(
        self: "GameLogic",
        player_name: str,
        positions: int,
        colors: int,
        max_attempts: int,
    ) -> None:
        self.player_name = player_name
        self.positions = positions
        self.colors = colors
        self.max_round = max_attempts
        self.computer_guesser = ComputerGuesser(positions, colors)
        self.computer_coder = ComputerCoder(positions, colors)

    def has_saved_game(self: "GameLogic") -> bool:
        """Check if saved game exists through persistence layer"""
        return self.persistence_manager.has_saved_game()

    def start_as_coder(self: "GameLogic") -> str:
        """Start a new game with player as code maker.

        Private helper method called by startgame().

        Returns:
            str: "need_code_input" to request secret code from player
        """
        return "need_code_input"

    def start_as_guesser(self: "GameLogic") -> str:
        """Start a new game with player as code guesser.

        Private helper method called by startgame().
        Creates new game state with computer generated secret code.

        Returns:
            str: "need_guess_input" to request first guess from player

        Raises:
            ValueError: If game configuration is invalid
        """
        try:
            secret_code = self.computer_coder.generate_code()
            self.game_state = GameState(
                secret_code,
                self.max_round,
                self.positions,
                self.colors,
                self.player_name,
                self.player_guesser,
            )
            return "need_guess_input"
        except ValueError:
            return "need_guess_input"

    def start_as_online_guesser(
        self: "GameLogic", server_ip: str, server_port: int
    ) -> str:
        """Start game as online guesser.

        Args:
            server_ip: IP address of the game server
            server_port: Port number of the game server

        Returns:
            str: "need_server_connection" if successful, "error" otherwise
        """
        self.network_service = NetworkService(server_ip, server_port)
        if self.network_service.start_game(self.player_name):
            self.game_state = GameState(
                None,
                self.max_round,
                self.positions,
                self.colors,
                self.player_name,
                self.player_guesser,
            )
            return "need_server_connection"
        return "error"
