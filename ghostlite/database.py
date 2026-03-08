import os
import json
import builtins

from .table import GhostTable
from .transaction import TransactionManager
from .sql import SQLParser
from .optimizer import QueryOptimizer

# optional extensions
from .extensions.search import FullTextSearch
from .extensions.dashboard import DashboardServer
from .extensions.api import APIServer
from .extensions.admin.server import AdminPanel
from .extensions.distributed import DistributedNode


class GhostDB:

    def __init__(self, name):

        self.name = name

        # database root folder
        self.base = os.path.join(os.getcwd(), ".ghostlite", name)

        os.makedirs(self.base, exist_ok=True)

        # core systems
        self.transaction = TransactionManager()
        self.optimizer = QueryOptimizer()

        # optional systems
        self.search_engine = None
        self.dashboard = None
        self.api_server = None
        self.admin_panel = None
        self.cluster = None

    # ----------------------------------
    # Table Access
    # ----------------------------------

    def __getitem__(self, table_name):

        return GhostTable(self.base, table_name)

    # ----------------------------------
    # Transactions
    # ----------------------------------

    def begin(self):

        print("🔒 Transaction started")
        self.transaction.begin()

    def commit(self):

        print("✅ Transaction committed")
        self.transaction.commit()

    def rollback(self):

        print("↩ Transaction rolled back")
        self.transaction.rollback()

    # ----------------------------------
    # Enable Full Text Search
    # ----------------------------------

    def enable_search(self):

        self.search_engine = FullTextSearch(self)

        print("🔎 Full-Text Search enabled")

    def search(self, table, keyword):

        if not self.search_engine:
            raise Exception("Search engine not enabled")

        self.search_engine.index_table(table)

        return self.search_engine.search(table, keyword)

    # ----------------------------------
    # Enable Web Dashboard
    # ----------------------------------

    def enable_dashboard(self, port=8080):

        self.dashboard = DashboardServer(self, port)

        print("🌐 Starting Ghostlite dashboard...")

        self.dashboard.start()

    # ----------------------------------
    # Enable REST API Server
    # ----------------------------------

    def enable_api(self, port=5000):

        self.api_server = APIServer(self, port)

        print("🚀 Starting Ghostlite API server...")

        self.api_server.start()

    # ----------------------------------
    # Enable Admin Panel
    # ----------------------------------

    def enable_admin(self, port=9000):

        self.admin_panel = AdminPanel(self, port)

        print("👻 Starting Ghostlite Admin Panel...")

        self.admin_panel.start()

    # ----------------------------------
    # Enable Distributed Mode
    # ----------------------------------

    def enable_cluster(self, peers):

        self.cluster = DistributedNode(self, peers)

        print("🌐 Ghostlite Distributed Mode enabled")

        self.cluster.start()

    # ----------------------------------
    # SQL Query Engine
    # ----------------------------------

    def query(self, sql):

        parser = SQLParser()

        parsed = parser.parse(sql)

        qtype = parsed.get("type")

        if not qtype:
            return {"error": "Invalid SQL query"}

        # -------- SELECT --------

        if qtype == "SELECT":

            table = self[parsed["table"]]

            records = table.all()

            if parsed.get("where"):

                key = list(parsed["where"].keys())[0]
                value = parsed["where"][key]

                # optimizer tracking
                self.optimizer.track(key)

                # auto index creation
                if self.optimizer.should_index(key):

                    try:
                        table.create_index(key)
                    except:
                        pass

                records = [
                    r for r in records if str(r.get(key)) == value
                ]

            if parsed.get("limit"):

                records = records[:parsed["limit"]]

            return records

        # -------- CREATE TABLE --------

        if qtype == "CREATE":

            table = parsed["table"]

            self[table]

            return {"message": f"Table '{table}' created"}

        # -------- DELETE --------

        if qtype == "DELETE":

            table = self[parsed["table"]]

            records = table.all()

            key = list(parsed["where"].keys())[0]
            value = parsed["where"][key]

            remaining = [
                r for r in records if str(r.get(key)) != value
            ]

            table._write_chunk("chunk0.json", remaining)

            return {"message": "Records deleted"}

        # -------- UPDATE --------

        if qtype == "UPDATE":

            table = self[parsed["table"]]

            records = table.all()

            where_key = list(parsed["where"].keys())[0]
            where_val = parsed["where"][where_key]

            set_key = list(parsed["set"].keys())[0]
            set_val = parsed["set"][set_key]

            for r in records:

                if str(r.get(where_key)) == where_val:

                    r[set_key] = set_val

            table._write_chunk("chunk0.json", records)

            return {"message": "Records updated"}

        # -------- SHOW TABLES --------

        if qtype == "SHOW":

            return {"tables": self.tables()}

        return {"error": "Unsupported query"}

    # ----------------------------------
    # List Tables
    # ----------------------------------

    def tables(self):

        tables = []

        for item in os.listdir(self.base):

            path = os.path.join(self.base, item)

            if os.path.isdir(path):

                tables.append(item)

        return tables

    # ----------------------------------
    # Count Records
    # ----------------------------------

    def _count_records(self, table):

        table_path = os.path.join(self.base, table)

        total = 0

        for file in os.listdir(table_path):

            if file.endswith(".json"):

                with builtins.open(os.path.join(table_path, file)) as f:

                    data = json.load(f)

                total += len(data)

        return total

    # ----------------------------------
    # Database Stats
    # ----------------------------------

    def stats(self):

        tables = self.tables()

        total_records = 0

        for table in tables:

            total_records += self._count_records(table)

        return {
            "database": self.name,
            "tables": len(tables),
            "records": total_records
        }