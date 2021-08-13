import sqlite3

with sqlite3.connect("ManyMusic.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
userID INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
password VARCHAR(20)NOT NULL);
""")

cursor.execute("""
INSERT INTO Users(username,password)
VALUES("andrew1","password4")
""")
db.commit()

cursor.execute("SELECT * FROM Users")
print(cursor.fetchall())
