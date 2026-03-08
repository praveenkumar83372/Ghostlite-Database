class GhostQuery:

    CACHE = {}

    def __init__(self, table):

        self.table = table
        self.filters = {}
        self.limit_count = None
        self.order_field = None

    def where(self, **filters):

        self.filters = filters
        return self

    def limit(self, count):

        self.limit_count = count
        return self

    def order_by(self, field):

        self.order_field = field
        return self

    def _cache_key(self):

        return str(self.filters) + str(self.limit_count) + str(self.order_field)

    def execute(self):

        key = self._cache_key()

        # -----------------------
        # Cache lookup
        # -----------------------

        if key in GhostQuery.CACHE:

            print("⚡ Cache hit")

            return GhostQuery.CACHE[key]

        print("🔍 Executing query")

        records = self.table._all_records()

        # -----------------------
        # Filtering
        # -----------------------

        if self.filters:

            filtered = []

            for r in records:

                match = True

                for k, v in self.filters.items():

                    if r.get(k) != v:

                        match = False
                        break

                if match:

                    filtered.append(r)

            records = filtered

        # -----------------------
        # Sorting
        # -----------------------

        if self.order_field:

            records = sorted(records, key=lambda x: x.get(self.order_field))

        # -----------------------
        # Limit
        # -----------------------

        if self.limit_count:

            records = records[:self.limit_count]

        # -----------------------
        # Cache store
        # -----------------------

        GhostQuery.CACHE[key] = records

        return records