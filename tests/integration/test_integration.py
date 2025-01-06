"""Integration tests for the mastermind game."""
import os
import unittest
from unittest.mock import Mock

from src.application_logic.application_logic import ApplicationLogic
from src.business_logic.business_logic import BusinessLogic
from src.cli.console import Console
from src.persistence.i_persistence_manager import IPersistenceManager
from src.persistence.persistence_manager import PersistenceManager
from src.util.color_code import ColorCode


class TestIntegration(unittest.TestCase):
    """Integration test suite."""

    def test_business_application_integration(self):
        """Test BusinessLogic and ApplicationLogic integration."""
        # Setup
        mock_persistence_manager = Mock(spec=IPersistenceManager)
        business_logic = BusinessLogic(mock_persistence_manager)
        app_logic = ApplicationLogic(business_logic)

        # Test complete game flow
        app_logic.handle_game_configuration("Player1", "4", "6", "10")
        business_logic.startgame("guesser")  # Start the game first

        # Now make a guess
        result = app_logic.process_game_action("need_guess_input", "1234")
        self.assertIn(result, ["need_guess_input", "game_over"])

    def test_network_business_integration(self):
        """Test NetworkService and BusinessLogic integration."""
        mock_persistence_manager = Mock(spec=IPersistenceManager)
        business_logic = BusinessLogic(mock_persistence_manager)

        # Test online game flow
        business_logic.startgame("online_guesser")
        business_logic.start_as_online_guesser("localhost", 8080)
        result = business_logic.make_guess([ColorCode(1)] * 4)
        self.assertIn(result, ["need_guess_input", "error"])

    def test_persistence_business_integration(self):
        """Test PersistenceManager and BusinessLogic integration."""
        persistence_manager = PersistenceManager()  # Real persistence manager
        business_logic = BusinessLogic(persistence_manager)

        # Setup initial game
        business_logic.configure_game("Player1", 4, 6, 10)
        business_logic.startgame("guesser")

        # Make some moves to create game state
        guess = [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4)]
        business_logic.make_guess(guess)
        initial_state = business_logic.get_game_state()

        # Save game
        business_logic.save_game_state()

        # Verify save exists
        self.assertTrue(business_logic.has_saved_game())

        # Create new business logic instance
        new_business_logic = BusinessLogic(persistence_manager)

        # Load game in new instance
        new_business_logic.load_game_state()
        loaded_state = new_business_logic.get_game_state()

        # Verify loaded state matches original
        self.assertEqual(loaded_state.player_name, initial_state.player_name)
        self.assertEqual(loaded_state.positions, initial_state.positions)
        self.assertEqual(loaded_state.colors, initial_state.colors)
        self.assertEqual(len(loaded_state.get_turns()), len(initial_state.get_turns()))
        self.assertEqual(loaded_state.get_turns()[0].guesses, guess)

        # Cleanup
        if os.path.exists(os.path.join(persistence_manager.save_dir, "game_state.pkl")):
            os.remove(os.path.join(persistence_manager.save_dir, "game_state.pkl"))

    def test_cli_application_integration(self):
        """Test basic CLI and ApplicationLogic integration."""
        # Setup
        mock_persistence_manager = Mock(spec=IPersistenceManager)
        business_logic = BusinessLogic(mock_persistence_manager)
        app_logic = ApplicationLogic(business_logic)
        console = Console(app_logic)

        # Mock user input
        console.input_handler.handle_user_input = Mock()

        # Mock minimal game setup
        business_logic.configure_game("Player1", 4, 6, 10)
        business_logic.startgame("guesser")

        # Mock user input for guess
        console.input_handler.handle_user_input.return_value = "1234"

        # Test game action processing through getting user input
        user_input = console.get_user_input("need_guess_input")
        result = app_logic.process_game_action("need_guess_input", user_input)

        # Verify that:
        # 1. Console correctly got user input
        console.input_handler.handle_user_input.assert_called_once()

        # 2. Input was processed through application logic
        # 3. Result was returned back through the chain
        self.assertIn(result, ["need_guess_input", "game_won", "game_lost"])
