from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class DashboardServer:

    def __init__(self, db, port=8080):

        self.db = db
        self.port = port

    def start(self):

        db = self.db

        class Handler(BaseHTTPRequestHandler):

            def do_GET(self):

                # Homepage
                if self.path == "/":

                    tables = db.tables()

                    html = "<h1> Ghostlite Dashboard</h1>"
                    html += "<h2>Tables</h2><ul>"

                    for t in tables:
                        html += f"<li><a href='/table/{t}'>{t}</a></li>"

                    html += "</ul>"

                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()

                    self.wfile.write(html.encode())

                # Table data
                elif self.path.startswith("/table/"):

                    table = self.path.split("/")[-1]

                    data = db[table].all()

                    html = f"<h1>Table: {table}</h1>"

                    if not data:
                        html += "<p>No records</p>"
                    else:

                        html += "<table border='1'><tr>"

                        for col in data[0].keys():
                            html += f"<th>{col}</th>"

                        html += "</tr>"

                        for row in data:

                            html += "<tr>"

                            for val in row.values():
                                html += f"<td>{val}</td>"

                            html += "</tr>"

                        html += "</table>"

                    html += "<br><a href='/'>⬅ Back</a>"

                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()

                    self.wfile.write(html.encode())

        server = HTTPServer(("localhost", self.port), Handler)

        print(f"🌐 Dashboard running at http://localhost:{self.port}")

        server.serve_forever()