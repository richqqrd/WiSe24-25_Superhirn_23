import json
import random
from http.server import BaseHTTPRequestHandler
from typing import Dict, Any


class MastermindTestServer(BaseHTTPRequestHandler):
    """Test server for Mastermind game."""
    
    # Store active games
    games: Dict[int, Dict[str, Any]] = {}
    next_game_id = 1

    def _send_response(self, status_code: int, response_data: Dict[str, Any]) -> None:
        """Send HTTP response with JSON data."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def _validate_request(self, data: Dict[str, Any]) -> bool:
        """Validate request against schema."""
        required_fields = ['gameid', 'gamerid', 'positions', 'colors', 'value']
        if not all(field in data for field in required_fields):
            return False
            
        if not isinstance(data['gameid'], int):
            return False
        if not isinstance(data['gamerid'], str):
            return False
        if not (1 <= data['positions'] <= 8):
            return False
        if not (1 <= data['colors'] <= 8):
            return False
        if not isinstance(data['value'], str):
            return False
            
        return True

    def _calculate_feedback(self, guess: str, code: str) -> str:
        """Calculate feedback for a guess."""
        feedback = []
        temp_guess = list(guess)
        temp_code = list(code)

        # Check for exact matches (black pins)
        for i in range(len(temp_code)):
            if temp_guess[i] == temp_code[i]:
                feedback.append('8')  # Black pin
                temp_code[i] = 'X'
                temp_guess[i] = 'Y'

        # Check for color matches (white pins)
        for i in range(len(temp_guess)):
            if temp_guess[i] != 'Y' and temp_guess[i] in temp_code:
                feedback.append('7')  # White pin
                temp_code[temp_code.index(temp_guess[i])] = 'X'

        return ''.join(feedback)


    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            if not self._validate_request(data):
                self._send_response(400, {"error": "Invalid request format"})
                return

            # New game request (gameid = 0)
            if data['gameid'] == 0:
                game_id = self.next_game_id
                self.next_game_id += 1
                
                # Generate secret code based on positions and colors
                secret_code = ''.join(
                    str(random.randint(1, data['colors'])) 
                    for _ in range(data['positions'])
                )
                
                # Store new game data
                self.games[game_id] = {
                    'gamerid': data['gamerid'],
                    'positions': data['positions'],
                    'colors': data['colors'],
                    'secret_code': secret_code
                }
                
                response = {
                    'gameid': game_id,
                    'gamerid': data['gamerid'],
                    'positions': data['positions'],
                    'colors': data['colors'],
                    'value': ''
                }
                print(f"New game started with secret code: {secret_code}")
                self._send_response(200, response)
                return

            # Handle guess for existing game
            game_id = data['gameid']
            if game_id not in self.games:
                self._send_response(404, {"error": "Game not found"})
                return

            game = self.games[game_id]
            if data['gamerid'] != game['gamerid']:
                self._send_response(403, {"error": "Invalid player"})
                return

            # Calculate feedback for guess
            guess = data['value']
            feedback = self._calculate_feedback(guess, game['secret_code'])
            
            response = {
                'gameid': game_id,
                'gamerid': data['gamerid'],
                'positions': game['positions'],
                'colors': game['colors'],
                'value': feedback
            }
            self._send_response(200, response)

        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
        except Exception as e:
            self._send_response(500, {"error": str(e)})

def run_server(port: int = 8000):
        """Run the test server on localhost."""
        from http.server import HTTPServer
        server_address = ('localhost', port)
        httpd = HTTPServer(server_address, MastermindTestServer)
        print(f"Starting test server on http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()

if __name__ == "__main__":
        run_server()