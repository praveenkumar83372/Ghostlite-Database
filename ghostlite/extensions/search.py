class FullTextSearch:

    def __init__(self, db):

        self.db = db
        self.index = {}

    def index_table(self, table):

        records = self.db[table].all()

        for pos, r in enumerate(records):

            for value in r.values():

                word = str(value).lower()

                if word not in self.index:
                    self.index[word] = []

                self.index[word].append((table, pos))

    def search(self, table, keyword):

        keyword = keyword.lower()

        results = []

        if keyword not in self.index:
            return results

        records = self.db[table].all()

        for t, pos in self.index[keyword]:

            if t == table:

                results.append(records[pos])

        return results