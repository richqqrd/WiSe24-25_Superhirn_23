import unittest
from src.business_logic.business_logic import BusinessLogic
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode
from src.business_logic.game_turn import GameTurn


class TestBusinessLogic(unittest.TestCase):
    """Test suite for the business_logic class.

    This class tests the core game logic functionality including game initialization,
    making guesses, handling feedback, and determining game end conditions.
    """

    def setUp(self):
        """Set up test fixtures before each test method.

        Initializes a fresh business_logic instance and necessary mock objects
        for testing game state transitions.
        """
        self.game_logic = BusinessLogic()

    def test_startgame_as_guesser(self):
        """Test game initialization when player is guesser.

        Verifies that the game state is properly initialized and returns
        the correct state for player as guesser.
        """
        result = self.game_logic.startgame("guesser")
        self.assertEqual(result, "need_guess_input")
        self.assertIsNotNone(self.game_logic.game_state)
        self.assertEqual(len(self.game_logic.game_state.secret_code), 5)

    def test_startgame_as_coder(self):
        """Test game initialization when player is coder.

        Verifies that the game returns the correct state for player as coder.
        """
        result = self.game_logic.startgame("coder")
        self.assertEqual(result, "need_code_input")

    def test_make_guess_valid(self):
        """Test making a valid guess.

        Verifies that a valid guess is properly processed and feedback is generated.
        """
        self.game_logic.startgame("guesser")
        guess = ["1", "2", "3", "4", "5"]  # Strings statt ColorCode Objekte
        result = self.game_logic.make_guess(guess)
        self.assertIn(result, ["need_guess_input", "game_over"])
        self.assertEqual(len(self.game_logic.game_state.get_turns()), 1)

    def test_make_guess_invalid(self):
        """Test making an invalid guess.

        Verifies that invalid guesses are properly handled and error state is returned.
        """
        self.game_logic.startgame("guesser")
        result = self.game_logic.make_guess(
            ["invalid"]
        )  # Ungültiger Input statt leere Liste
        self.assertEqual(result, "need_guess_input")

    def test_set_secret_code_valid(self):
        """Test setting a valid secret code.

        Verifies that a valid secret code is properly set and game state transitions.
        """
        code = [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4), ColorCode(5)]
        result = self.game_logic.set_secret_code(code)
        self.assertEqual(result, "wait_for_computer_guess")
        self.assertEqual(self.game_logic.game_state.secret_code, code)

    def test_is_game_over_win(self):
        """Test game over condition when player wins.

        Verifies that the game correctly identifies a winning condition.
        """
        self.game_logic.startgame("guesser")
        feedback = [FeedbackColorCode.BLACK] * 5
        result = self.game_logic.is_game_over(feedback)
        self.assertEqual(result, "game_over")

    def test_is_game_over_max_rounds(self):
        """Test game over condition when max rounds reached.

        Verifies that the game ends when maximum rounds are reached.
        """
        self.game_logic.startgame("guesser")
        for _ in range(self.game_logic.max_round):
            turn = GameTurn([ColorCode(1)], [FeedbackColorCode.WHITE])
            self.game_logic.game_state.add_turn(turn)

        result = self.game_logic.is_game_over([FeedbackColorCode.WHITE])
        self.assertEqual(result, "game_over")


if __name__ == "__main__":
    unittest.main()
