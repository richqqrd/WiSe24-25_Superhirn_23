"""Test cases for HTTPHandler class."""
import unittest
from unittest.mock import patch
import requests
from src.network.http_handler import HttpHandler
from src.network.http_handler import JsonValidator, HttpClient


class TestHTTPHandler(unittest.TestCase):
    """Test cases for HTTPHandler class."""

    def setUp(self: "TestHTTPHandler") -> None:
        """Set up test fixtures before each test method."""
        self.handler: HttpHandler = HttpHandler("127.0.0.1", 8000)
        self.valid_json: dict = {
            "gameid": 0,
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": "",
        }

    def test_init(self: "TestHTTPHandler") -> None:
        """Test initialization of HTTPHandler."""
        self.assertEqual(self.handler.base_url, "http://127.0.0.1:8000")
        self.assertIsNotNone(self.handler.http_client)
        self.assertIsNotNone(self.handler.validate)

    @patch("src.network.http_handler.HttpClient.post")
    @patch("src.network.http_handler.JsonValidator")
    def test_send_json_via_post_success(self: "TestHTTPHandler",
                                        mock_validator: JsonValidator,
                                        mock_post: HttpClient) -> None:
        """Test successful JSON POST request."""
        mock_validator.return_value.validate.return_value = True
        mock_post.return_value = self.valid_json

        response = self.handler.send_json_via_post(self.valid_json)

        self.assertEqual(response, self.valid_json)
        mock_post.assert_called_once_with("", self.valid_json)

    @patch("src.network.http_handler.HttpClient.post")
    @patch("src.network.http_handler.JsonValidator")
    def test_send_json_via_post_invalid_json(self: "TestHTTPHandler",
                                             mock_validator: JsonValidator,
                                             mock_post: HttpClient) -> None:
        """Test POST request with invalid JSON."""
        mock_validator.return_value.validate.return_value = False

        with self.assertRaises(ValueError):
            self.handler.send_json_via_post({"invalid": "json"})

        mock_post.assert_not_called()

    @patch("src.network.http_handler.HttpClient.post")
    @patch("src.network.http_handler.JsonValidator")
    def test_send_json_via_post_http_error(self: "TestHTTPHandler",
                                           mock_validator: JsonValidator,
                                           mock_post: HttpClient) -> None:
        """Test POST request with HTTP error."""
        mock_validator.return_value.validate.return_value = True
        mock_post.side_effect = requests.exceptions.HTTPError("404 Error")

        with self.assertRaises(requests.exceptions.HTTPError):
            self.handler.send_json_via_post(self.valid_json)

    @patch("src.network.http_handler.HttpClient.post")
    @patch("src.network.http_handler.JsonValidator")
    def test_start_new_game_success(self: "TestHTTPHandler",
                                    mock_validator: JsonValidator,
                                    mock_post: HttpClient) -> None:
        """Test successful game start."""
        mock_validator.return_value.validate.return_value = True
        mock_response: dict = {
            "gameid": 1,
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": ""
        }
        mock_post.return_value = mock_response

        game_id = self.handler.start_new_game("player1", 5, 8)

        self.assertEqual(game_id, 1)
        expected_request: dict = {
            "gameid": 0,
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": ""
        }
        mock_post.assert_called_once_with("", expected_request)

    @patch("src.network.http_handler.HttpClient.post")
    @patch("src.network.http_handler.JsonValidator")
    def test_start_new_game_error(self: "TestHTTPHandler",
                                  mock_validator: JsonValidator,
                                  mock_post: HttpClient) -> None:
        """Test game start with error."""
        mock_validator.return_value.validate.return_value = True
        mock_post.side_effect = requests.exceptions.HTTPError("500 Error")

        with self.assertRaises(requests.exceptions.HTTPError):
            self.handler.start_new_game("player1", 5, 8)

    @patch("src.network.http_handler.HttpClient.post")
    @patch("src.network.http_handler.JsonValidator")
    def test_make_move_success(self: "TestHTTPHandler", mock_validator: JsonValidator,
                               mock_post: HttpClient) -> None:
        """Test successful move."""
        mock_validator.return_value.validate.return_value = True
        mock_post.return_value = {**self.valid_json, "value": "7788"}

        response = self.handler.make_move(1, "player1", 5, 8, "1234")

        self.assertEqual(response, "7788")
        self.assertTrue(mock_post.called)

    @patch("src.network.http_handler.HttpClient.post")
    @patch("src.network.http_handler.JsonValidator")
    def test_make_move_error(self: "TestHTTPHandler", mock_validator: JsonValidator,
                             mock_post: HttpClient) -> None:
        """Test move with error."""
        mock_validator.return_value.validate.return_value = True
        mock_post.side_effect = requests.exceptions.HTTPError("500 Error")

        with self.assertRaises(requests.exceptions.HTTPError):
            self.handler.make_move(1, "player1", 5, 8, "1234")


if __name__ == "__main__":
    unittest.main()
