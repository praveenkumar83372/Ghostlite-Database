import ghostlite


class GhostShell:

    def __init__(self):
        self.db = None

    def start(self):

        print("👻 Ghostlite Interactive Shell")
        print("Type HELP for commands")

        while True:

            cmd = input("ghostlite> ").strip()

            if not cmd:
                continue

            cmd_upper = cmd.upper()

            if cmd_upper == "EXIT":
                print("Bye 👋")
                break

            elif cmd_upper == "HELP":
                self.help()

            elif cmd_upper.startswith("OPEN"):
                self.open_db(cmd)

            elif cmd_upper.startswith("SELECT"):
                self.run_query(cmd)

            elif cmd_upper.startswith("INSERT"):
                self.insert(cmd)

            elif cmd_upper.startswith("CREATE"):
                self.run_query(cmd)

            elif cmd_upper.startswith("DELETE"):
                self.run_query(cmd)

            elif cmd_upper.startswith("UPDATE"):
                self.run_query(cmd)

            elif cmd_upper == "SHOW TABLES":
                self.show_tables()

            else:
                print("Unknown command")

    # --------------------
    # Open database
    # --------------------

    def open_db(self, cmd):

        parts = cmd.split()

        if len(parts) < 2:
            print("Usage: OPEN <dbname>")
            return

        name = parts[1]

        self.db = ghostlite.open(name)

        print(f"Database '{name}' opened")

    # --------------------
    # Run SQL query
    # --------------------

    def run_query(self, sql):

        if not self.db:
            print("Open a database first")
            return

        try:
            result = self.db.query(sql)
            print(result)
        except Exception as e:
            print("Query error:", e)

    # --------------------
    # Insert command
    # --------------------

    def insert(self, cmd):

        if not self.db:
            print("Open a database first")
            return

        try:

            parts = cmd.split()

            table = parts[1]

            data = {}

            for item in parts[2:]:

                key, value = item.split("=")

                try:
                    value = int(value)
                except:
                    pass

                data[key] = value

            self.db[table].insert(**data)

            print("Inserted")

        except:
            print("Insert syntax error")

    # --------------------
    # Show tables
    # --------------------

    def show_tables(self):

        if not self.db:
            print("Open a database first")
            return

        print(self.db.tables())

    # --------------------
    # Help
    # --------------------

    def help(self):

        print("""
Commands:

OPEN <dbname>

CREATE TABLE users
SHOW TABLES

SELECT * FROM users
SELECT * FROM users WHERE age = 25 LIMIT 5

INSERT users name=Bob age=30

UPDATE users SET age=30 WHERE name=Alice
DELETE FROM users WHERE age=30

HELP
EXIT
""")