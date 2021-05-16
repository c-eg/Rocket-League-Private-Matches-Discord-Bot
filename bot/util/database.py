import sqlite3


class Database(object):
    def __init__(self, db_location):
        self.__db_location = db_location
        self.connection = sqlite3.connect(self.__db_location)
        self.cursor = self.connection.cursor()

    def __exit__(self):
        self.connection.commit()
        self.connection.close()

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(f'Exception: {e}')

    def create_tables(self, ddl_location):
        """Function to run the DDL for the database"""
        with open(ddl_location, "r") as ddl:
            self.connection.executescript(ddl.read())
