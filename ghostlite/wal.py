import os
import json
import builtins


class WriteAheadLog:

    def __init__(self, db_path):

        self.log_file = os.path.join(db_path, "wal.log")

        if not os.path.exists(self.log_file):

            with builtins.open(self.log_file, "w") as f:
                json.dump([], f)

    def log(self, action, data):

        with builtins.open(self.log_file, "r") as f:
            logs = json.load(f)

        logs.append({
            "action": action,
            "data": data
        })

        with builtins.open(self.log_file, "w") as f:
            json.dump(logs, f, indent=2)

    def clear(self):

        with builtins.open(self.log_file, "w") as f:
            json.dump([], f)