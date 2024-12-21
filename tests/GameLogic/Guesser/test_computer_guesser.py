import unittest
from src.GameLogic.Guesser.ComputerGuesser import ComputerGuesser
from src.util.ColorCode import ColorCode


class test_computer_guesser(unittest.TestCase):
    """Test suite for the ComputerGuesser class.

    This test suite verifies the functionality of the ComputerGuesser class,
    which implements the IGuesser interface and represents the computer's
    guessing strategy in the game.
    """

    def setUp(self):
        """Set up test fixtures before each test method.

        Creates a new ComputerGuesser instance for testing.
        """
        self.guesser = ComputerGuesser()

    def test_make_guess_length(self):
        """Test that make_guess returns correct length.

        Verifies that the computer's guess is always 5 colors long,
        which is the standard length for a Mastermind code.
        """
        guess = self.guesser.make_guess()
        self.assertEqual(len(guess), 5)

    def test_make_guess_valid_colors(self):
        """Test that make_guess returns valid colors.

        Verifies that each color in the computer's guess is a valid
        ColorCode instance with a value between 1 and 8.
        """
        guess = self.guesser.make_guess()
        for color in guess:
            self.assertIsInstance(color, ColorCode)
            self.assertTrue(1 <= color.value <= 8)

    def test_make_guess_randomness(self):
        """Test that make_guess generates different guesses.

        Verifies that multiple calls to make_guess don't always return
        the same sequence, ensuring some randomness in the guessing.
        """
        guesses = [self.guesser.make_guess() for _ in range(5)]
        # Convert guesses to tuples of values for comparison
        guess_values = [tuple(color.value for color in guess) for guess in guesses]
        # Check if all guesses are the same
        all_same = all(guess == guess_values[0] for guess in guess_values)
        self.assertFalse(all_same, "All guesses were identical")

    def test_make_guess_multiple_calls(self):
        """Test that make_guess can be called multiple times.

        Verifies that the method can be called repeatedly without
        errors or state-related issues.
        """
        for _ in range(10):
            guess = self.guesser.make_guess()
            self.assertEqual(len(guess), 5)
            for color in guess:
                self.assertIsInstance(color, ColorCode)


if __name__ == '__main__':
    unittest.main()