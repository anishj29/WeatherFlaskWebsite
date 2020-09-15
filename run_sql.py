import _sqlite3


class sql:
    def __init__(self):
        self.conn = _sqlite3.connect("email.db", check_same_thread=False)
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

    def get_by_email(self, email):
        self.c.execute("SELECT * FROM email WHERE email = ?", (email,))
        return self.c.fetchall()

    def get_by_location(self, location):
        self.c.execute("SELECT * FROM email WHERE location = ?", (location,))
        return self.c.fetchall()

    def update_email(self, new_email, old_email, location):
        self.c.execute("UPDATE email SET email = ? WHERE email = ? AND location = ?", (new_email, old_email, location))

    def update_location(self, new_location, old_location, email):
        self.c.execute("UPDATE email SET location = ? WHERE email = ? AND location = ?",
                       (new_location, email, old_location))

    def delete(self, email, location):
        self.c.execute("DELETE email WHERE email = ? AND location = ?",
                       (email, location))

    def close(self):
        self.conn.close()

# s = sql()
# print(s.get_all())
# mysql.create_table()    No need to create again when already created
# mysql.commit()
# mysql.insert('varunk3249@gmail.com', 'Princeton')
# mysql.commit()
#
# for i in range(0, len(x)):
#     for j in range(0, 2):
#         print(x[i][j])  # prints out email and city for each person in database
# will add program to send email to people when ran
