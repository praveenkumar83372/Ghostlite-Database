class TransactionManager:

    def __init__(self):
        self.active = False
        self.operations = []

    def begin(self):
        self.active = True
        self.operations = []

    def add(self, operation):
        if self.active:
            self.operations.append(operation)

    def commit(self):
        self.active = False
        self.operations = []

    def rollback(self):
        self.active = False
        self.operations = []