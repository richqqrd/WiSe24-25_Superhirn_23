import unittest
from src.GameLogic.GameState import GameState
from src.GameLogic.GameTurn import GameTurn
from src.util.ColorCode import ColorCode
from src.GameLogic.Guesser.PlayerGuesser import PlayerGuesser
from src.GameLogic.Guesser.ComputerGuesser import ComputerGuesser


class test_game_state(unittest.TestCase):
    """Test suite for the GameState class.

    This test suite verifies the functionality of the GameState class,
    which manages the game state including secret code, turns, and
    maximum rounds allowed.
    """

    def setUp(self):
        """Set up test fixtures before each test method.

        Creates a new GameState instance with test data including
        a secret code and maximum rounds.
        """
        self.secret_code = [
            ColorCode.RED,
            ColorCode.BLUE,
            ColorCode.GREEN,
            ColorCode.YELLOW,
        ]
        self.max_rounds = 10
        self.player_guesser = PlayerGuesser()
        self.game_state = GameState(
            self.secret_code, self.max_rounds, self.player_guesser
        )

    def test_initialization(self):
        """Test the initialization of GameState.

        Verifies that a new GameState instance is correctly initialized
        with the provided secret code, max rounds, and empty turns list.
        """
        self.assertEqual(self.game_state.secret_code, self.secret_code)
        self.assertEqual(self.game_state.max_rounds, self.max_rounds)
        self.assertEqual(self.game_state.turns, [])
        self.assertEqual(self.game_state.current_guesser, self.player_guesser)

    def test_add_turn(self):
        """Test adding a turn to the game state.

        Verifies that turns can be successfully added to the game state
        and are correctly stored.
        """
        turn = GameTurn(guesses=[ColorCode.RED], feedback=[])
        self.game_state.add_turn(turn)
        self.assertEqual(len(self.game_state.turns), 1)
        self.assertEqual(self.game_state.turns[0], turn)

    def test_add_turn_max_rounds(self):
        """Test adding a turn when max rounds are reached.

        Verifies that attempting to add a turn beyond the maximum
        number of rounds raises a ValueError.
        """
        for _ in range(self.max_rounds):
            self.game_state.add_turn(GameTurn(guesses=[ColorCode.RED], feedback=[]))
        with self.assertRaises(ValueError):
            self.game_state.add_turn(GameTurn(guesses=[ColorCode.RED], feedback=[]))

    def test_get_secret_code(self):
        """Test getting the secret code.

        Verifies that the get_secret_code method returns the correct
        secret code that was set during initialization.
        """
        self.assertEqual(self.game_state.get_secret_code(), self.secret_code)

    def test_get_turns(self):
        """Test getting the list of turns.

        Verifies that the get_turns method returns the correct list
        of turns that have been added to the game state.
        """
        turn = GameTurn(guesses=[ColorCode.RED], feedback=[])
        self.game_state.add_turn(turn)
        self.assertEqual(self.game_state.get_turns(), [turn])

    def test_repr(self):
        """Test the string representation of the game state.

        Verifies that the string representation of GameState contains
        all relevant information in the expected format.
        """
        expected_repr = (f"GameState(secret_code={self.secret_code}, "
                         f"turns=[], max_rounds={self.max_rounds})")
        self.assertEqual(repr(self.game_state), expected_repr)

    def test_initialization_with_computer_guesser(self):
        """Test initialization with computer guesser.

        Verifies that GameState can be initialized with a computer guesser
        and correctly stores the guesser reference.
        """
        computer_guesser = ComputerGuesser()
        game_state = GameState(self.secret_code, self.max_rounds, computer_guesser)
        self.assertEqual(game_state.current_guesser, computer_guesser)


if __name__ == "__main__":
    unittest.main()
