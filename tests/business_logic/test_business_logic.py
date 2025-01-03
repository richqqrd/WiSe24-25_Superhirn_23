import unittest
from unittest.mock import Mock

from src.business_logic.business_logic import BusinessLogic
from src.persistence.i_persistence_manager import IPersistenceManager
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode
from src.business_logic.game_turn import GameTurn


class TestBusinessLogic(unittest.TestCase):
    """Test suite for the business_logic class.

    This class tests the core game logic functionality including game initialization,
    making guesses, handling feedback, and determining game end conditions.
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock persistence manager needed
        mock_persistence_manager = Mock(spec=IPersistenceManager)
        self.game_logic = BusinessLogic(mock_persistence_manager)
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)  # Configure game first

    def test_startgame_as_guesser(self):
        """Test game initialization when player is guesser."""
        result = self.game_logic.startgame("guesser")
        self.assertEqual(result, "need_guess_input")
        self.assertIsNotNone(self.game_logic.game_state)
        self.assertIsNotNone(self.game_logic.computer_coder)
        self.assertEqual(len(self.game_logic.game_state.secret_code), self.game_logic.positions)

    def test_startgame_as_coder(self):
        """Test game initialization when player is coder."""
        result = self.game_logic.startgame("coder")
        self.assertEqual(result, "need_code_input")
        self.assertIsNotNone(self.game_logic.game_state)
        self.assertIsNotNone(self.game_logic.computer_guesser)

    def test_make_guess_valid(self):
        """Test making a valid guess."""
        self.game_logic.startgame("guesser")
        guess = [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4)]
        result = self.game_logic.make_guess(guess)

        self.assertIn(result, ["need_guess_input", "game_over"])
        last_turn = self.game_logic.game_state.turns[-1]
        self.assertEqual(last_turn.guesses, guess)
        self.assertGreater(len(last_turn.feedback), 0)

    def test_make_guess_invalid(self):
        """Test making an invalid guess."""
        self.game_logic.startgame("guesser")

        # Test that invalid guesses are handled before adding to game state
        def assert_invalid_guess(guess):
            """Helper to test an invalid guess."""
            initial_turn_count = len(self.game_logic.game_state.turns)
            result = self.game_logic.make_guess(guess)
            self.assertEqual(result, "need_guess_input")
            self.assertEqual(len(self.game_logic.game_state.turns), initial_turn_count)

        # Test each invalid case
        assert_invalid_guess([])  # Empty
        assert_invalid_guess([ColorCode(1)])  # Too short
        assert_invalid_guess([ColorCode(1)] * (self.game_logic.positions + 1))  # Too long
        assert_invalid_guess([ColorCode(7)])  # Invalid color
        assert_invalid_guess(None)  # None

    def test_is_game_over_win(self):
        """Test game over condition when player wins."""
        self.game_logic.startgame("guesser")
        feedback = [FeedbackColorCode.BLACK] * self.game_logic.positions  # All correct
        result = self.game_logic.is_game_over(feedback)
        self.assertEqual(result, "game_won")

    def test_is_game_over_max_rounds(self):
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


if __name__ == "__main__":
    unittest.main()
