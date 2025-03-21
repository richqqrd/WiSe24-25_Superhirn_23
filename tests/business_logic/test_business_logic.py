"""Test module for the business_logic class."""
import unittest
from unittest.mock import Mock, patch

from src.business_logic.business_logic import BusinessLogic
from src.business_logic.guesser.computer_guesser import ComputerGuesser
from src.business_logic.guesser.player_guesser import PlayerGuesser
from src.persistence.i_persistence_manager import IPersistenceManager
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode
from src.business_logic.game_turn import GameTurn


class TestBusinessLogic(unittest.TestCase):
    """Test suite for the business_logic class.

    This class tests the core game logic functionality including game initialization,
    making guesses, handling feedback, and determining game end conditions.
    """

    def setUp(self: "TestBusinessLogic") -> None:
        """Set up test fixtures before each test method."""
        # Mock persistence manager needed
        mock_persistence_manager = Mock(spec=IPersistenceManager)
        self.game_logic = BusinessLogic(mock_persistence_manager)
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)  # Configure game first

    def test_startgame_as_guesser(self: "TestBusinessLogic") -> None:
        """Test game initialization when player is guesser."""
        result = self.game_logic.startgame("guesser")
        self.assertEqual(result, "need_guess_input")
        self.assertIsNotNone(self.game_logic.game_state)
        self.assertIsNotNone(self.game_logic.computer_coder)
        self.assertEqual(len(self.game_logic.game_state.secret_code),
                         self.game_logic.positions)

    def test_startgame_as_coder(self: "TestBusinessLogic") -> None:
        """Test game initialization when player is coder."""
        # Start game as coder
        result = self.game_logic.startgame("coder")
        self.assertEqual(result, "need_code_input")

        # Set secret code to initialize game state
        secret_code = [ColorCode(1)] * 4
        self.game_logic.set_secret_code(secret_code)

        # Now verify game state
        self.assertIsNotNone(self.game_logic.game_state)
        self.assertIsNotNone(self.game_logic.computer_guesser)

    def test_make_guess_valid(self: "TestBusinessLogic") -> None:
        """Test making a valid guess."""
        self.game_logic.startgame("guesser")
        guess = [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4)]
        result = self.game_logic.make_guess(guess)

        self.assertIn(result, ["need_guess_input", "game_over"])
        last_turn = self.game_logic.game_state.turns[-1]
        self.assertEqual(last_turn.guesses, guess)
        self.assertGreater(len(last_turn.feedback), 0)

    def test_make_guess_invalid(self: "TestBusinessLogic") -> None:
        """Test making an invalid guess."""
        self.game_logic.startgame("guesser")

        # Test that invalid guesses are handled before adding to game state
        def assert_invalid_guess(guess: list[ColorCode]) -> None:
            """Helper to test an invalid guess."""
            initial_turn_count = len(self.game_logic.game_state.turns)
            result = self.game_logic.make_guess(guess)
            self.assertEqual(result, "need_guess_input")
            self.assertEqual(len(self.game_logic.game_state.turns), initial_turn_count)

        # Test each invalid case
        assert_invalid_guess([])  # Empty
        assert_invalid_guess([ColorCode(1)])  # Too short
        # Too long
        assert_invalid_guess([ColorCode(1)] * (self.game_logic.positions + 1))
        assert_invalid_guess([ColorCode(7)])  # Invalid color
        assert_invalid_guess(None)  # None

    def test_is_game_over_win(self: "TestBusinessLogic") -> None:
        """Test game over condition when player wins."""
        self.game_logic.startgame("guesser")
        feedback = [FeedbackColorCode.BLACK] * self.game_logic.positions  # All correct
        result = self.game_logic.is_game_over(feedback)
        self.assertEqual(result, "game_won")

    def test_is_game_over_max_rounds(self: "TestBusinessLogic") -> None:
        """Test game over condition when max rounds reached.

        Verifies that the game ends when maximum rounds are reached.
        """
        self.game_logic.startgame("guesser")

        # Create turn with correct number of positions
        turn = GameTurn(
            [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4)],  # 4 positions
            [FeedbackColorCode.WHITE]
        )

        # Add turns until max rounds reached
        for _ in range(self.game_logic.max_round):
            self.game_logic.game_state.add_turn(turn)

        result = self.game_logic.is_game_over([FeedbackColorCode.WHITE])
        self.assertEqual(result, "game_lost")  # Player loses when max rounds reached

    def test_make_guess_network(self: "TestBusinessLogic") -> None:
        """Test making a guess with network service."""
        # Setup
        self.game_logic.startgame("guesser")
        self.game_logic.network_service = Mock()
        guess = [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4)]

        # Test successful network guess
        self.game_logic.network_service.make_move.return_value = "8877"
        result = self.game_logic.make_guess(guess)

        # Verify guess string conversion and feedback processing
        self.game_logic.network_service.make_move.assert_called_with("1234")
        last_turn = self.game_logic.game_state.turns[-1]
        self.assertEqual(
            last_turn.feedback,
            [FeedbackColorCode.BLACK, FeedbackColorCode.BLACK,
             FeedbackColorCode.WHITE, FeedbackColorCode.WHITE]
        )
        self.assertIn(result, ["need_guess_input", "game_over"])

        # Test network error case
        self.game_logic.network_service.make_move.return_value = None
        result = self.game_logic.make_guess(guess)
        self.assertEqual(result, "error")

    def test_is_game_over_max_rounds_computer_wins(self: "TestBusinessLogic") -> None:
        """Test game over condition when max rounds reached with computer guesser."""
        # Setup game with computer as guesser
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)

        # Create turn with correct number of positions
        turn = GameTurn(
            [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4)],
            [FeedbackColorCode.WHITE]
        )

        # Add turns until max rounds reached
        for _ in range(self.game_logic.max_round):
            self.game_logic.game_state.add_turn(turn)

        # Test that computer wins when max rounds reached
        result = self.game_logic.is_game_over([FeedbackColorCode.WHITE])
        self.assertEqual(result, "game_won")
        # Computer wins when max rounds reached as guesser

    def test_set_feedback_exceptions(self: "TestBusinessLogic") -> None:
        """Test set_feedback exception handling."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")
        # Set secret code to initialize GameState
        self.game_logic.set_secret_code([ColorCode(1)] * 4)

        # Test empty turns list (IndexError)
        result = self.game_logic.set_feedback([FeedbackColorCode.BLACK])
        self.assertEqual(result, "need_feedback_input")

        # Test ValueError case
        self.game_logic.game_state.get_turns = Mock(side_effect=ValueError)
        result = self.game_logic.set_feedback([FeedbackColorCode.BLACK])
        self.assertEqual(result, "need_feedback_input")

    def test_set_secret_code_exception(self: "TestBusinessLogic") -> None:
        """Test set_secret_code error handling."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")

        # Mock GameState to raise ValueError
        with patch('src.business_logic.business_logic.GameState',
                   side_effect=ValueError):
            result = self.game_logic.set_secret_code([ColorCode(1)] * 4)
            self.assertEqual(result, "need_code_input")

    def test_make_computer_guess_exceptions(self: "TestBusinessLogic") -> None:
        """Test computer guess exception handling."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)

        # Test cheating detection
        self.game_logic.computer_guesser.make_guess = Mock(
            side_effect=ValueError("CHEATING_DETECTED")
        )
        result = self.game_logic.make_computer_guess()
        self.assertEqual(result, "cheating_detected")

        # Test other ValueError
        self.game_logic.computer_guesser.make_guess = Mock(
            side_effect=ValueError("Some other error")
        )
        result = self.game_logic.make_computer_guess()
        self.assertEqual(result, "error")

    def test_load_game_state(self: "TestBusinessLogic") -> None:
        """Test loading game state."""
        # Test loading player guesser game
        mock_game_state = Mock()
        mock_game_state.current_guesser = PlayerGuesser()
        mock_game_state.positions = 4
        mock_game_state.colors = 6
        mock_game_state.player_name = "TestPlayer"
        mock_game_state.max_rounds = 10
        mock_game_state.secret_code = [ColorCode(1)] * 4
        mock_game_state.get_turns.return_value = []  # Leere Liste für iterierbare Turns

        self.game_logic.persistence_manager.load_game_state.return_value = (
            mock_game_state)
        result = self.game_logic.load_game_state()
        self.assertEqual(result, "game_loaded")

        # Test loading computer guesser game (should fail)
        mock_game_state.current_guesser = ComputerGuesser(4, 6)
        result = self.game_logic.load_game_state()
        self.assertEqual(result, "error")

    def test_has_saved_game(self: "TestBusinessLogic") -> None:
        """Test checking for saved game existence."""
        # Test when no save exists
        self.game_logic.persistence_manager.has_saved_game.return_value = False
        result = self.game_logic.has_saved_game()
        self.assertFalse(result)

        # Test when save exists
        self.game_logic.persistence_manager.has_saved_game.return_value = True
        result = self.game_logic.has_saved_game()
        self.assertTrue(result)

        # Verify persistence manager was called
        self.game_logic.persistence_manager.has_saved_game.assert_called()

    def test_make_computer_guess_network(self: "TestBusinessLogic") -> None:
        """Test computer guess with network service."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)
        self.game_logic.network_service = Mock()

        # Test successful network guess
        self.game_logic.network_service.make_move.return_value = "8877"
        result = self.game_logic.make_computer_guess()
        self.assertIn(result, ["need_feedback_input", "game_over",
                               "wait_for_computer_guess"])

        # Test different network errors
        error_tests = [
            ({"error": "connection_failed"}, "connection_error"),
            ({"error": "server_error"}, "server_error"),
            ({"error": "timeout"}, "timeout_error"),
            ({"error": "unknown"}, "network_error:unknown"),
            (None, "error")
        ]

        for error_response, expected_result in error_tests:
            self.game_logic.network_service.make_move.return_value = error_response
            result = self.game_logic.make_computer_guess()
            self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
