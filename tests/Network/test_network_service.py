import unittest
from unittest.mock import patch
from src.Network.network_service import NetworkService


class TestNetworkService(unittest.TestCase):
    def setUp(self):
        """
        Set up test cases.
        """
        self.service = NetworkService("localhost", 8000)
        self.test_player_id = "player1"
        self.test_value = "1234"

    @patch("src.Network.HttpHandler.HTTPHandler.start_new_game")
    def test_start_game_success(self, mock_start_game):
        """
        Test successful game start
        """
        mock_start_game.return_value = 1

        result = self.service.start_game(self.test_player_id)

        self.assertTrue(result)
        self.assertEqual(self.service.current_game_id, 1)
        self.assertEqual(self.service.current_player_id, self.test_player_id)
        mock_start_game.assert_called_once_with(
            self.test_player_id, self.service.positions, self.service.colors
        )

    @patch("src.Network.HttpHandler.HTTPHandler.start_new_game")
    def test_start_game_failure(self, mock_start_game):
        """
        Test failed game start
        """
        mock_start_game.side_effect = Exception("Connection error")

        with self.assertLogs(level="ERROR") as log:
            result = self.service.start_game(self.test_player_id)

        self.assertFalse(result)
        self.assertIsNone(self.service.current_game_id)
        self.assertEqual(self.service.current_player_id, self.test_player_id)
        self.assertIn("Failed to start game", log.output[0])

    @patch("src.Network.HttpHandler.HTTPHandler.make_move")
    def test_make_move_success(self, mock_make_move):
        """
        Test successful move
        """
        self.service.current_game_id = 1
        self.service.current_player_id = self.test_player_id
        expected_response = "7788"
        mock_make_move.return_value = expected_response

        result = self.service.make_move(self.test_value)

        self.assertEqual(result, expected_response)
        mock_make_move.assert_called_once_with(
            self.service.current_game_id,
            self.service.current_player_id,
            self.service.positions,
            self.service.colors,
            self.test_value,
        )

    def test_make_move_no_active_game(self):
        """
        Test move without active game
        """
        self.service.current_game_id = None
        self.service.current_player_id = None

        with self.assertRaises(ValueError) as context:
            self.service.make_move(self.test_value)

        self.assertEqual(str(context.exception), "No active game")

    @patch("src.Network.HttpHandler.HTTPHandler.make_move")
    def test_make_move_failure(self, mock_make_move):
        """
        Test failed move
        """
        self.service.current_game_id = 1
        self.service.current_player_id = self.test_player_id
        mock_make_move.side_effect = Exception("Connection error")

        with self.assertLogs(level="ERROR") as log:
            result = self.service.make_move(self.test_value)

        self.assertIsNone(result)
        self.assertIn("Failed to make move", log.output[0])


if __name__ == "__main__":
    unittest.main()
