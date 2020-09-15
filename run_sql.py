import _sqlite3


class sql:
    def __init__(self):
        self.conn = _sqlite3.connect("email.db")
        self.c = self.conn.cursor()

    def create_table(self):
        self.c.execute("CREATE TABLE email (email text, location text)")

    def insert(self, email, location):
        self.c.execute("INSERT INTO email VALUES (?, ?)", (email, location))

    def commit(self):
        self.conn.commit()

    def get_all(self):
        self.c.execute("SELECT * FROM email")
        return self.c.fetchall()

    def close(self):
        self.conn.close()


mysql = sql()
# mysql.create_table()    No need to create again when already created
# mysql.commit()
# mysql.insert('varunk3249@gmail.com', 'Princeton')
# mysql.commit()
x = mysql.get_all()
mysql.close()

for i in range(0, len(x)):
    for j in range(0, 2):
        print(x[i][j])  # prints out email and city for each person in database
        # will add program to send email to people when ran
