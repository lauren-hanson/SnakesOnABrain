from urllib.parse import urlparse, parse_qs
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import *


class HandleRequests(BaseHTTPRequestHandler):
    # Here's a class function
    # replace the parse_url function in the class
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
        id = None
        try:
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass
        return (resource, id)

    def do_GET(self):
        """Handles GET requests to the server """
        self._set_headers(200)
        response = {}  # Default response
        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)
        if resource == "species":
            if id is not None:
                response = get_single_species(id)
            else:
                response = get_all_species()

        self.wfile.write(json.dumps(response).encode())

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
