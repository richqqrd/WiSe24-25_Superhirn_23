import unittest
import os
import pickle

from src.GameLogic.GameTurn import GameTurn
from src.Persistence.PersistenceManager import PersistenceManager
from src.GameLogic.GameState import GameState
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode

class TestPersistenceManager(unittest.TestCase):
    def setUp(self):
        self.persistence_manager = PersistenceManager()
        self.test_file = "test_game_state.pkl"
        self.game_state = GameState(
            secret_code=[ColorCode.RED, ColorCode.BLUE, ColorCode.GREEN, ColorCode.YELLOW, ColorCode.ORANGE],
            max_rounds=12,
            positions=5,
            colors=8,
            player_name="player1",
            current_guesser=None
        )
        self.game_state.add_turn(GameTurn(
            guesses=[ColorCode.RED, ColorCode.BLUE, ColorCode.GREEN, ColorCode.YELLOW, ColorCode.ORANGE],
            feedback=[FeedbackColorCode.BLACK, FeedbackColorCode.BLACK, FeedbackColorCode.WHITE]
        ))
        self.game_state.add_turn(GameTurn(
            guesses=[ColorCode.RED, ColorCode.BLUE, ColorCode.GREEN, ColorCode.YELLOW, ColorCode.ORANGE],
            feedback=[FeedbackColorCode.BLACK, FeedbackColorCode.BLACK, FeedbackColorCode.WHITE]
        ))

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_game_state(self):
        self.persistence_manager.save_game_state(self.game_state, self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

        with open(self.test_file, "rb") as file:
            loaded_game_state = pickle.load(file)
            self.assertEqual(loaded_game_state.secret_code, self.game_state.secret_code)
            self.assertEqual(loaded_game_state.max_rounds, self.game_state.max_rounds)
            self.assertEqual(loaded_game_state.positions, self.game_state.positions)
            self.assertEqual(loaded_game_state.colors, self.game_state.colors)
            self.assertEqual(loaded_game_state.player_name, self.game_state.player_name)
            self.assertEqual(len(loaded_game_state.turns), len(self.game_state.turns))
            self.assertEqual(loaded_game_state.turns[0].guesses, self.game_state.turns[0].guesses)
            self.assertEqual(loaded_game_state.turns[0].feedback, self.game_state.turns[0].feedback)
            self.assertEqual(loaded_game_state.turns[1].guesses, self.game_state.turns[1].guesses)
            self.assertEqual(loaded_game_state.turns[1].feedback, self.game_state.turns[1].feedback)

    def test_load_game_state(self):
        with open(self.test_file, "wb") as file:
            pickle.dump(self.game_state, file)

        loaded_game_state = self.persistence_manager.load_game_state(self.test_file)
        self.assertEqual(loaded_game_state.secret_code, self.game_state.secret_code)
        self.assertEqual(loaded_game_state.max_rounds, self.game_state.max_rounds)
        self.assertEqual(loaded_game_state.positions, self.game_state.positions)
        self.assertEqual(loaded_game_state.colors, self.game_state.colors)
        self.assertEqual(loaded_game_state.player_name, self.game_state.player_name)
        self.assertEqual(len(loaded_game_state.turns), len(self.game_state.turns))
        self.assertEqual(loaded_game_state.turns[0].guesses, self.game_state.turns[0].guesses)
        self.assertEqual(loaded_game_state.turns[0].feedback, self.game_state.turns[0].feedback)
        self.assertEqual(loaded_game_state.turns[1].guesses, self.game_state.turns[1].guesses)
        self.assertEqual(loaded_game_state.turns[1].feedback, self.game_state.turns[1].feedback)

    def test_load_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            self.persistence_manager.load_game_state("non_existent_file.pkl")

    def test_save_invalid_data(self):
        with self.assertRaises(TypeError):
            self.persistence_manager.save_game_state("invalid_data", self.test_file)

    def test_load_invalid_data(self):
        with open(self.test_file, "wb") as file:
            file.write(b"invalid_data")

        with self.assertRaises(pickle.UnpicklingError):
            self.persistence_manager.load_game_state(self.test_file)

if __name__ == "__main__":
    unittest.main()