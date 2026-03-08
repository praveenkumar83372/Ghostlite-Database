class QueryOptimizer:

    def __init__(self):
        self.query_stats = {}

    def track(self, field):

        if field not in self.query_stats:
            self.query_stats[field] = 0

        self.query_stats[field] += 1

    def should_index(self, field):

        return self.query_stats.get(field, 0) >= 3