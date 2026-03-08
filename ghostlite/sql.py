import re


class SQLParser:

    def parse(self, query):

        query = query.strip()

        # ---------------- SELECT ----------------

        select = re.match(
            r"SELECT\s+\*\s+FROM\s+(\w+)(?:\s+WHERE\s+(\w+)=([^\s]+))?(?:\s+LIMIT\s+(\d+))?",
            query,
            re.IGNORECASE
        )

        if select:

            table = select.group(1)

            where = None
            limit = None

            if select.group(2):
                where = {select.group(2): select.group(3)}

            if select.group(4):
                limit = int(select.group(4))

            return {
                "type": "SELECT",
                "table": table,
                "where": where,
                "limit": limit
            }

        # ---------------- CREATE TABLE ----------------

        create = re.match(
            r"CREATE\s+TABLE\s+(\w+)",
            query,
            re.IGNORECASE
        )

        if create:

            return {
                "type": "CREATE",
                "table": create.group(1)
            }

        # ---------------- DELETE ----------------

        delete = re.match(
            r"DELETE\s+FROM\s+(\w+)\s+WHERE\s+(\w+)=([^\s]+)",
            query,
            re.IGNORECASE
        )

        if delete:

            return {
                "type": "DELETE",
                "table": delete.group(1),
                "where": {delete.group(2): delete.group(3)}
            }

        # ---------------- UPDATE ----------------

        update = re.match(
            r"UPDATE\s+(\w+)\s+SET\s+(\w+)=([^\s]+)\s+WHERE\s+(\w+)=([^\s]+)",
            query,
            re.IGNORECASE
        )

        if update:

            return {
                "type": "UPDATE",
                "table": update.group(1),
                "set": {update.group(2): update.group(3)},
                "where": {update.group(4): update.group(5)}
            }

        # ---------------- SHOW TABLES ----------------

        if query.upper() == "SHOW TABLES":

            return {
                "type": "SHOW"
            }

        return {}