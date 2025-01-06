"""End-to-end tests for the mastermind game."""
import unittest
import os
from unittest.mock import Mock

from src.persistence.persistence_manager import PersistenceManager
from src.business_logic.business_logic import BusinessLogic
from src.application_logic.application_logic import ApplicationLogic
from src.cli.console import Console


class TestEndToEnd(unittest.TestCase):
    """End-to-end test suite."""

    def test_complete_game_flow_as_guesser(self):
        """Test complete game flow from start to finish as guesser."""
        # Setup real components
        persistence_manager = PersistenceManager()
        business_logic = BusinessLogic(persistence_manager)
        app_logic = ApplicationLogic(business_logic)
        console = Console(app_logic)

        # Mock user input
        console.input_handler.handle_user_input = Mock()
        console.input_handler.handle_user_input.side_effect = [
            "1",  # Choose guesser mode
            "Player1",  # Player name
            "4",  # Positions
            "6",  # Colors
            "10",  # Max attempts
            "1234",  # First guess
            "menu",  # Open menu
            "1",  # Save game
            "1",  # Confirm save with "Yes"
            "5666",  # Another guess
            "menu",  # Open menu again
            "4",  # End game
        ]

        # Run game flow
        console.handle_game_mode_choice()  # This starts the game loop internally

        # Verify final state
        game_state = app_logic.get_game_state()
        self.assertIsNotNone(game_state)
        self.assertEqual(game_state.player_name, "Player1")
        self.assertEqual(len(game_state.get_turns()), 2)  # Two guesses made

        # Cleanup
        if os.path.exists(os.path.join(persistence_manager.save_dir, "game_state.pkl")):
            os.remove(os.path.join(persistence_manager.save_dir, "game_state.pkl"))

    def test_complete_game_flow_as_coder(self):
        """Test complete game flow from start to finish as coder."""
        # Setup real components
        persistence_manager = PersistenceManager()
        business_logic = BusinessLogic(persistence_manager)
        app_logic = ApplicationLogic(business_logic)
        console = Console(app_logic)

        # Mock user input
        console.input_handler.handle_user_input = Mock()
        console.input_handler.handle_user_input.side_effect = [
            "2",  # Choose coder mode
            "Player1",  # Name
            "4",  # Positions
            "1",  # Colors
            "10",  # Max attempts
            "1111",  # Secret code # Menu
            "8888",  # Feedback for computer's guess
        ]

        # Run game flow
        console.handle_game_mode_choice()  # This starts the game loop internally

        # Verify final state
        game_state = app_logic.get_game_state()
        self.assertIsNotNone(game_state)
        self.assertEqual(game_state.player_name, "Player1")
        self.assertEqual(len(game_state.get_turns()), 1)  # Two guesses made

        # Cleanup
        if os.path.exists(os.path.join(persistence_manager.save_dir, "game_state.pkl")):
            os.remove(os.path.join(persistence_manager.save_dir, "game_state.pkl"))

    def test_complete_game_flow_with_win(self):
        """Test complete game flow ending with player win."""
        persistence_manager = PersistenceManager()
        business_logic = BusinessLogic(persistence_manager)
        app_logic = ApplicationLogic(business_logic)
        console = Console(app_logic)

        console.input_handler.handle_user_input = Mock()
        console.input_handler.handle_user_input.side_effect = [
            "1",  # Guesser mode
            "Player1",  # Name
            "4",  # Positions
            "6",  # Colors
            "10",  # Attempts
            "1234",  # Winning guess
            "menu",  # Menu
            "4"  # End game
        ]

        console.handle_game_mode_choice()

        game_state = app_logic.get_game_state()
        self.assertEqual(len(game_state.get_turns()), 1)

        self.assertTrue(app_logic.is_game_over("game_won"))

    def test_complete_game_flow_with_save_and_load(self):
        """Test game flow with save/load functionality."""
        persistence_manager = PersistenceManager()
        business_logic = BusinessLogic(persistence_manager)
        app_logic = ApplicationLogic(business_logic)
        console = Console(app_logic)

        # First session - save game
        console.input_handler.handle_user_input = Mock()
        console.input_handler.handle_user_input.side_effect = [
            "1",  # Mode
            "Player1",  # Name
            "4",  # Positions
            "8",  # Colors
            "10",  # Attempts
            "1111",  # Guess
            "menu",  # Menu
            "1",
            "1",  # Save
            "menu",
            "3",
            "11111",
            "1111",
            "menu",
            "4"  # End
        ]

        console.handle_game_mode_choice()

        game_state = app_logic.get_game_state()
        print(game_state)
        self.assertEqual(len(game_state.get_turns()), 2)

        if os.path.exists(os.path.join(persistence_manager.save_dir, "game_state.pkl")):
            os.remove(os.path.join(persistence_manager.save_dir, "game_state.pkl"))
