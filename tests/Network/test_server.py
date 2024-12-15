import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class TestServerRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        response = {}

        try:
            data = json.loads(post_data)
            if 'gameid' in data and 'gamerid' in data and 'positions' in data and 'colors' in data and 'value' in data:
                if data['positions'] > 9 or data['colors'] > 8:
                    self.send_response(400)
                    response = {"error": "Invalid JSON"}
                else:
                    self.send_response(200)
                    response = {"gameid": 1, "result": "success"}
            else:
                self.send_response(400)
                response = {"error": "Invalid JSON"}
        except json.JSONDecodeError:
            self.send_response(400)
            response = {"error": "Invalid JSON"}

        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=TestServerRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting test server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()