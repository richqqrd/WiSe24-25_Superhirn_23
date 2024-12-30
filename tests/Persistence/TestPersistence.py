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
            max_rounds=12
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

    def test_load_game_state(self):
        with open(self.test_file, "wb") as file:
            pickle.dump(self.game_state, file)

        loaded_game_state = self.persistence_manager.load_game_state(self.test_file)
        self.assertEqual(loaded_game_state.secret_code, self.game_state.secret_code)
        self.assertEqual(loaded_game_state.max_rounds, self.game_state.max_rounds)

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