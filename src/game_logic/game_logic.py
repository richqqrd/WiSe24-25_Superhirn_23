"""Module for core game logic implementation."""

from typing import List

from src.game_logic import game_logic
from src.game_logic.coder.computer_coder import ComputerCoder
from src.game_logic.coder.player_coder import PlayerCoder
from src.game_logic.game_state import GameState
from src.game_logic.game_turn import GameTurn
from src.game_logic.guesser.computer_guesser import ComputerGuesser
from src.game_logic.guesser.player_guesser import PlayerGuesser
from src.business_logic.i_business_logic import IGameLogic
from src.Network.network_service import NetworkService
from src.Persistence.i_persistence_manager import IPersistenceManager
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class GameLogic(IGameLogic):
    """Core game logic implementation.

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

    def __init__(self: "game_logic", persistence_manager: IPersistenceManager) -> None:
        """Initialize game_logic with persistence manager.

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

    def startgame(self: "game_logic", role: str) -> str:
        """Start a new game with the given role.

        Args:
            role: Role of the player ('guesser', 'coder', 'online_guesser')

        Returns:
            str: Initial game state or error message
        """
        if role == "guesser":
            return self.start_as_guesser()
        elif role == "coder":
            return self.start_as_coder()
        elif role == "online_guesser":
            return "need_server_connection"
        return "invalid_role"

    def make_guess(self: "game_logic", guess_list: List[ColorCode]) -> str:
        """Make a guess as the player guesser.

        Args:
            guess_list: List of color codes representing the guess

        Returns:
            str: Next game state after the current turn
        """
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

    def is_game_over(self: "game_logic", feedback_list: List[FeedbackColorCode]) -> str:
        """Check if the game is over based on feedback.

        Args:
            feedback_list: List of feedback pins

        Returns:
            str: Game state after the current turn
        """
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

    def set_feedback(self: "game_logic", feedback_list: List[FeedbackColorCode]) -> str:
        """Set feedback for the current guess.

        Args:
            feedback_list: List of feedback pins

        Returns:
            str: Game state after the current turn
        """
        try:
            current_turn = self.game_state.get_turns()[-1]
            current_turn.feedback = feedback_list

            if isinstance(self.game_state.current_guesser, ComputerGuesser):
                self.game_state.current_guesser.process_feedback(feedback_list)

            return self.is_game_over(feedback_list)
        except (IndexError, ValueError):
            return "need_feedback_input"

    def set_secret_code(self: "game_logic", code_list: List[ColorCode]) -> str:
        """Set the secret code for the game.

        Args:
            code_list: List of color codes representing the secret code

        Returns:
            str: Next game state after setting the code
        """
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

    def make_computer_guess(self: "game_logic") -> str:
        """Make a guess as the computer player.

        Returns:
            str: Next game state after computer's guess
        """
        try:
            guess = self.computer_guesser.make_guess()
            turn = GameTurn(guess, [])
            self.game_state.add_turn(turn)
            return "need_feedback_input"
        except ValueError as e:
            if str(e) == "CHEATING_DETECTED":
                return "cheating_detected"
            return "error"

    def get_game_state(self: "game_logic") -> GameState:
        """Get the current game state.

        Returns:
            GameState: Current game state
        """
        return self.game_state

    def save_game_state(self: "game_logic") -> str:
        """Save the current game state through persistence layer.

        Returns:
            str: Save operation result status
        """
        self.persistence_manager.save_game_state(self.game_state)
        return "game_saved"

    def load_game_state(self: "game_logic") -> str:
        """Load a previously saved game state through persistence layer.

        Returns:
            str: Load operation result status
        """
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
        self: "game_logic",
        player_name: str,
        positions: int,
        colors: int,
        max_attempts: int,
    ) -> None:
        """Configure game settings.

        Args:
            player_name: Name of the player
            positions: Number of code positions
            colors: Number of available colors
            max_attempts: Maximum allowed attempts
        """
        self.player_name = player_name
        self.positions = positions
        self.colors = colors
        self.max_round = max_attempts
        self.computer_guesser = ComputerGuesser(positions, colors)
        self.computer_coder = ComputerCoder(positions, colors)

    def has_saved_game(self: "game_logic") -> bool:
        """Check if saved game exists through persistence layer.

        Returns:
            bool: True if saved game exists, False otherwise
        """
        return self.persistence_manager.has_saved_game()

    def start_as_coder(self: "game_logic") -> str:
        """Start a new game with player as code maker.

        Private helper method called by startgame().

        Returns:
            str: "need_code_input" to request secret code from player
        """
        return "need_code_input"

    def start_as_guesser(self: "game_logic") -> str:
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
        self: "game_logic", server_ip: str, server_port: int
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
