# tests/Network/test_http_handler.py
import os
import unittest
from unittest.mock import patch, Mock
import requests

from src.Network.HttpHandler import HTTPHandler


class TestHTTPHandler(unittest.TestCase):
    def setUp(self):
        self.handler = HTTPHandler("127.0.0.1", 8000)

    @patch("src.Network.HttpHandler.requests.post")
    def test_start_new_game_success(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"gameid": 1}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = self.handler.start_new_game("player1", 5, 8)
        self.assertEqual(response, 1)
        mock_post.assert_called_once_with(
            "http://127.0.0.1:8000",
            headers={"Content-Type": "application/json"},
            json={
                "gameid": 0,
                "gamerid": "player1",
                "positions": 5,
                "colors": 8,
                "value": "",
            },
        )

    @patch("src.Network.HttpHandler.requests.post")
    def test_make_move_success(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"value": "7788"}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = self.handler.make_move(1, "player1", 5, 8, "12345")
        self.assertEqual(response, "7788")
        mock_post.assert_called_once_with(
            "http://127.0.0.1:8000",
            headers={"Content-Type": "application/json"},
            json={
                "gameid": 1,
                "gamerid": "player1",
                "positions": 5,
                "colors": 8,
                "value": "12345",
            },
        )

    @patch("src.Network.HttpHandler.requests.post")
    def test_invalid_json(self, mock_post):
        invalid_json = {
            "gameid": 0,
            "gamerid": "player1",
            "position": 10,  # Invalid key
            "colors": 8,
            "value": "",
        }
        mock_post.return_value = None  # Ensure no actual post is made
        with self.assertLogs(level="ERROR") as log:
            response = self.handler.send_json_via_post(
                "http://127.0.0.1:8000", invalid_json
            )
            self.assertIsNone(response)
            self.assertIn(
                "Validation error: 'positions' is a required property", log.output[0]
            )

    @patch("src.Network.HttpHandler.requests.post")
    def test_http_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.HTTPError("HTTP error")
        with self.assertRaises(requests.exceptions.HTTPError):
            self.handler.start_new_game("player1", 5, 8)

    @patch("src.Network.HttpHandler.requests.post")
    def test_request_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Request error")
        with self.assertRaises(requests.exceptions.RequestException):
            self.handler.start_new_game("player1", 5, 8)

    def test_validate_json_success(self):
        valid_json = {
            "gameid": 0,
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": "",
        }
        self.assertTrue(self.handler.validate_json(valid_json))

    def test_validate_json_failure(self):
        invalid_json = {
            "gameid": 0,
            "gamerid": "player1",
            "positions": 5,
            "color": 8,  # Invalid key
            "value": "",
        }
        self.assertFalse(self.handler.validate_json(invalid_json))

    @patch("src.Network.HttpHandler.requests.post")
    def test_load_schema(self, mock_post):
        cur_path = os.path.dirname(__file__)
        schema_path = os.path.relpath("../../src/util/schema.json", cur_path)
        schema = self.handler.load_schema(schema_path)
        self.assertIsNotNone(schema)
        self.assertIn("gameid", schema)
        self.assertIn("gamerid", schema)
        self.assertIn("positions", schema)
        self.assertIn("colors", schema)
        self.assertIn("value", schema)


if __name__ == "__main__":
    unittest.main()
