import requests


class GhostCluster:

    def __init__(self, db):

        self.db = db
        self.nodes = []

    def add_node(self, url):

        self.nodes.append(url)

    def sync_insert(self, table, data):

        for node in self.nodes:

            requests.post(
                f"{node}/replicate_insert",
                json={"table": table, "data": data}
            )