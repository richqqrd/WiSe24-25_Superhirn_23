"""Test module for GameState class."""

import unittest
from src.business_logic.game_state import GameState
from src.business_logic.game_turn import GameTurn
from src.util.color_code import ColorCode
from src.business_logic.guesser.player_guesser import PlayerGuesser
from src.business_logic.guesser.computer_guesser import ComputerGuesser


class TestGameState(unittest.TestCase):
    """Test suite for the GameState class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.positions = 4
        self.colors = 6
        self.secret_code = [
            ColorCode.RED,
            ColorCode.BLUE,
            ColorCode.GREEN,
            ColorCode.YELLOW,
        ]
        self.max_rounds = 10
        self.player_name = "TestPlayer"
        self.player_guesser = PlayerGuesser()
        self.game_state = GameState(
            secret_code=self.secret_code,
            max_rounds=self.max_rounds,
            positions=self.positions,
            colors=self.colors,
            player_name=self.player_name,
            current_guesser=self.player_guesser
        )

    def test_initialization(self):
        """Test initialization of GameState."""
        self.assertEqual(self.game_state.secret_code, self.secret_code)
        self.assertEqual(self.game_state.max_rounds, self.max_rounds)
        self.assertEqual(self.game_state.positions, self.positions)
        self.assertEqual(self.game_state.colors, self.colors)
        self.assertEqual(self.game_state.player_name, self.player_name)
        self.assertEqual(self.game_state.current_guesser, self.player_guesser)
        self.assertEqual(self.game_state.turns, [])

    def test_add_turn(self):
        """Test adding a turn."""
        turn = GameTurn(
            guesses=[ColorCode.RED, ColorCode.BLUE, ColorCode.GREEN, ColorCode.YELLOW],  # 4 Positionen
            feedback=[]
        )
        self.game_state.add_turn(turn)
        self.assertEqual(len(self.game_state.turns), 1)
        self.assertEqual(self.game_state.turns[0], turn)

    def test_add_turn_max_rounds(self):
        """Test adding turn when max rounds reached."""
        turn = GameTurn(
            guesses=[ColorCode.RED, ColorCode.BLUE, ColorCode.GREEN, ColorCode.YELLOW],  # 4 Positionen
            feedback=[]
        )
        for _ in range(self.max_rounds):
            self.game_state.add_turn(turn)

        with self.assertRaises(ValueError):
            self.game_state.add_turn(turn)

    def test_add_turn_invalid_positions(self):
        """Test adding turn with wrong number of positions."""
        turn = GameTurn(
            guesses=[ColorCode.RED],  # Only one position
            feedback=[]
        )
        with self.assertRaises(ValueError):
            self.game_state.add_turn(turn)

    def test_get_secret_code(self):
        """Test getting secret code."""
        self.assertEqual(self.game_state.get_secret_code(), self.secret_code)

    def test_get_turns(self):
        """Test getting turns list."""
        turn1 = GameTurn(
            guesses=[ColorCode.RED, ColorCode.BLUE, ColorCode.GREEN, ColorCode.YELLOW],  # 4 Positionen
            feedback=[]
        )
        turn2 = GameTurn(
            guesses=[ColorCode.GREEN, ColorCode.YELLOW, ColorCode.RED, ColorCode.BLUE],  # 4 Positionen
            feedback=[]
        )
        self.game_state.add_turn(turn1)
        self.game_state.add_turn(turn2)
        self.assertEqual(self.game_state.get_turns(), [turn1, turn2])

    def test_initialization_with_computer_guesser(self):
        """Test initialization with computer guesser."""
        computer_guesser = ComputerGuesser(self.positions, self.colors)
        game_state = GameState(
            secret_code=self.secret_code,
            max_rounds=self.max_rounds,
            positions=self.positions,
            colors=self.colors,
            player_name=self.player_name,
            current_guesser=computer_guesser
        )
        self.assertEqual(game_state.current_guesser, computer_guesser)

    def test_repr(self):
        """Test string representation."""
        expected = (
            f"GameState(secret_code={self.secret_code}, "
            f"turns={self.game_state.turns}, "
            f"max_rounds={self.max_rounds})"
        )
        self.assertEqual(repr(self.game_state), expected)


if __name__ == "__main__":
    unittest.main()