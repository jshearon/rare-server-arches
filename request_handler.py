import json
from http.server import BaseHTTPRequestHandler, HTTPServer
<<<<<<< Updated upstream
from users.request import create_new_user
from users import get_user_by_id, get_user_by_email
=======
from categories.request import get_all_categories, get_single_category
>>>>>>> Stashed changes

class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:

            param = resource.split("?")[1] 
            resource = resource.split("?")[0] 
            pair = param.split("=")
            key = pair[0]
            value = pair[1]

            return ( resource, key, value )

        else:
            id = None
            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)

        #one or two item urls a.k.a /resource or /resource/id
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "user":
                if id is not None:
                    response = f"{get_user_by_id(id)}"
                else:
                    response = ""
            elif resource == "post":
                if id is not None:
                    response = ""
                else:
                    response = ""
            elif resource == "comment":
                if id is not None:
                    response = ""
                else:
                    response = ""
            elif resource == "tag":
                if id is not None:
                    response = ""
                else:
                    response = ""
            elif resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"

        # three item url a.k.a `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key ) = parsed

<<<<<<< Updated upstream
            if key == "email" and resource == "user":
                response = f"{get_user_by_email(value)}"

=======
            if key == "post_id" and resource == "comment":
                response = ""
        
>>>>>>> Stashed changes
        self.wfile.write(response.encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        new_object = None
        if resource == "user":
            new_object = create_new_user(post_body)
        self.wfile.write(f"{new_object}".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "user":
            success = ""

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "user":
          print("")
            

        # Encode the new animal and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()
