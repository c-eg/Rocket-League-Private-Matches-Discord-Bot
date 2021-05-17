# -*- coding: utf-8 -*-
import sqlite3


class Database(object):
    def __init__(self, db_location):
        self.__db_location = db_location
        self.connection = sqlite3.connect(self.__db_location)
        self.cursor = self.connection.cursor()

    def __exit__(self):
        self.connection.commit()
        self.connection.close()

    def create_tables(self, ddl_location):
        """Function to run the DDL for the database"""
        with open(ddl_location, "r") as ddl:
            try:
                self.cursor.execute(ddl.read())
                self.connection.commit()
            except Exception as e:
                print(f'Exception: {e}')
