# DB connector to aws rds
# url receiptapp.crjjkt9g1zem.eu-north-1.rds.amazonaws.com
# port 5432
# username postgres
# password ?4}]1[T+GX9{
import psycopg2

class DBConnector:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host="receiptapp.crjjkt9g1zem.eu-north-1.rds.amazonaws.com",
                port="5432",
                database="postgres",
                user="postgres",
                password="?4}]1[T+GX9{"
            )
            self.cursor = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            self.cursor.close()

    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.disconnect()
            self.connect()
            self.cursor.execute(query, params)
            self.conn.commit()

    def fetch(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.disconnect()
            self.connect()
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
