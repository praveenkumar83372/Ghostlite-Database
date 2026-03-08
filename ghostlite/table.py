import os
import json
import builtins
from datetime import datetime
from .query import GhostQuery
from .transaction import TransactionManager


CHUNK_SIZE = 5


class GhostTable:

    def __init__(self, db_path, name):

        self.name = name
        self.db_path = db_path

        self.table_path = os.path.join(db_path, name)
        self.index_file = os.path.join(db_path, f"{name}_index.json")
        self.wal_file = os.path.join(db_path, "wal.log")

        os.makedirs(self.table_path, exist_ok=True)

        # create index file if not exists
        if not os.path.exists(self.index_file):

            with builtins.open(self.index_file, "w") as f:
                json.dump({}, f)

        # create wal file if not exists
        if not os.path.exists(self.wal_file):

            with builtins.open(self.wal_file, "w") as f:
                json.dump([], f)

    # ----------------------------
    # WAL helpers
    # ----------------------------

    def _wal_log(self, action, data):

        with builtins.open(self.wal_file, "r") as f:
            logs = json.load(f)

        logs.append({
            "action": action,
            "data": data
        })

        with builtins.open(self.wal_file, "w") as f:
            json.dump(logs, f, indent=2)

    def _wal_clear(self):

        with builtins.open(self.wal_file, "w") as f:
            json.dump([], f)

    # ----------------------------
    # Chunk helpers
    # ----------------------------

    def _chunk_files(self):

        return sorted([
            f for f in os.listdir(self.table_path)
            if f.endswith(".json")
        ])

    def _read_chunk(self, file):

        with builtins.open(os.path.join(self.table_path, file), "r") as f:
            return json.load(f)

    def _write_chunk(self, file, data):

        with builtins.open(os.path.join(self.table_path, file), "w") as f:
            json.dump(data, f, indent=2)

    def _all_records(self):

        records = []

        for chunk in self._chunk_files():

            records.extend(self._read_chunk(chunk))

        return records

    # ----------------------------
    # Index helpers
    # ----------------------------

    def _read_index(self):

        with builtins.open(self.index_file, "r") as f:
            return json.load(f)

    def _write_index(self, data):

        with builtins.open(self.index_file, "w") as f:
            json.dump(data, f, indent=2)

    # ----------------------------
    # Insert
    # ----------------------------

    def insert(self, **data):

        data["_created"] = datetime.now().isoformat()

        # write ahead log
        self._wal_log("insert", data)

        chunks = self._chunk_files()

        if not chunks:

            chunk_name = "chunk0.json"

            self._write_chunk(chunk_name, [data])

        else:

            last_chunk = chunks[-1]

            records = self._read_chunk(last_chunk)

            if len(records) >= CHUNK_SIZE:

                new_chunk = f"chunk{len(chunks)}.json"

                self._write_chunk(new_chunk, [data])

            else:

                records.append(data)

                self._write_chunk(last_chunk, records)

        # clear WAL after success
        self._wal_clear()

        return data

    # ----------------------------
    # Create index
    # ----------------------------

    def create_index(self, field):

        records = self._all_records()

        index = {}

        for i, r in enumerate(records):

            value = r.get(field)

            if value is not None:

                if str(value) not in index:
                    index[str(value)] = []

                index[str(value)].append(i)

        self._write_index({field: index})

        print(f"Index created on '{field}'")

    # ----------------------------
    # Find
    # ----------------------------

    def find(self, **filters):

        records = self._all_records()

        if not filters:
            return records

        result = []

        for r in records:

            match = True

            for k, v in filters.items():

                if r.get(k) != v:
                    match = False
                    break

            if match:
                result.append(r)

        return result

    # ----------------------------
    # Query Builder
    # ----------------------------

    def where(self, **filters):

        return GhostQuery(self).where(**filters)

    # ----------------------------
    # Get all records
    # ----------------------------

    def all(self):

        return self._all_records()