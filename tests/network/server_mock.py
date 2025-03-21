"""Description: Mock server for testing the network module."""
import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import ClassVar, Union, Tuple


class MockServerRequestHandler(BaseHTTPRequestHandler):
    """Request handler for the test server."""

    last_game_id: ClassVar[int] = 0

    def __init__(self: "MockServerRequestHandler",
                 request: Union[socket.socket, tuple[bytes, socket.socket]],
                 client_address: Tuple[str, int], server: HTTPServer) -> None:
        """Initialize the request handler."""
        super().__init__(request, client_address, server)

    def do_POST(self: "MockServerRequestHandler") -> None:
        """Handle POST requests."""
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        response = {}

        try:
            data = json.loads(post_data)
            if (
                "gameid" in data
                and "gamerid" in data
                and "positions" in data
                and "colors" in data
                and "value" in data
            ):  # valid JSON
                if (
                    data["positions"] > 9 or data["colors"] > 8
                ):  # invalid positions or colors
                    self.send_response(400)
                    response = {"error": "Invalid JSON"}
                else:
                    if data["gameid"] == 0:  # start new game
                        self.send_response(200)
                        response = data
                        response["gameid"] = self.last_game_id + 1
                        self.last_game_id = self.last_game_id + 1

                    if data["gameid"] > 0 and data["value"] != "":  # make move
                        self.send_response(200)
                        response = data
                        response["value"] = "7788"
            else:
                self.send_response(400)
                response = {"error": "Invalid JSON"}
        except json.JSONDecodeError:
            self.send_response(400)
            response = {"error": "Invalid JSON"}

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))


def run(server_class: HTTPServer, handler_class: MockServerRequestHandler,
        port: int = 8000) -> None:
    """Run the test server."""
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting test server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    """
    Main program execution.
    """
    run()
