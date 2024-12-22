import unittest

import requests
import os
import subprocess
import time
from src.Network.HttpHandler import HTTPHandler


class TestHTTPHandlerWithServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_ip = os.getenv("TEST_SERVER_IP", "141.45.35.16")
        cls.server_port = int(os.getenv("TEST_SERVER_PORT", 5001))
        # cls.server_process = subprocess.Popen(['python', 'test_server.py'])
        # time.sleep(1)  # Give the server a second to start
        cls.handler = HTTPHandler(cls.server_ip, cls.server_port)

    @classmethod
    def tearDownClass(cls):
        pass
        # cls.server_process.terminate()
        # cls.server_process.wait()

    def print_response(self, response):
        print()
        print()
        print(f"Response: {response}")
        print()

    def test_start_new_game_success(self):
        response = self.handler.start_new_game("player1", 5, 8)
        self.print_response(response)
        expected_response = {
            "gameid": 22544278,
            "gamerid": "player1",
            "positions": 5,
            "colors": 8,
            "value": "",
        }
        self.assertIsNotNone(response)
        self.assertDictEqual(response, expected_response)

    def test_start_new_game_invalid_params(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            response = self.handler.start_new_game(
                "player1", 10, 9
            )  # Invalid positions and colors
            self.print_response(response)

    def test_make_move_success(self):
        # only the value is changed in the response of a successful move
        initial_value = "1234"
        response = self.handler.make_move(1, "player1", 5, 8, initial_value)
        self.print_response(response)
        self.assertIsNotNone(response)
        self.assertEqual(response["gameid"], 1)
        self.assertEqual(response["gamerid"], "player1")
        self.assertEqual(response["positions"], 5)
        self.assertEqual(response["colors"], 8)
        self.assertNotEqual(response["value"], initial_value)

    def test_make_move_invalid_params(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            response = self.handler.make_move(
                1, "player1", 10, 9, "1234"
            )  # Invalid positions and colors
            self.print_response(response)

    def test_invalid_json_via_post(self):
        invalid_json = {
            "gameid": 0,
            "gamerid": "player1",
            "positions": 10,  # Invalid value
            "colors": 8,
            "value": "",
        }
        with self.assertLogs(level="ERROR") as log:
            with self.assertRaises(requests.exceptions.HTTPError):
                response = self.handler.send_json_via_post(
                    f"http://{self.server_ip}:{self.server_port}", invalid_json
                )
                self.print_response(response)


if __name__ == "__main__":
    unittest.main()
