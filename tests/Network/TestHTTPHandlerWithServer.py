import unittest
from unittest.mock import patch, Mock
import requests
import os
import subprocess
import time
from src.Network.HttpHandler import HTTPHandler
from jsonschema.exceptions import ValidationError

class TestHTTPHandlerWithServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_ip = os.getenv('TEST_SERVER_IP', '127.0.0.1')
        cls.server_port = int(os.getenv('TEST_SERVER_PORT', 8000))
        cls.server_process = subprocess.Popen(['python', 'test_server.py'])
        time.sleep(1)  # Give the server a second to start
        cls.handler = HTTPHandler(cls.server_ip, cls.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()
        cls.server_process.wait()

    def test_start_new_game_success(self):
        response = self.handler.start_new_game('player1', 4, 6)
        expected_response = {
            "gameid": 1,
            "gamerid": 'player1',
            "positions": 4,
            "colors": 6,
            "value": ""
        }
        self.assertIsNotNone(response)
        self.assertDictEqual(response, expected_response)

    def test_start_new_game_invalid_params(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            self.handler.start_new_game('player1', 10, 9)  # Invalid positions and colors

    def test_make_move_success(self):
        response = self.handler.make_move(1, 'player1', 4, 6, '1234')
        self.assertIsNotNone(response)
        self.assertIn('result', response)

    def test_make_move_invalid_params(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            self.handler.make_move(1, 'player1', 10, 9, '1234')  # Invalid positions and colors

    def test_json_validation_error(self):
        invalid_json = {
            "gameid": 0,
            "gamerid": 'player1',
            "positions": 10,  # Invalid value
            "colors": 8,
            "value": ""
        }
        with self.assertLogs(level='ERROR') as log:
            response = self.handler.send_json_via_post(f'http://{self.server_ip}:{self.server_port}', invalid_json)
            self.assertIsNone(response)
            self.assertIn("Invalid JSON data. Aborting POST request.", log.output[0])

    def test_http_error(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            self.handler.send_json_via_post(f'http://{self.server_ip}:{self.server_port}', {})

    def test_request_error(self):
        with self.assertRaises(requests.exceptions.RequestException):
            self.handler.send_json_via_post(f'http://{self.server_ip}:{self.server_port}', {})

if __name__ == '__main__':
    unittest.main()