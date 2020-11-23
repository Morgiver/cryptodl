import sqlite3
from sqlite3 import Error


class Connector:
    def __init__(self, path):
        self.path = path
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)

    def create_table(self, request):
        self.cursor.execute(request)

    def select(self, request):
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def insert(self, request):
        self.cursor.execute(request)
        self.connection.commit()
        return None
