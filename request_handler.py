import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from tags import get_all_tags, get_tag_by_id, create_new_tag, update_tag, delete_tag
from users import get_user_by_id, get_user_by_email, create_new_user, delete_user, update_user
from posts import get_all_posts, get_single_post, create_post, update_post, delete_post
from categories.request import delete_category, get_all_categories, get_single_category, create_category, update_category
from comments.request import get_all_comments, get_single_comment, get_comment_by_post_id

class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
       
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
                pass
            except ValueError:
                pass
            return (resource, id)

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

    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)
      
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "user":
                if id is not None:
                    response = f"{get_user_by_id(id)}"
                else:
                    response = ""
            elif resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
            elif resource == "comment":
                if id is not None:
                    response = f"{get_single_comment(id)}"
                else:
<<<<<<< Updated upstream
                    response = ""
            elif resource == "tags":
=======
                    response = f"{get_all_comments()}"
            elif resource == "tag":
>>>>>>> Stashed changes
                if id is not None:
                    response = f"{get_tag_by_id(id)}"
                else:
                    response = f"{get_all_tags()}"
            elif resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
      
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            if key == "email" and resource == "user":
                response = f"{get_user_by_email(value)}"
            if key == "post_id" and resource == "comments":
                response = f"{get_comment_by_post_id(value)}"

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
        elif resource == "posts":
            new_object = create_post(post_body)
        elif resource == "categories":
            new_object = create_category(post_body)
        elif resource == "tags":
            new_object = create_new_tag(post_body)
        self.wfile.write(f"{new_object}".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
       
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "user":
            success = ""
        elif resource == "posts":
            success = update_post(id, post_body)
        elif resource == "categories":
            success = update_category(id, post_body)
        elif resource == "tags":
            success = update_tag(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "user":
            delete_user(id)
        elif resource == "posts":
            delete_post(id)          
        elif resource == "categories":
          delete_category(id)
        elif resource == "tags":
          delete_tag(id)

        self.wfile.write("".encode())

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()
    
if __name__ == "__main__":
    main()
