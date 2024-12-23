import threading
import unittest
from http.server import HTTPServer

import requests
from src.Network.HttpHandler import HTTPHandler
from tests.Network.test_server import TestServerRequestHandler


class TestHTTPHandlerWithServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the test server and HTTPHandler instance.
        """
        cls.server = HTTPServer(("localhost", 0), TestServerRequestHandler)
        cls.server_port = cls.server.server_address[1]

        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

        cls.handler = HTTPHandler("localhost", cls.server_port)

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test server.
        """
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def print_response(self, response):
        """
        Print the response for debugging purposes.
        """
        print()
        print()
        print(f"Response: {response}")
        print()

    def test_start_new_game_success(self):
        """
        Test starting a new game successfully.
        """
        response = self.handler.start_new_game("player1", 5, 8)
        self.print_response(response)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, int)
        self.assertGreater(response, 0)

    def test_start_new_game_invalid_params(self):
        """
        Test starting a new game with invalid parameters.
        """
        with self.assertRaises(requests.exceptions.HTTPError):
            response = self.handler.start_new_game(
                "player1", 10, 9
            )  # Invalid positions and colors
            self.print_response(response)

    def test_make_move_success(self):
        """
        Test making a move successfully.
        """
        # only the value is changed in the response of a successful move
        initial_value = "1234"
        response = self.handler.make_move(1, "player1", 5, 8, initial_value)
        self.print_response(response)
        self.assertIsNotNone(response)
        self.assertNotEqual(response, initial_value)
        self.assertEqual(response, "7788")  # Der TestServer gibt immer "7788" zurück

    def test_make_move_invalid_params(self):
        """
        Test making a move with invalid parameters.
        """
        with self.assertRaises(requests.exceptions.HTTPError):
            response = self.handler.make_move(
                1, "player1", 10, 9, "1234"
            )  # Invalid positions and colors
            self.print_response(response)

    def test_invalid_json_via_post(self):
        """
        Test sending invalid JSON via POST.
        """
        invalid_json = {
            "gameid": 0,
            "gamerid": "player1",
            "positions": 10,  # Invalid value
            "colors": 8,
            "value": "",
        }
        with self.assertLogs(level="ERROR"):
            with self.assertRaises(requests.exceptions.HTTPError):
                response = self.handler.send_json_via_post(invalid_json)
                self.print_response(response)


if __name__ == "__main__":
    unittest.main()
