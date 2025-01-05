"""Test module for ApplicationLogic."""
import unittest
from unittest.mock import Mock, patch
from src.application_logic.application_logic import ApplicationLogic
from src.business_logic.business_logic import BusinessLogic
from src.business_logic.game_turn import GameTurn
from src.business_logic.guesser.player_guesser import PlayerGuesser
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode
from src.persistence.i_persistence_manager import IPersistenceManager


class TestApplicationLogic(unittest.TestCase):
    """Test suite for the ApplicationLogic class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock the persistence manager
        mock_persistence_manager = Mock(spec=IPersistenceManager)
        self.game_logic = BusinessLogic(mock_persistence_manager)
        self.app_logic = ApplicationLogic(self.game_logic)
        self.game_logic.positions = 4
        self.game_logic.colors = 6

    def test_is_valid_code(self):
        """Test code validation."""
        # Valid cases
        self.assertTrue(self.app_logic._is_valid_code("1234"))
        self.assertTrue(self.app_logic._is_valid_code("6543"))

        # Invalid cases
        self.assertFalse(self.app_logic._is_valid_code("123"))  # Too short
        self.assertFalse(self.app_logic._is_valid_code("12345"))  # Too long
        self.assertFalse(self.app_logic._is_valid_code("123A"))  # Invalid char
        self.assertFalse(self.app_logic._is_valid_code(""))  # Empty
        self.assertFalse(self.app_logic._is_valid_code("0123"))  # Invalid number
        self.assertFalse(self.app_logic._is_valid_code("7890"))  # Out of range

    def test_is_valid_feedback(self):
        """Test feedback validation."""
        # Valid cases
        self.assertTrue(self.app_logic._is_valid_feedback("78"))
        self.assertTrue(self.app_logic._is_valid_feedback("8877"))
        self.assertTrue(self.app_logic._is_valid_feedback(""))

        # Invalid cases
        self.assertFalse(self.app_logic._is_valid_feedback("789"))  # Invalid number
        self.assertFalse(self.app_logic._is_valid_feedback("12"))  # Invalid feedback
        self.assertFalse(self.app_logic._is_valid_feedback("A8"))  # Invalid char

    def test_convert_to_color_code(self):
        """Test color code conversion."""
        # Single valid conversion
        self.assertEqual(self.app_logic._convert_to_color_code(1), ColorCode.RED)
        self.assertEqual(self.app_logic._convert_to_color_code(2), ColorCode.GREEN)
        self.assertEqual(self.app_logic._convert_to_color_code(4), ColorCode.BLUE)

        # Invalid input raises ValueError
        with self.assertRaises(ValueError):
            self.app_logic._convert_to_color_code(9)  # Out of range

    def test_handle_code_input(self):
        """Test code input handling."""
        # Valid input
        self.assertEqual(self.app_logic.handle_code_input("1234"), "wait_for_computer_guess")

        # Invalid input
        self.assertEqual(self.app_logic.handle_code_input("123"), "need_code_input")
        self.assertEqual(self.app_logic.handle_code_input("ABCD"), "need_code_input")
        self.assertEqual(self.app_logic.handle_code_input(""), "need_code_input")


    def test_handle_guess_input(self):
        """Test guess input handling."""
        # Configure game first
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)

        # Then start game
        self.game_logic.startgame("guesser")

        # Valid guess
        result = self.app_logic.handle_guess_input("1234")
        self.assertIn(result, ["need_guess_input", "game_over"])

        # Invalid guess
        result = self.app_logic.handle_guess_input("invalid")
        self.assertEqual(result, "need_guess_input")

    def test_handle_feedback_input_conversion(self):
        """Test feedback string to enum conversion in handle_feedback_input."""
        # Setup game state first
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)
        self.game_logic.make_computer_guess()

        # Test conversion through handle_feedback_input
        result = self.app_logic.handle_feedback_input("78")
        self.assertNotEqual(result, "need_feedback_input")  # Valid conversion

        result = self.app_logic.handle_feedback_input("12")
        self.assertEqual(result, "need_feedback_input")  # Invalid conversion#
    
    def test_handle_code_input_invalid(self):
        """Test handling of invalid code input."""
        # Invalid inputs
        self.assertEqual(self.app_logic.handle_code_input("123"), "need_code_input")  # Too short
        self.assertEqual(self.app_logic.handle_code_input("12345"), "need_code_input")  # Too long
        self.assertEqual(self.app_logic.handle_code_input("ABCD"), "need_code_input")  # Invalid chars
        self.assertEqual(self.app_logic.handle_code_input(""), "need_code_input")  # Empty

    def test_handle_guess_input(self):
        """Test guess input handling."""
        # Configure and start game first
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")
        
        # Valid guess
        result = self.app_logic.handle_guess_input("1234")
        self.assertIn(result, ["need_guess_input", "game_over"])

        # Invalid guesses
        self.assertEqual(self.app_logic.handle_guess_input("123"), "need_guess_input")
        self.assertEqual(self.app_logic.handle_guess_input("ABCD"), "need_guess_input")
        self.assertEqual(self.app_logic.handle_guess_input(""), "need_guess_input")

    def test_handle_feedback_input(self):
        """Test feedback input handling."""
        # Configure and start game first
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)
        self.game_logic.make_computer_guess()

        # Partial feedback - game continues
        self.assertEqual(self.app_logic.handle_feedback_input("78"), "wait_for_computer_guess")

        # All correct feedback - computer wins
        self.assertEqual(self.app_logic.handle_feedback_input("8888"), "game_lost")

        # Invalid feedback
        self.assertEqual(self.app_logic.handle_feedback_input("999"), "need_feedback_input")
        self.assertEqual(self.app_logic.handle_feedback_input("ABC"), "need_feedback_input")

    def test_handle_computer_guess(self):
        """Test computer guess handling."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)

        # Test computer guess
        result = self.app_logic.handle_computer_guess()
        self.assertIn(result, ["need_feedback_input", "game_over"])  # include need_feedback_input

    def test_is_valid_code_none(self):
        """Test code validation with None input."""
        self.assertFalse(self.app_logic._is_valid_code(None))

    def test_handle_invalid_role(self):
        """Test handling invalid role."""
        # Configure and start game with invalid role
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        result = self.game_logic.startgame("invalid_role")
        self.assertEqual(result, "invalid_role")

    def test_handle_game_configuration(self):
        """Test game configuration validation."""
        # Valid configuration
        result = self.app_logic.handle_game_configuration(
            "Player1", "4", "6", "10"
        )
        self.assertNotEqual(result, "invalid_configuration")

        # Invalid player name
        self.assertEqual(
            self.app_logic.handle_game_configuration(
                "", "4", "6", "10"
            ),
            "invalid_configuration"
        )
        self.assertEqual(
            self.app_logic.handle_game_configuration(
                "   ", "4", "6", "10"
            ),
            "invalid_configuration"
        )

        # Invalid positions
        self.assertEqual(
            self.app_logic.handle_game_configuration(
                "Player1", "0", "6", "10"
            ),
            "invalid_configuration"
        )
        self.assertEqual(
            self.app_logic.handle_game_configuration(
                "Player1", "10", "6", "10"
            ),
            "invalid_configuration"
        )

        # Invalid colors
        self.assertEqual(
            self.app_logic.handle_game_configuration(
                "Player1", "4", "0", "10"
            ),
            "invalid_configuration"
        )
        self.assertEqual(
            self.app_logic.handle_game_configuration(
                "Player1", "4", "9", "10"
            ),
            "invalid_configuration"
        )

        # Invalid attempts
        self.assertEqual(
            self.app_logic.handle_game_configuration(
                "Player1", "4", "6", "-1"
            ),
            "invalid_configuration"
        )

        # Non-numeric values
        self.assertEqual(
            self.app_logic.handle_game_configuration(
                "Player1", "abc", "6", "10"
            ),
            "invalid_configuration"
        )

    def test_is_valid_feedback_edge_cases(self):
        """Test edge cases for feedback validation."""
        # Test None input
        self.assertFalse(self.app_logic._is_valid_feedback(None))

        # Test feedback too long (more than configured positions)
        too_long = "8" * (self.game_logic.positions + 1)
        self.assertFalse(self.app_logic._is_valid_feedback(too_long))

        # Test invalid characters
        self.assertFalse(self.app_logic._is_valid_feedback("123"))

        # Test mixed valid/invalid characters
        self.assertFalse(self.app_logic._is_valid_feedback("78A"))

        # Test exception case by passing a non-string
        # This will trigger the exception path since numbers don't have len()
        self.assertFalse(self.app_logic._is_valid_feedback(123))

    def test_handle_feedback_input_value_error(self):
        """Test handle_feedback_input with ValueError from game_logic."""
        # Setup game state
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)

        # Mock set_feedback to raise ValueError
        self.game_logic.set_feedback = Mock(side_effect=ValueError)

        # Test that ValueError is caught and handled
        result = self.app_logic.handle_feedback_input("78")
        self.assertEqual(result, "need_feedback_input")

    def test_get_game_state(self):
        """Test getting game state."""
        # Setup game state
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        # Setze einen geheimen Code, um den GameState zu initialisieren
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)  # Set secret code

        # Get game state through application logic
        game_state = self.app_logic.get_game_state()

        # Verify game state
        self.assertIsNotNone(game_state)
        self.assertEqual(game_state.positions, 4)
        self.assertEqual(game_state.colors, 6)
        self.assertEqual(game_state.player_name, "TestPlayer")
        self.assertEqual(game_state.max_rounds, 10)

    def test_handle_code_input_value_error(self):
        """Test handle_code_input with ValueError from color code conversion."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("coder")

        # Mock _convert_to_color_code to raise ValueError
        self.app_logic._convert_to_color_code = Mock(side_effect=ValueError)

        # Test that ValueError is caught and handled
        result = self.app_logic.handle_code_input("1234")
        self.assertEqual(result, "need_code_input")

    def test_handle_guess_input_edge_cases(self):
        """Test edge cases for guess input handling."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")

        # Test empty list case
        # Mock _convert_to_color_code to return empty list
        self.app_logic._convert_to_color_code = Mock(return_value=[])
        result = self.app_logic.handle_guess_input("1234")
        self.assertEqual(result, "need_guess_input")

        # Test ValueError case
        # Mock _convert_to_color_code to raise ValueError
        self.app_logic._convert_to_color_code = Mock(side_effect=ValueError)
        result = self.app_logic.handle_guess_input("1234")
        self.assertEqual(result, "need_guess_input")

    def test_handle_command(self):
        """Test command handling."""
        # Test valid commands
        self.assertEqual(self.app_logic.handle("1"), "choose_mode")
        self.assertEqual(self.app_logic.handle("2"), "choose_language")
        self.assertEqual(self.app_logic.handle("3"),"load_game")
        self.assertEqual(self.app_logic.handle("4"), "end_game")

        # Test invalid command
        self.assertEqual(self.app_logic.handle("invalid"), "invalid")
        self.assertEqual(self.app_logic.handle("5"), "invalid")

    def test_handle_server_connection(self):
        """Test server connection handling."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)

        # Mock NetworkService start_game to return True
        with patch('src.business_logic.business_logic.NetworkService') as mock_network:
            mock_network_instance = mock_network.return_value
            mock_network_instance.start_game.return_value = True

            # Test successful server connection
            result = self.app_logic.handle_server_connection("localhost", 8080)
            self.assertEqual(result, "need_guess_input")  # Changed expectation

            # Test failed server connection
            mock_network_instance.start_game.return_value = False
            result = self.app_logic.handle_server_connection("localhost", 8080)
            self.assertEqual(result, "error")

    def test_change_language(self):
        """Test language change handling."""
        result = self.app_logic.change_language()
        self.assertEqual(result, "choose_language")

    def test_end_game(self):
        """Test end game handling."""
        result = self.app_logic.end_game()
        self.assertEqual(result, "end_game")

    def test_save_game(self):
        """Test save game handling."""
        # Setup game state
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")

        # Test save game
        result = self.app_logic.save_game()
        self.assertEqual(result, "need_guess_input")

    def test_load_game(self):
        """Test load game handling."""
        # Setup mock game state
        mock_game_state = Mock()
        mock_game_state.current_guesser = PlayerGuesser()

        # Test successful load
        self.game_logic.load_game_state = Mock(return_value=None)
        self.game_logic.get_game_state = Mock(return_value=mock_game_state)
        result = self.app_logic.load_game()
        self.assertEqual(result, "need_guess_input")

        # Test load with FileNotFoundError
        self.game_logic.load_game_state = Mock(side_effect=FileNotFoundError)
        result = self.app_logic.load_game()
        self.assertEqual(result, "error")

    def test_process_game_action(self):
        """Test game action processing."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")

        # Test need_guess_input
        self.assertEqual(
            self.app_logic.process_game_action("need_guess_input", "menu"),
            "show_menu"
        )
        self.assertEqual(
            self.app_logic.process_game_action("need_guess_input", "1234"),
            "need_guess_input"  # or "game_over" depending on guess
        )

        # Test need_code_input
        self.assertEqual(
            self.app_logic.process_game_action("need_code_input", "menu"),
            "show_menu"
        )
        self.assertEqual(
            self.app_logic.process_game_action("need_code_input", "1234"),
            "wait_for_computer_guess"
        )

        # Test need_feedback_input
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)
        self.game_logic.make_computer_guess()

        self.assertEqual(
            self.app_logic.process_game_action("need_feedback_input", "menu"),
            "show_menu"
        )
        self.assertEqual(
            self.app_logic.process_game_action("need_feedback_input", "7878"),
            "wait_for_computer_guess"
        )

        # Test wait_for_computer_guess
        self.assertEqual(
            self.app_logic.process_game_action("wait_for_computer_guess"),
            "need_feedback_input"
        )

        # Test need_server_connection
        self.assertEqual(
            self.app_logic.process_game_action("need_server_connection", "menu"),
            "show_menu"
        )
        with patch('src.business_logic.business_logic.NetworkService') as mock_network:
            mock_network_instance = mock_network.return_value
            # Test successful connection
            mock_network_instance.start_game.return_value = True
            self.assertEqual(
                self.app_logic.process_game_action("need_server_connection", "localhost:8080"),
                "need_guess_input"  # Erwartet need_guess_input statt need_server_connection
            )
            # Test failed connection
            mock_network_instance.start_game.return_value = False
            self.assertEqual(
                self.app_logic.process_game_action("need_server_connection", "localhost:8080"),
                "error"
            )

    def test_handle_menu_action(self):
        """Test handling of menu actions."""
        # Setup game state with player guesser
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")

        # Test save game (when no save exists)
        self.game_logic.has_saved_game = Mock(return_value=False)
        result = self.app_logic.handle_menu_action("1")
        self.assertEqual(result, "save_game")

        # Test save game (when save exists)
        self.game_logic.has_saved_game = Mock(return_value=True)
        result = self.app_logic.handle_menu_action("1")
        self.assertEqual(result, "confirm_save")

        # Test change language
        result = self.app_logic.handle_menu_action("2")
        self.assertEqual(result, "choose_language")

        # Mock ComputerGuesser
        with patch('src.business_logic.business_logic.ComputerGuesser') as mock_guesser:
            # Mock load_game_state
            mock_game_state = Mock()
            mock_game_state.current_guesser = PlayerGuesser()
            self.game_logic.load_game_state = Mock(return_value=None)
            self.game_logic.get_game_state = Mock(return_value=mock_game_state)

            # Test load game
            result = self.app_logic.handle_menu_action("3")
            self.assertEqual(result, "need_guess_input")

        # Test end game
        result = self.app_logic.handle_menu_action("4")
        self.assertEqual(result, "back_to_menu")

        result = self.app_logic.handle_menu_action("5")
        self.assertEqual(result, "end_game")

        result = self.app_logic.handle_menu_action("10")
        self.assertEqual(result, "need_guess_input")

    def test_get_required_action(self):
        """Test getting required action for game modes."""
        # Test valid modes
        self.assertEqual(self.app_logic.get_required_action("1"), "need_configuration")
        self.assertEqual(self.app_logic.get_required_action("2"), "need_configuration")
        self.assertEqual(self.app_logic.get_required_action("3"), "need_configuration")
        self.assertEqual(self.app_logic.get_required_action("4"), "need_configuration")
        self.assertEqual(self.app_logic.get_required_action("5"), "back_to_menu")

        # Test invalid mode
        self.assertEqual(self.app_logic.get_required_action("6"), "invalid_mode")

    def test_configure_game(self):
        """Test game configuration with different modes."""
        config = {
            "player_name": "TestPlayer",
            "positions": "4",
            "colors": "6",
            "max_attempts": "10"
        }

        # Test guesser mode
        result = self.app_logic.configure_game("1", config)
        self.assertEqual(result, "need_guess_input")

        # Test coder mode
        result = self.app_logic.configure_game("2", config)
        self.assertEqual(result, "need_code_input")

        # Test online guesser mode
        result = self.app_logic.configure_game("3", config)
        self.assertEqual(result, "need_server_connection")

        # Test invalid mode
        result = self.app_logic.configure_game("5", config)
        self.assertEqual(result, "invalid_mode")

        # Test invalid configuration
        invalid_config = {
            "player_name": "",
            "positions": "4",
            "colors": "6",
            "max_attempts": "10"
        }
        result = self.app_logic.configure_game("1", invalid_config)
        self.assertEqual(result, "invalid_configuration")

    def test_can_start_game(self):
        """Test game start validation."""
        # Valid actions
        self.assertTrue(self.app_logic.can_start_game("need_guess_input"))
        self.assertTrue(self.app_logic.can_start_game("need_code_input"))

        # Invalid actions
        self.assertFalse(self.app_logic.can_start_game("invalid_mode"))
        self.assertFalse(self.app_logic.can_start_game("invalid_configuration"))
        self.assertFalse(self.app_logic.can_start_game("back_to_menu"))

    def test_is_game_over(self):
        """Test game over detection."""
        # Game over states
        self.assertTrue(self.app_logic.is_game_over("game_won"))
        self.assertTrue(self.app_logic.is_game_over("game_lost"))
        self.assertTrue(self.app_logic.is_game_over("error"))
        self.assertTrue(self.app_logic.is_game_over("cheating_detected"))

        # Non-game over states
        self.assertFalse(self.app_logic.is_game_over("need_guess_input"))
        self.assertFalse(self.app_logic.is_game_over("need_feedback_input"))

    def test_get_current_game_action(self):
        """Test getting current game action."""
        # Setup game state with player guesser
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")

        # Test player guesser case
        result = self.app_logic.get_current_game_action()
        self.assertEqual(result, "need_guess_input")

        # Setup game state with computer guesser
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)

        # Test computer guesser case
        result = self.app_logic.get_current_game_action()
        self.assertEqual(result, "need_feedback_input")

    def test_get_available_menu_actions(self):
        """Test getting available menu actions."""
        # Setup game state with player guesser
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")

        # Test player guesser menu
        actions = self.app_logic.get_available_menu_actions()
        self.assertIn("save_game", actions)
        self.assertIn("load_game", actions)
        self.assertIn("change_language", actions)
        self.assertIn("end_game", actions)

        # Setup game state with computer guesser
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)

        # Test computer guesser menu
        actions = self.app_logic.get_available_menu_actions()
        self.assertNotIn("save_game", actions)
        self.assertNotIn("load_game", actions)
        self.assertIn("change_language", actions)
        self.assertIn("end_game", actions)

    def test_confirm_save_game(self):
        """Test save game confirmation."""
        # Setup game state
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")

        # Test successful save
        result = self.app_logic.confirm_save_game()
        self.assertEqual(result, "save_game")

        # Test save failure
        self.game_logic.save_game_state = Mock(side_effect=FileNotFoundError)  # Änderung hier
        result = self.app_logic.confirm_save_game()
        self.assertEqual(result, "error")

    def test_get_positions(self):
        """Test getting number of positions."""
        # Without game state
        self.assertEqual(self.app_logic.get_positions(), 4)

        # With game state
        self.game_logic.configure_game("TestPlayer", 5, 6, 10)
        self.game_logic.startgame("guesser")
        self.assertEqual(self.app_logic.get_positions(), 5)

    def test_get_colors(self):
        """Test getting number of colors."""
        # Without game state
        self.assertEqual(self.app_logic.get_colors(), 6)

        # With game state
        self.game_logic.configure_game("TestPlayer", 4, 8, 10)
        self.game_logic.startgame("guesser")
        self.assertEqual(self.app_logic.get_colors(), 8)

    def test_handle_guess_input_empty_list(self):
        """Test handling of empty guess list."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")

        # Create a mock that returns valid numbers but creates empty list
        original_convert = self.app_logic._convert_to_color_code
        convert_results = []

        def mock_convert(num):
            if not convert_results:
                return original_convert(num)
            return convert_results.pop(0)

        self.app_logic._convert_to_color_code = mock_convert

        # Test empty list case
        result = self.app_logic.handle_guess_input("1234")
        self.assertEqual(result, "need_guess_input")

    def test_process_game_action_invalid(self):
        """Test process_game_action with invalid action."""
        # Setup
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")

        # Test invalid action
        result = self.app_logic.process_game_action("invalid_action")
        self.assertEqual(result, "error")

        # Test None action
        result = self.app_logic.process_game_action(None)
        self.assertEqual(result, "error")

        # Test empty action
        result = self.app_logic.process_game_action("")
        self.assertEqual(result, "error")

    def test_handle_menu_action_fallback(self):
        """Test handle_menu_action fallback to current game action."""
        # Setup game state with player guesser
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")

        # Mock get_current_game_action to return known value
        self.app_logic.get_current_game_action = Mock(return_value="need_guess_input")

        # Test that unhandled action falls back to current game action
        result = self.app_logic.handle_menu_action("7")  # Invalid choice
        self.assertEqual(result, "need_guess_input")

        # Test action when no special actions are available
        # Setup computer guesser state so save_game/load_game aren't available
        self.game_logic.startgame("coder")
        self.game_logic.set_secret_code([ColorCode(1)] * 4)

        # Test that menu option 3 maps to end_game when load_game isn't available
        result = self.app_logic.handle_menu_action("3")
        self.assertEqual(result, "end_game")  # Changed from need_guess_input

    def test_handle_menu_action_final_fallback(self):
        """Test handle_menu_action final fallback to current game action."""
        # Setup game state with player guesser
        self.game_logic.configure_game("TestPlayer", 4, 6, 10)
        self.game_logic.startgame("guesser")

        # Mock get_current_game_action to return known value
        self.app_logic.get_current_game_action = Mock(return_value="need_guess_input")

        # Create a situation where menu_map returns an invalid action
        mock_actions = []  # Empty list so no special actions are available
        self.app_logic.get_available_menu_actions = Mock(return_value=mock_actions)

        # Use an invalid menu choice that doesn't map to any action
        result = self.app_logic.handle_menu_action("5")  # Invalid choice
        self.assertEqual(result, "need_guess_input")



if __name__ == "__main__":
    unittest.main()