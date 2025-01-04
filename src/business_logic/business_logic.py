"""Module for core business logic implementation."""

from typing import List
from src.business_logic.coder.computer_coder import ComputerCoder
from src.business_logic.coder.player_coder import PlayerCoder
from src.business_logic.game_state import GameState
from src.business_logic.game_turn import GameTurn
from src.business_logic.guesser.computer_guesser import ComputerGuesser
from src.business_logic.guesser.player_guesser import PlayerGuesser
from src.business_logic.i_business_logic import IBusinessLogic
from src.network.network_service import NetworkService
from src.persistence.i_persistence_manager import IPersistenceManager
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class BusinessLogic(IBusinessLogic):
    """Core game business implementation.

    This class implements the game mechanics including:
        - Game state management
        - Player/Computer moves
        - Win/loss conditions
        - network gameplay
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

    def __init__(self: "BusinessLogic", persistence_manager: IPersistenceManager) -> None:
        """Initialize business_logic with persistence manager.

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
        self.current_mode = None

    def startgame(self: "BusinessLogic", role: str) -> str:
        self.current_mode = role
        if role == "guesser":
            return self.start_as_guesser()
        elif role == "coder":
            return self.start_as_coder()
        elif role == "online_guesser":
            return "need_server_connection"
        elif role == "online_computer_guesser":
            return "need_server_connection"
        return "invalid_role"

    def make_guess(self: "BusinessLogic", guess_list: List[ColorCode]) -> str:
        if not guess_list or len(guess_list) != self.positions:
            return "need_guess_input"
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

    def is_game_over(self: "BusinessLogic", feedback_list: List[FeedbackColorCode]) -> str:
        if len(feedback_list) == self.positions and all(
            [f == FeedbackColorCode.BLACK for f in feedback_list]
        ):
            if isinstance(self.game_state.current_guesser, PlayerGuesser):
                return "game_won"
            else:
                return "game_lost"

        if len(self.game_state.get_turns()) >= self.max_round:
            if isinstance(self.game_state.current_guesser, PlayerGuesser):
                return "game_lost"
            else:
                return "game_won"

        if isinstance(self.game_state.current_guesser, PlayerGuesser):
            return "need_guess_input"
        else:
            return "wait_for_computer_guess"

    def set_feedback(self: "BusinessLogic", feedback_list: List[FeedbackColorCode]) -> str:
        try:
            current_turn = self.game_state.get_turns()[-1]
            current_turn.feedback = feedback_list

            if isinstance(self.game_state.current_guesser, ComputerGuesser):
                self.game_state.current_guesser.process_feedback(feedback_list)

            return self.is_game_over(feedback_list)
        except (IndexError, ValueError):
            return "need_feedback_input"

    def set_secret_code(self: "BusinessLogic", code_list: List[ColorCode]) -> str:
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

    def make_computer_guess(self: "BusinessLogic") -> str:
        try:
            guess = self.computer_guesser.make_guess()
            turn = GameTurn(guess, [])
            self.game_state.add_turn(turn)

            if self.network_service:
                guess_str = "".join(str(color.value) for color in guess)
                feedback_str = self.network_service.make_move(guess_str)
                if feedback_str is None:
                    return "error"

                feedback_list = [
                    FeedbackColorCode.BLACK if c == "8" else FeedbackColorCode.WHITE
                    for c in feedback_str
                ]
                turn.feedback = feedback_list

                self.computer_guesser.process_feedback(feedback_list)
                return self.is_game_over(feedback_list)
            return "need_feedback_input"
        except ValueError as e:
            if str(e) == "CHEATING_DETECTED":
                return "cheating_detected"
            return "error"

    def get_game_state(self: "BusinessLogic") -> GameState:
        return self.game_state

    def save_game_state(self: "BusinessLogic") -> str:
        self.persistence_manager.save_game_state(self.game_state)
        return "game_saved"

    def load_game_state(self: "BusinessLogic") -> str:
        self.game_state = self.persistence_manager.load_game_state()

        # Only allow loading if player was guesser
        if not isinstance(self.game_state.current_guesser, PlayerGuesser):
            return "error"

        # Initialize computer components
        self.computer_coder = ComputerCoder(
            self.game_state.positions, self.game_state.colors
        )

        # Store loaded game state properties
        self.positions = self.game_state.positions
        self.colors = self.game_state.colors
        self.player_name = self.game_state.player_name
        self.max_round = self.game_state.max_rounds

        # Create and restore player guesser
        self.player_guesser = PlayerGuesser()
        self.game_state.current_guesser = self.player_guesser

        # Restore computer coder state
        self.computer_coder.secret_code = self.game_state.secret_code

        # Replay turns to restore game state
        for turn in self.game_state.get_turns():
            feedback = self.computer_coder.give_feedback(turn.guesses)
            turn.feedback = feedback
            self.player_guesser.set_guess(turn.guesses)

        return "game_loaded"

    def configure_game(
        self: "BusinessLogic",
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

    def has_saved_game(self: "BusinessLogic") -> bool:
        """Check if saved game exists through persistence layer"""
        return self.persistence_manager.has_saved_game()

    def start_as_coder(self: "BusinessLogic") -> str:
        """Start a new game with player as code maker.

        Private helper method called by startgame().

        Returns:
            str: "need_code_input" to request secret code from player
        """
        return "need_code_input"

    def start_as_guesser(self: "BusinessLogic") -> str:
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
        self: "BusinessLogic", server_ip: str, server_port: int
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
    

    def start_as_online_computer_guesser(
        self: "BusinessLogic", server_ip: str, server_port: int
    ) -> str:
        """Start game online game as the computer as guesser.

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
                self.computer_guesser,
            )
            return "need_server_connection"
        return "error"
