"""Test module for PersistenceManager."""

import unittest
import os
import pickle
from src.persistence.persistence_manager import PersistenceManager
from src.business_logic.game_state import GameState
from src.business_logic.game_turn import GameTurn
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class TestPersistenceManager(unittest.TestCase):
    """Test cases for PersistenceManager."""

    def setUp(self: 'TestPersistenceManager') -> None:
        """Set up test fixtures before each test method."""
        self.persistence_manager = PersistenceManager()
        self.test_file = "test_save.pkl"

        # Create test game state with required secret_code
        self.game_state = GameState(
            secret_code=[ColorCode.RED, ColorCode.BLUE,
                         ColorCode.GREEN, ColorCode.YELLOW],  # Required parameter
            positions=4,
            colors=6,
            max_rounds=12,
            player_name="TestPlayer"
        )

        # Add test turns
        turn = GameTurn(
            guesses=[ColorCode.RED, ColorCode.BLUE,
                     ColorCode.GREEN, ColorCode.YELLOW],
            feedback=[FeedbackColorCode.BLACK, FeedbackColorCode.WHITE]
        )
        self.game_state.add_turn(turn)

    def tearDown(self: 'TestPersistenceManager') -> None:
        """Clean up after each test method."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_game_state(self: 'TestPersistenceManager') -> None:
        """Test saving and loading game state."""
        # Get full path in saves directory
        file_path = os.path.join(self.persistence_manager.save_dir, self.test_file)

        # Ensure saves directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save game state
        self.persistence_manager.save_game_state(self.game_state, self.test_file)
        self.assertTrue(os.path.exists(file_path))  # Check correct path

        # Load and verify
        loaded_state = self.persistence_manager.load_game_state(self.test_file)
        self.assertEqual(loaded_state.positions, self.game_state.positions)
        self.assertEqual(loaded_state.colors, self.game_state.colors)
        self.assertEqual(loaded_state.max_rounds, self.game_state.max_rounds)
        self.assertEqual(loaded_state.player_name, self.game_state.player_name)
        self.assertEqual(loaded_state.secret_code, self.game_state.secret_code)

        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_has_saved_game(self: 'TestPersistenceManager') -> None:
        """Test checking for saved game existence."""
        # Get full path to default save file
        default_save = os.path.join(self.persistence_manager.save_dir, "game_state.pkl")

        # Initially no save should exist
        if os.path.exists(default_save):
            os.remove(default_save)
        self.assertFalse(self.persistence_manager.has_saved_game())

        # After saving, should return true
        self.persistence_manager.save_game_state(self.game_state)
        self.assertTrue(self.persistence_manager.has_saved_game())

        # Cleanup
        if os.path.exists(default_save):
            os.remove(default_save)

    def test_load_non_existent_file(self: 'TestPersistenceManager') -> None:
        """Test loading from non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.persistence_manager.load_game_state("non_existent.pkl")

    def test_save_invalid_game_state(self: 'TestPersistenceManager') -> None:
        """Test saving invalid game state."""
        with self.assertRaises(TypeError):
            self.persistence_manager.save_game_state("not a game state")

    def test_load_corrupted_file(self: 'TestPersistenceManager') -> None:
        """Test loading corrupted save file."""
        # Create corrupted file in the saves directory
        file_path = os.path.join(self.persistence_manager.save_dir, self.test_file)

        # Ensure saves directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write corrupted data
        with open(file_path, "wb") as file:
            file.write(b"corrupted data")

        # Test loading corrupted file
        with self.assertRaises(pickle.UnpicklingError):
            self.persistence_manager.load_game_state(self.test_file)

        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    unittest.main()
