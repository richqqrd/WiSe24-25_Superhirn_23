"""Test module for NetworkService."""

import unittest
from unittest.mock import patch, Mock
from src.network.network_service import NetworkService
from src.network.http_handler import HttpHandler


class TestNetworkService(unittest.TestCase):
    """Test cases for NetworkService."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.service = NetworkService("localhost", 8000)
        self.test_player_id = "player1"
        self.test_value = "1234"
        self.service.positions = 4
        self.service.colors = 6

    def test_init(self):
        """Test initialization of NetworkService."""
        self.assertIsNotNone(self.service.http_handler)
        self.assertIsNone(self.service.current_game_id)
        self.assertIsNone(self.service.current_player_id)
        self.assertEqual(self.service.positions, 4)
        self.assertEqual(self.service.colors, 6)

    @patch("src.network.http_handler.HttpHandler.start_new_game")
    def test_start_game_success(self, mock_start_game):
        """Test successful game start."""
        mock_start_game.return_value = 1

        result = self.service.start_game(self.test_player_id)

        self.assertTrue(result)
        self.assertEqual(self.service.current_game_id, 1)
        self.assertEqual(self.service.current_player_id, self.test_player_id)
        mock_start_game.assert_called_once_with(
            self.test_player_id, self.service.positions, self.service.colors
        )

    @patch("src.network.http_handler.HttpHandler.start_new_game")
    def test_start_game_failure(self, mock_start_game):
        """Test failed game start."""
        mock_start_game.side_effect = Exception("Connection error")

        with self.assertLogs(level="ERROR") as log:
            result = self.service.start_game(self.test_player_id)

        self.assertFalse(result)
        self.assertIsNone(self.service.current_game_id)
        self.assertEqual(self.service.current_player_id, self.test_player_id)
        self.assertIn("Failed to start game", log.output[0])

    @patch("src.network.http_handler.HttpHandler.make_move")
    def test_make_move_success(self, mock_make_move):
        """Test successful move."""
        expected_response = "7788"
        mock_make_move.return_value = expected_response
        self.service.current_game_id = 1
        self.service.current_player_id = self.test_player_id

        result = self.service.make_move(self.test_value)

        self.assertEqual(result, expected_response)
        mock_make_move.assert_called_once_with(
            1, self.test_player_id, self.service.positions, 
            self.service.colors, self.test_value
        )

    @patch("src.network.http_handler.HttpHandler.make_move")
    def test_make_move_failure(self, mock_make_move):
        """Test failed move."""
        mock_make_move.side_effect = Exception("Connection error")
        self.service.current_game_id = 1
        self.service.current_player_id = self.test_player_id

        with self.assertLogs(level="ERROR") as log:
            result = self.service.make_move(self.test_value)

        self.assertIsNone(result)
        self.assertIn("Failed to make move", log.output[0])

    def test_make_move_no_game(self):
        """Test move without active game."""
        self.service.current_game_id = None
        with self.assertRaises(ValueError):
            self.service.make_move(self.test_value)

    def test_make_move_no_player(self):
        """Test move without player ID."""
        self.service.current_game_id = 1
        self.service.current_player_id = None
        with self.assertRaises(ValueError):
            self.service.make_move(self.test_value)


if __name__ == "__main__":
    unittest.main()