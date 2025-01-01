import unittest
from src.GameLogic.Guesser.player_guesser import PlayerGuesser
from src.util.color_code import ColorCode


class test_player_guesser(unittest.TestCase):
    """Test suite for the PlayerGuesser class.

    This test suite verifies the functionality of the PlayerGuesser class,
    which implements the IGuesser interface and represents a human player
    making guesses in the game.
    """

    def setUp(self):
        """Set up test fixtures before each test method.

        Creates a new PlayerGuesser instance for testing.
        """
        self.guesser = PlayerGuesser()

    def test_initialization(self):
        """Test initialization of PlayerGuesser.

        Verifies that a new PlayerGuesser instance is created correctly
        with an empty guess list.
        """
        self.assertIsInstance(self.guesser, PlayerGuesser)
        self.assertEqual(self.guesser.current_guess, [])

    def test_make_guess_empty(self):
        """Test make_guess with no guess set.

        Verifies that make_guess returns an empty list when no guess has been set.
        """
        result = self.guesser.make_guess()
        self.assertEqual(result, [])

    def test_set_and_make_guess(self):
        """Test setting and retrieving a guess.

        Verifies that a guess can be set and retrieved correctly.
        """
        test_guess = [ColorCode(1), ColorCode(2), ColorCode(3)]
        self.guesser.set_guess(test_guess)
        result = self.guesser.make_guess()
        self.assertEqual(result, test_guess)

    def test_set_guess_multiple_times(self):
        """Test setting multiple guesses.

        Verifies that set_guess can be called multiple times
        and always returns the latest guess.
        """
        first_guess = [ColorCode(1), ColorCode(2)]
        second_guess = [ColorCode(3), ColorCode(4)]

        self.guesser.set_guess(first_guess)
        self.assertEqual(self.guesser.make_guess(), first_guess)

        self.guesser.set_guess(second_guess)
        self.assertEqual(self.guesser.make_guess(), second_guess)


if __name__ == "__main__":
    unittest.main()
