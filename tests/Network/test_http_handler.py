# tests/Network/test_http_handler.py
import unittest
from unittest.mock import patch
from src.Network.HttpHandler import HTTPHandler


class TestHTTPHandler(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case with an instance of HTTPHandler.
        """
        self.handler = HTTPHandler("127.0.0.1", 8000)

    @patch("src.Network.HttpHandler.HttpClient.post")
    @patch("src.Network.HttpHandler.JsonValidator")
    def test_send_json_via_post_success(self, mock_validator, mock_post):
        """
        Test sending JSON via POST request successfully.
        """
        mock_validator.return_value.validate.return_value = True
        valid_json = {
            "gameid": 0,
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": "",
        }
        mock_post.return_value = valid_json
        response = self.handler.send_json_via_post(valid_json)
        self.assertEqual(response, valid_json)

    @patch("src.Network.HttpClient.HttpClient.post")
    @patch("src.Network.HttpHandler.JsonValidator")
    def test_send_json_via_post_invalid(self, mock_validator, mock_post):
        """
        Test sending invalid JSON via POST request.
        """
        mock_validator.return_value.validate.return_value = False
        invalid_json = {
            "gameid": 0,
            "gamerid": "player1",
            "invalid_key": 5,
            "colors": 8,
            "value": "",
        }
        with self.assertRaises(ValueError):
            self.handler.send_json_via_post(invalid_json)
        mock_post.assert_not_called()

    @patch("src.Network.HttpHandler.HttpClient.post")
    @patch("src.Network.HttpHandler.JsonValidator")
    def test_start_new_game_success(self, mock_validator, mock_post):
        """
        Test starting a new game successfully.
        """
        mock_validator.return_value.validate.return_value = True
        mock_response = {
            "gameid": 1,
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": "",
        }
        mock_post.return_value = mock_response
        response = self.handler.start_new_game("player1", 5, 8)
        self.assertEqual(response, 1)
        mock_post.assert_called_once_with(
            "",
            {
                "gameid": 0,
                "gamerid": "player1",
                "positions": 5,
                "colors": 8,
                "value": "",
            },
        )

    @patch("src.Network.HttpHandler.HttpClient.post")
    @patch("src.Network.HttpHandler.JsonValidator")
    def test_make_move_success(self, mock_validator, mock_post):
        """
        Test making a move successfully.
        """
        mock_validator.return_value.validate.return_value = True
        mock_response = {
            "gameid": 1,
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": "7788",
        }

        mock_post.return_value = mock_response

        response = self.handler.make_move(1, "player1", 5, 8, "12345")

        self.assertEqual(response, "7788")
        mock_post.assert_called_once_with(
            "",
            {
                "gameid": 1,
                "gamerid": "player1",
                "positions": 5,
                "colors": 8,
                "value": "12345",
            },
        )


if __name__ == "__main__":
    unittest.main()
