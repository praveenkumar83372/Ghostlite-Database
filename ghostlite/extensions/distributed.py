import requests
import json
import time


class DistributedNode:

    def __init__(self, db, peers):

        self.db = db
        self.peers = peers
        self.last_sync = 0

    def push(self):

        data = {}

        for table in self.db.tables():

            data[table] = self.db[table].all()

        for peer in self.peers:

            try:

                requests.post(
                    peer + "/sync",
                    json=data,
                    timeout=2
                )

                print("🔄 Synced with", peer)

            except:

                print("⚠️ Peer offline:", peer)

    def pull(self):

        for peer in self.peers:

            try:

                r = requests.get(peer + "/pull")

                remote = r.json()

                for table, rows in remote.items():

                    t = self.db[table]

                    for row in rows:

                        t.insert(**row)

                print("⬇ Pulled data from", peer)

            except:

                pass

    def start(self):

        print("🌐 Distributed mode started")

        while True:

            self.push()

            self.pull()

            time.sleep(5)