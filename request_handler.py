from urllib.parse import urlparse, parse_qs
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import *


class HandleRequests(BaseHTTPRequestHandler):
    # Here's a class function
    # replace the parse_url function in the class
    def parse_url(self, path):
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]
        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)
        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def do_GET(self):
        """Handles GET requests to the server """
        response = {}  # Default response
        parsed = self.parse_url(self.path)
        # Parse the URL and capture the tuple that is returned

        if '?' not in self.path:
            (resource, id) = parsed
            if resource == "species":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_species(id)

                else:
                    self._set_headers(200)
                    response = get_all_species()

            elif resource == "snakes":
                if id is not None:
                    # self._set_headers(200)
                    response = get_single_snakes(self, id)

                else:
                    self._set_headers(200)
                    response = get_all_snakes()

            elif resource == "owners":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_owners(id)

                else:
                    self._set_headers(200)
                    response = get_all_owners()

            else:
                self._set_headers(404)
                response = {}
        else:
            (resource, query) = parsed
            # see if the query dictionary has an email key
            if query.get('species') and resource == 'snakes':
                response = get_snake_by_species(query['species'][0])
                self._set_headers(200)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)
        new_snake = None

        if resource == "snakes":
            # self._set_headers(201)

            if "name" not in post_body:
                self._set_headers(400)
                new_snake = "Missing snake name"
            elif "owner_id" not in post_body:
                self._set_headers(400)
                new_snake = "Missing owner information."
            elif "species_id" not in post_body:
                self._set_headers(400)
                new_snake = "Missing species information."
            elif "gender" not in post_body:
                self._set_headers(400)
                new_snake = "Missing gender information."
            elif "color" not in post_body:
                self._set_headers(400)
                new_snake = "Missing color information."

            else:
                self._set_headers(201)
                new_snake = create_snake(post_body)

        self.wfile.write(json.dumps(new_snake).encode())

    def do_DELETE(self):
        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        # Delete a single order from the list
        if resource == "snakes":
            # Set a 204 response code
            self._set_headers(204)
            response = {}
        else:
            self._set_headers(404)
            response = {}

        # Encode the new order and send in response
        self.wfile.write(response.encode())

    def do_PUT(self):
        """Handles PUT requests to the server """
        (resource, id) = self.parse_url(self.path)
        # Delete a single order from the list
        if resource == "snakes":
            # Set a 204 response code
            self._set_headers(204)
            response = {}
        else:
            self._set_headers(404)
            response = {}

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
