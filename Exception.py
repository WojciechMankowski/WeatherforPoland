
class DatabaseConnectionStatusException(Exception):
    def __init__(self):
        super(DatabaseConnectionStatusException, self).__init__("Program na potkał problem")