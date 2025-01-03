"""Test module for ApplicationLogic."""
import unittest
from unittest.mock import Mock
from src.application_logic.application_logic import ApplicationLogic
from src.business_logic.business_logic import BusinessLogic
from src.business_logic.game_turn import GameTurn
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode
from src.persistence.i_persistence_manager import IPersistenceManager


class TestApplicationLogic(unittest.TestCase):
    """Test suite for the ApplicationLogic class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock the persistence manager
        mock_persistence_manager = Mock(spec=IPersistenceManager)
        self.game_logic = BusinessLogic(mock_persistence_manager)
        self.app_logic = ApplicationLogic(self.game_logic)
        self.game_logic.positions = 4
        self.game_logic.colors = 6

    def test_is_valid_code(self):
        """Test code validation."""
        # Valid cases
        self.assertTrue(self.app_logic._is_valid_code("1234"))
        self.assertTrue(self.app_logic._is_valid_code("6543"))

        # Invalid cases
        self.assertFalse(self.app_logic._is_valid_code("123"))  # Too short
        self.assertFalse(self.app_logic._is_valid_code("12345"))  # Too long
        self.assertFalse(self.app_logic._is_valid_code("123A"))  # Invalid char
        self.assertFalse(self.app_logic._is_valid_code(""))  # Empty
        self.assertFalse(self.app_logic._is_valid_code("0123"))  # Invalid number
        self.assertFalse(self.app_logic._is_valid_code("7890"))  # Out of range

    def test_is_valid_feedback(self):
        """Test feedback validation."""
        # Valid cases
        self.assertTrue(self.app_logic._is_valid_feedback("78"))
        self.assertTrue(self.app_logic._is_valid_feedback("8877"))
        self.assertTrue(self.app_logic._is_valid_feedback(""))

        # Invalid cases
        self.assertFalse(self.app_logic._is_valid_feedback("789"))  # Invalid number
        self.assertFalse(self.app_logic._is_valid_feedback("12"))  # Invalid feedback
        self.assertFalse(self.app_logic._is_valid_feedback("A8"))  # Invalid char

    def test_convert_to_color_code(self):
        """Test color code conversion."""
        # Single valid conversion
        self.assertEqual(self.app_logic._convert_to_color_code(1), ColorCode.RED)
        self.assertEqual(self.app_logic._convert_to_color_code(2), ColorCode.GREEN)
        self.assertEqual(self.app_logic._convert_to_color_code(4), ColorCode.BLUE)

        # Invalid input raises ValueError
        with self.assertRaises(ValueError):
            self.app_logic._convert_to_color_code(9)  # Out of range

    def test_handle_code_input(self):
        """Test code input handling."""
        # Valid input
        self.assertEqual(self.app_logic.handle_code_input("1234"), "wait_for_computer_guess")

        # Invalid input
        self.assertEqual(self.app_logic.handle_code_input("123"), "need_code_input")
        self.assertEqual(self.app_logic.handle_code_input("ABCD"), "need_code_input")
        self.assertEqual(self.app_logic.handle_code_input(""), "need_code_input")


    def test_handle_guess_input(self):
        """Test guess input handling."""
        # Configure game first
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)

        # Then start game
        self.game_logic.startgame("guesser")

        # Valid guess
        result = self.app_logic.handle_guess_input("1234")
        self.assertIn(result, ["need_guess_input", "game_over"])

        # Invalid guess
        result = self.app_logic.handle_guess_input("invalid")
        self.assertEqual(result, "need_guess_input")

    def test_handle_feedback_input_conversion(self):
        """Test feedback string to enum conversion in handle_feedback_input."""
        # Setup game state first
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)
        self.game_logic.make_computer_guess()

        # Test conversion through handle_feedback_input
        result = self.app_logic.handle_feedback_input("78")
        self.assertNotEqual(result, "need_feedback_input")  # Valid conversion

        result = self.app_logic.handle_feedback_input("12")
        self.assertEqual(result, "need_feedback_input")  # Invalid conversion#
    
    def test_handle_code_input_invalid(self):
        """Test handling of invalid code input."""
        # Invalid inputs
        self.assertEqual(self.app_logic.handle_code_input("123"), "need_code_input")  # Too short
        self.assertEqual(self.app_logic.handle_code_input("12345"), "need_code_input")  # Too long
        self.assertEqual(self.app_logic.handle_code_input("ABCD"), "need_code_input")  # Invalid chars
        self.assertEqual(self.app_logic.handle_code_input(""), "need_code_input")  # Empty

    def test_handle_guess_input(self):
        """Test guess input handling."""
        # Configure and start game first
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")
        
        # Valid guess
        result = self.app_logic.handle_guess_input("1234")
        self.assertIn(result, ["need_guess_input", "game_over"])

        # Invalid guesses
        self.assertEqual(self.app_logic.handle_guess_input("123"), "need_guess_input")
        self.assertEqual(self.app_logic.handle_guess_input("ABCD"), "need_guess_input")
        self.assertEqual(self.app_logic.handle_guess_input(""), "need_guess_input")

    def test_handle_feedback_input(self):
        """Test feedback input handling."""
        # Configure and start game first
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)
        self.game_logic.make_computer_guess()

        # Partial feedback - game continues
        self.assertEqual(self.app_logic.handle_feedback_input("78"), "wait_for_computer_guess")

        # All correct feedback - computer wins
        self.assertEqual(self.app_logic.handle_feedback_input("8888"), "game_lost")

        # Invalid feedback
        self.assertEqual(self.app_logic.handle_feedback_input("999"), "need_feedback_input")
        self.assertEqual(self.app_logic.handle_feedback_input("ABC"), "need_feedback_input")

    def test_handle_computer_guess(self):
        """Test computer guess handling."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)

        # Test computer guess
        result = self.app_logic.handle_computer_guess()
        self.assertIn(result, ["need_feedback_input", "game_over"])  # include need_feedback_input

    def test_is_valid_code_none(self):
        """Test code validation with None input."""
        self.assertFalse(self.app_logic._is_valid_code(None))

    def test_handle_invalid_role(self):
        """Test handling invalid role."""
        # Configure and start game with invalid role
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        result = self.game_logic.startgame("invalid_role")
        self.assertEqual(result, "invalid_role")


if __name__ == "__main__":
    unittest.main()