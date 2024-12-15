import unittest
from unittest.mock import patch, Mock
import requests
import self

from src.Network.HttpHandler import HTTPHandler
from jsonschema.exceptions import ValidationError


class TestHTTPHandler(unittest.TestCase):
    def setUp(self):
        self.handler = HTTPHandler('127.0.0.1', 8000)

    @patch('src.Network.HttpHandler.requests.post')
    def test_start_new_game_success(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"gameid": 1}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = self.handler.start_new_game('player1', 5, 8)
        self.assertEqual(response, {"gameid": 1})
        mock_post.assert_called_once_with(
            'http://127.0.0.1:8000',
            headers={'Content-Type': 'application/json'},
            json={
                "gameid": 0,
                "gamerid": 'player1',
                "positions": 5,
                "colors": 8,
                "value": ""
            }
        )

    @patch('src.Network.HttpHandler.requests.post')
    def test_make_move_success(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success"}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = self.handler.make_move(1, 'player1', 5, 8, '12345')
        self.assertEqual(response, {"result": "success"})
        mock_post.assert_called_once_with(
            'http://127.0.0.1:8000',
            headers={'Content-Type': 'application/json'},
            json={
                "gameid": 1,
                "gamerid": 'player1',
                "positions": 5,
                "colors": 8,
                "value": '12345'
            }
        )

@patch('src.Network.HttpHandler.requests.post')
def test_invalid_json(self, mock_post):
    invalid_json = {
        "gameid": 0,
        "gamerid": 'player1',
        "positions": 10,  # Invalid value
        "colors": 8,
        "value": ""
    }
    mock_response = Mock()
    mock_response.status_code = 400  # Simulate a bad request response
    mock_post.return_value = mock_response
    with self.assertLogs(level='ERROR') as log:
        response = self.handler.send_json_via_post('http://127.0.0.1:8000', invalid_json)
        self.assertIsNone(response)
        self.assertIn("Invalid JSON data. Aborting POST request.", log.output[0])

    @patch('src.Network.HttpHandler.requests.post')
    def test_http_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.HTTPError("HTTP error")
        with self.assertRaises(requests.exceptions.HTTPError):
            self.handler.start_new_game('player1', 5, 8)

    @patch('src.Network.HttpHandler.requests.post')
    def test_request_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Request error")
        with self.assertRaises(requests.exceptions.RequestException):
            self.handler.start_new_game('player1', 5, 8)

    def test_load_schema(self):
        schema = self.handler.load_schema('src/util/schema.json')
        self.assertIn('$schema', schema)
        self.assertIn('properties', schema)

    def test_validate_json_success(self):
        valid_json = {
            "gameid": 0,
            "gamerid": 'player1',
            "positions": 5,
            "colors": 8,
            "value": ""
        }
        self.assertTrue(self.handler.validate_json(valid_json))

    def test_validate_json_failure(self):
        invalid_json = {
            "gameid": 0,
            "gamerid": 'player1',
            "positions": 10,  # Invalid value
            "colors": 8,
            "value": ""
        }
        self.assertFalse(self.handler.validate_json(invalid_json))


if __name__ == '__main__':
    unittest.main()