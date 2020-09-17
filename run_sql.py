import mysql.connector
#
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="boldtanswans",
#     database="users"
# )
#
# print(mydb)
# cursor = mydb.cursor()
#
# cursor.execute("SHOW TABLES")
#
# for tb in cursor:
#     print(tb)
#
# sql_formula = "INSERT INTO subscribers (email, location) VALUES (%s, %s)"
# cursor.execute("SELECT * FROM subscribers")
# my_result = cursor.fetchall()
# print(my_result)
# # mydb.commit()
# for row in my_result:
#     print(row)


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
        self.cursor.execute("SELECT * FROM subscribers WHERE email = ?", (email,))
        return self.cursor.fetchall()

    def get_a_location(self, location):
        self.cursor.execute("SELECT * FROM subscribers WHERE location = ?", (location,))
        return self.cursor.fetchall()

    def get_like(self, is_email, wildcard):
        if is_email:
            self.cursor.execute("SELECT * FROM subscribers WHERE email LIKE ?", (wildcard,))
        else:
            self.cursor.execute("SELECT * FROM subscribers WHERE location LIKE ?", (wildcard,))

        return self.cursor.fetchall()

    # def delete(self, email):
    #     self.cursor.execute("DELETE FROM subscribers WHERE email = ?", (email,))

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()


s = MySQL()
# print(s.create_table())
# s.insert("niranjanbk@gmail.com", "East Windsor")
# s.commit()
# s.delete('varunk3149@gmail.com')
print(s.get_all())

# from firebase import firebase
#
#
# class firebaseEmail:
#     def __init__(self):
#         self.firebase = firebase.FirebaseApplication('https://weather-flask-5973f.firebaseio.com/', None)
#
#     def insert(self, email, location):
#         data = {
#             'Email': email,
#             'Location': location
#         }
#         self.firebase.post('/email', data)
#
#     def get_all(self):
#         return self.firebase.get('/email', '')
#
#     def delete(self, email):
#         self.firebase.delete('/email', email)

# s = firebaseEmail()
# # s.update_email('anishwestwindsor@gmail.com', 'a@gmail.com')
# print(s.get_all())


# class sql:
#     def __init__(self):
#         self.conn = _sqlite3.connect("email.db", check_same_thread=False)
#         self.c = self.conn.cursor()
#
#     def create_table(self):
#         self.c.execute("CREATE TABLE email (email text, location text)")
#
#     def insert(self, email, location):
#         self.c.execute("INSERT INTO email VALUES (?, ?)", (email, location))
#
#     def commit(self):
#         self.conn.commit()
#
#     def get_all(self):
#         self.c.execute("SELECT * FROM email")
#         return self.c.fetchall()
#
#     def get_by_email(self, email):
#         self.c.execute("SELECT * FROM email WHERE email = ?", (email,))
#         return self.c.fetchall()
#
#     def get_by_location(self, location):
#         self.c.execute("SELECT * FROM email WHERE location = ?", (location,))
#         return self.c.fetchall()
#
#     def update_email(self, new_email, old_email):
#         self.c.execute("UPDATE email SET email = ? WHERE email = ?", (new_email, old_email))
#
#     def update_location(self, new_location, email):
#         self.c.execute("UPDATE email SET location = ? WHERE email = ?",
#                        (new_location, email))
#
#     def update(self, new_email, old_email, new_location):
#         self.c.execute("UPDATE email SET email = ? WHERE email = ?", (new_email, old_email))
#         self.c.execute("UPDATE email SET location = ? WHERE email = ?",
#                        (new_location, new_email))
#
#     def get_latest(self):
#         self.c.execute("SELECT * FROM email ORDER BY email DESC LIMIT 1")
#         return self.c.fetchall()
#
#     def delete(self, email, location):
#         self.c.execute("DELETE FROM email WHERE email = ? AND location = ?",
#                        (email, location))
#
#     def close(self):
#         self.conn.close()
#
#
# s = sql()
# # s.delete('varunk3249@gmail.com', 'Brooklyn')
# #
# # # # # mysql.insert('varunk3249@gmail.com', 'Princeton')
# # # # s.update_email('john', 'pizza', 'Ocean City')
# # s.commit()
# # s.delete('e new', 'loc new')
# # # s.commit()
# print(s.get_all())
# # s.close()
#
#
# # for i in range(0, len(x)):
# #     for j in range(0, 2):
# #         print(x[i][j])  # prints out email and city for each person in database
# # will add program to send email to people when ran