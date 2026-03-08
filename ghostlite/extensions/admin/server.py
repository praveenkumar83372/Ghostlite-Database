from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class AdminPanel:

    def __init__(self, db, port=9000):
        self.db = db
        self.port = port

    def start(self):

        db = self.db

        class Handler(BaseHTTPRequestHandler):

            def do_GET(self):

                if self.path == "/":

                    with open("ghostlite/extensions/admin/index.html") as f:
                        html = f.read()

                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()

                    self.wfile.write(html.encode())

                elif self.path == "/tables":

                    tables = db.tables()

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    self.wfile.write(json.dumps(tables).encode())

                elif self.path.startswith("/table/"):

                    table = self.path.split("/")[-1]

                    data = db[table].all()

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    self.wfile.write(json.dumps(data).encode())

        server = HTTPServer(("localhost", self.port), Handler)

        print(f"👻 Admin panel running: http://localhost:{self.port}")

        server.serve_forever()