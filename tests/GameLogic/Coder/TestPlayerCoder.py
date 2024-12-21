import unittest
from src.GameLogic.Coder.PlayerCoder import PlayerCoder
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class TestPlayerCoder(unittest.TestCase):
    """Test cases for the PlayerCoder class.

    This test suite verifies the functionality of the PlayerCoder class,
    which implements the ICoder interface and represents a human player
    acting as the code maker.
    """

    def setUp(self):
        """Set up test fixtures before each test method.

        Creates a new PlayerCoder instance for each test.
        """
        self.coder = PlayerCoder()

    def test_init(self):
        """Test initialization of PlayerCoder.

        Verifies that a new PlayerCoder instance has an empty code list.
        """
        self.assertEqual(self.coder.code, [])

    def test_generate_code_empty(self):
        """Test generate_code with empty code list.

        Verifies that generate_code raises ValueError when no code is set.
        """
        with self.assertRaises(ValueError):
            self.coder.generate_code()

    def test_generate_code_with_code(self):
        """Test generate_code with preset code.

        Verifies that generate_code returns the previously set code.
        """
        test_code = [ColorCode(1), ColorCode(2), ColorCode(3)]
        self.coder.code = test_code
        result = self.coder.generate_code()
        self.assertEqual(result, test_code)

    def test_give_feedback_not_implemented(self):
        """Test give_feedback method.

        Verifies that give_feedback returns None as it's not implemented yet.
        """
        result = self.coder.give_feedback()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()