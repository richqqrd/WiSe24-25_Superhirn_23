import unittest
from src.BusinessLogic.BusinessLogic import BusinessLogic
from src.GameLogic.GameLogic import GameLogic
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class TestBusinessLogic(unittest.TestCase):
    """Test suite for the BusinessLogic class.
    
    This test suite verifies the functionality of the BusinessLogic class,
    which handles input validation and conversion between the UI and game logic layers.
    """

    def setUp(self):
        """Set up test fixtures before each test method.
        
        Creates a new BusinessLogic instance with a GameLogic dependency
        for testing input handling and validation.
        """
        self.game_logic = GameLogic()
        self.business_logic = BusinessLogic(self.game_logic)

    def test_is_valid_code(self):
        """Test code validation.
        
        Verifies that the code validation correctly identifies valid
        and invalid color code inputs.
        """
        # Valid cases
        self.assertTrue(self.business_logic._is_valid_code("12345"))
        self.assertTrue(self.business_logic._is_valid_code("87654"))
        
        # Invalid cases
        self.assertFalse(self.business_logic._is_valid_code("123"))  # Too short
        self.assertFalse(self.business_logic._is_valid_code("123456"))  # Too long
        self.assertFalse(self.business_logic._is_valid_code("1234A"))  # Invalid character
        self.assertFalse(self.business_logic._is_valid_code(""))  # Empty string

    def test_is_valid_feedback(self):
        """Test feedback validation.
        
        Verifies that the feedback validation correctly identifies valid
        and invalid feedback inputs.
        """
        # Valid cases
        self.assertTrue(self.business_logic._is_valid_feedback("78"))
        self.assertTrue(self.business_logic._is_valid_feedback(""))
        
        # Invalid cases
        self.assertFalse(self.business_logic._is_valid_feedback("123"))  # Invalid characters
        self.assertFalse(self.business_logic._is_valid_feedback("778888"))  # Too long
        self.assertFalse(self.business_logic._is_valid_feedback(None))  # None input

    def test_convert_to_color_code(self):
        """Test color code conversion.
        
        Verifies that numeric inputs are correctly converted to ColorCode
        enum values and invalid inputs raise appropriate exceptions.
        """
        # Valid conversions
        self.assertEqual(self.business_logic._convert_to_color_code(1), ColorCode(1))
        self.assertEqual(self.business_logic._convert_to_color_code(8), ColorCode(8))
        
        # Invalid conversion
        with self.assertRaises(ValueError):
            self.business_logic._convert_to_color_code(9)  # Out of range

    def test_handle_feedback_input(self):
        """Test feedback input handling.
        
        Verifies that feedback input is properly validated and converted
        before being passed to the game logic.
        """
        # Setup game state
        self.game_logic.startgame("guesser")
        self.game_logic.make_guess([ColorCode(1) for _ in range(5)])
        
        # Valid feedback
        result = self.business_logic.handle_feedback_input("88")
        self.assertIn(result, ["need_guess_input", "game_over"])
        
        # Invalid feedback
        result = self.business_logic.handle_feedback_input("99")
        self.assertEqual(result, "need_feedback_input")


if __name__ == '__main__':
    unittest.main()