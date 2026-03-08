from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse


class APIServer:

    def __init__(self, db, port=5000):
        self.db = db
        self.port = port

    def start(self):

        db = self.db

        class Handler(BaseHTTPRequestHandler):

            def do_GET(self):

                try:

                    parsed = urllib.parse.urlparse(self.path)
                    path = parsed.path
                    params = urllib.parse.parse_qs(parsed.query)

                    # -------------------------
                    # Homepage
                    # -------------------------

                    if path == "/":

                        data = {
                            "service": "Ghostlite API",
                            "endpoints": [
                                "/tables",
                                "/table/<name>",
                                "/query?sql=SELECT * FROM table"
                            ]
                        }

                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        self.wfile.write(json.dumps(data).encode())

                    # -------------------------
                    # List tables
                    # -------------------------

                    elif path == "/tables":

                        tables = db.tables()

                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        self.wfile.write(json.dumps({"tables": tables}).encode())

                    # -------------------------
                    # Table data
                    # -------------------------

                    elif path.startswith("/table/"):

                        table = path.split("/")[-1]

                        data = db[table].all()

                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        self.wfile.write(json.dumps(data).encode())

                    # -------------------------
                    # SQL query
                    # -------------------------

                    elif path == "/query":

                        sql = urllib.parse.unquote(params.get("sql", [""])[0])

                        result = db.query(sql)

                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        self.wfile.write(json.dumps(result).encode())

                    else:

                        self.send_response(404)
                        self.end_headers()

                except Exception as e:

                    self.send_response(500)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()

                    self.wfile.write(
                        json.dumps({"error": str(e)}).encode()
                    )

        server = HTTPServer(("localhost", self.port), Handler)

        print(f"🚀 Ghostlite API running at http://localhost:{self.port}")

        server.serve_forever()