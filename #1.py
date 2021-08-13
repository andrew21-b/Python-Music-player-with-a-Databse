import time
import sqlite3 as lite
from sqlite3 import Error
import tkinter as tk
from glob import glob
import sqlite3

def login():
    for i in range(3):
        username=input("please enter your usernanme: ")
        password=input("please enter your password: ")
        with sqlite3.connect("manymusic.db") as db:
            cursor = db.cursor()
        findUser = ("SELECT * FROM Users WHERE username = ? AND password = ? ")
        cursor.execute(findUser,[(username),(password)])
        results = cursor.fetchall()                                                     #this function asks for the user's input and vcalidates to the database's version to grant the user acess to the program

        if results:
            for i in results:
                print("welcome "+i[1])
            #return("exit")
            break
        else:
            print("username and password not recognised")
            again = input("Do you want to try again? (y/n): ")
            if again.lower() == "n":
                print("goodbye")
                time.sleep(1)
                #return("exit")
                break

def newUser():
    found = 0
    while found ==0:
        username = input("Please enter a username: ")
        with sqlite3.connect("manymusic.db") as db:
            cursor = db.cursor()
        findUser= ("SELECT * FROM Users WHERE username = ?")
        cursor.execute(findUser,[(username)])

        if cursor.fetchall():
            print("Username taken, please try again")
        else:                                                  #This function registers a new user, it asks for a username and checks if it alreday exists in the database then it asks for a password and confirms it
            found = 1

    password = input("please enter your password: ")
    password1 = input("please reneter your password: ")
    while password != password1:
        print("your passwords did not match. please try again")
        password = input("please enter your password: ")
        password1 = input("please reneter your password: ")
    insertData = '''INSERT INTO Users(username,password)
    VALUES(?,?)'''
    cursor.execute(insertData,[(username),(password)])
    db.commit()

#newUser()
def querey():
    conn = sqlite3.connect("ManyMusicDB.db")
    c = conn.cursor()
    username = input("enter your usernaem")
    findUser_id = ("SELECT user_id FROM users WHERE username = ?")
    c.execute(findUser_id, [(username)])
    rows = c.fetchall()
    for row in rows:
        res = int(''.join(map(str, row)))
        print(res)

    conn.commit()
    conn.close()
    querey1()
#querey()



def querey1():
    conn = sqlite3.connect("ManyMusicDB.db")
    c = conn.cursor()
    findgenre = ("SELECT songs.song_title,favourites.song_id From songs INNER JOIN favourites ON songs.ong_id ")
    c.execute(findgenre, [(1)])
    rowsz = c.fetchall()
    for rowsy in rowsz:
        print(rowsy)

    conn.commit()
    conn.close()
querey1()






# def create(obj):
#     db = obj.e.get()
#
#     if db[-3] == ".db":
#         pass
#     else:
#         db = db + ".db"
#     try:
#         conn = lite.connect(db)
#         return conn
#     except Error as e:
#         print(e)
#     finally:
#         conn.close()
#         obj.lb.insert(tk.END, db)
#         obj.db.set("")


# class Window:
#     """Creates the widgets of the window"""
#
#     def __init__(self):
#         self.win = tk.Tk()
#         self.label()
#         self.entry()
#         self.button()
#         self.listbox()
#
#     def label(self):
#         self.l = tk.Label(self.win, text="Create a db [insert the name]")
#         self.l.pack()
#
#     def entry(self):
#         self.db = tk.StringVar()
#         self.e = tk.Entry(self.win, textvariable=self.db)
#         self.e.pack()
#
#     def button(self):
#         self.b = tk.Button(self.win, text="Create DB", command=lambda: create(self))
#         self.b.pack()
#
#     def listbox(self):
#         self.lb = tk.Listbox(self.win)
#         self.lb.pack()
#         self.show_db()
#
#     def show_db(self):
#         for file in glob("*.db"):
#             self.lb.insert(tk.END, file)
#
#         self.win.mainloop()


#win = Window()



