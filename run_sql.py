import mysql.connector


class MySQL:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="us-cdbr-east-02.cleardb.com",
            user="b0317e5f6ea3eb",
            password="7eb9f9ac",
            database="heroku_a0ac72f314d32a7"
        )
        self.cursor = self.db.cursor()

    def get_databases(self):
        self.cursor.execute("SHOW DATABASES")
        for db in self.cursor:
            print(db)

    def create_table(self):
        self.cursor.execute("CREATE TABLE subscribers (email VARCHAR(255), location VARCHAR(255 ))")

    def view_table(self):
        self.cursor.execute("SHOW TABLES")

        for tb in self.cursor:
            print(tb)

    def insert(self, email, location):
        self.cursor.execute("INSERT INTO subscribers (email, location) VALUES (%s, %s)", (email, location))

    def insert_multiple(self, values):
        self.cursor.executemany("INSERT INTO subscribers (email, location) VALUES (%s, %s)", values)

    def get_all(self):
        self.cursor.execute("SELECT * FROM subscribers")
        return self.cursor.fetchall()

    def get_emails(self):
        self.cursor.execute("SELECT email FROM subscribers")
        return self.cursor.fetchall()

    def get_locations(self):
        self.cursor.execute("SELECT location FROM subscribers")
        return self.cursor.fetchall()

    def get_a_email(self, email):
        self.cursor.execute("SELECT * FROM subscribers WHERE email = %s", email)
        return self.cursor.fetchall()

    def get_a_location(self, location):
        self.cursor.execute("SELECT * FROM subscribers WHERE location = %s", location)
        return self.cursor.fetchall()

    def get_like(self, is_email, wildcard):
        if is_email:
            self.cursor.execute("SELECT * FROM subscribers WHERE email LIKE %s", wildcard)
        else:
            self.cursor.execute("SELECT * FROM subscribers WHERE location LIKE %s", wildcard)

        return self.cursor.fetchall()

    def delete_row(self, email):
        self.cursor.execute("DELETE FROM subscribers WHERE email = %s", email)

    def __delete_table__(self):
        self.cursor.execute("DROP TABLE IF EXISTS subscribers")

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()


# s = MySQL()
# print(s.get_all())
# s.close()
