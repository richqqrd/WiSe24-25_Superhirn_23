# tests/GameLogic/test_game_state.py
import unittest
from src.GameLogic.GameState import GameState
from src.util.ColorCode import ColorCode
from src.GameLogic.GameTurn import GameTurn


class TestGameState(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.secret_code = [ColorCode.RED, ColorCode.BLUE, ColorCode.GREEN, ColorCode.YELLOW]
        self.max_rounds = 10
        self.game_state = GameState(self.secret_code, self.max_rounds)

    def test_initialization(self):
        """Test the initialization of GameState."""
        self.assertEqual(self.game_state.secret_code, self.secret_code)
        self.assertEqual(self.game_state.max_rounds, self.max_rounds)
        self.assertEqual(self.game_state.turns, [])

    def test_add_turn(self):
        """Test adding a turn to the game state."""
        turn = GameTurn(guesses=[ColorCode.RED], feedback=[])
        self.game_state.add_turn(turn)
        self.assertEqual(len(self.game_state.turns), 1)
        self.assertEqual(self.game_state.turns[0], turn)

    def test_add_turn_max_rounds(self):
        """Test adding a turn when max rounds are reached."""
        for _ in range(self.max_rounds):
            self.game_state.add_turn(GameTurn(guesses=[ColorCode.RED], feedback=[]))
        with self.assertRaises(ValueError):
            self.game_state.add_turn(GameTurn(guesses=[ColorCode.RED], feedback=[]))

    def test_get_secret_code(self):
        """Test getting the secret code."""
        self.assertEqual(self.game_state.get_secret_code(), self.secret_code)

    def test_get_turns(self):
        """Test getting the list of turns."""
        turn = GameTurn(guesses=[ColorCode.RED], feedback=[])
        self.game_state.add_turn(turn)
        self.assertEqual(self.game_state.get_turns(), [turn])

    def test_repr(self):
        """Test the string representation of the game state."""
        expected_repr = f"GameState(secret_code={self.secret_code}, turns=[], max_rounds={self.max_rounds})"
        self.assertEqual(repr(self.game_state), expected_repr)


if __name__ == "__main__":
    unittest.main()