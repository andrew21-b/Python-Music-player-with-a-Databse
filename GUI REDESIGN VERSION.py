import os
import pickle
import sqlite3
import threading
import time
import tkinter as tk
from tkinter import *  # the modules needed to use the libaries
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from mutagen.mp3 import MP3
from pygame import mixer
from ttkthemes import themed_tk as tk


def main():  # this defines the program to make the windows
    root = tk.ThemedTk()
    root.configure(bg="#423f3e")
    root.get_themes()  # Returns a list of all themes that can be set
    root.set_theme("equilux")
    mixer.init()
    app = loginWindow(root)
    root.mainloop()


class loginWindow:  # this class holds the GUI for the login window
    def __init__(self, master):
        loginFrame = Frame(master)
        self.master = master
        self.master.title("ManyMusic Login")
        self.master.geometry('300x300')
        loginFrame.configure(bg="#423f3e")
        loginFrame.pack(expand=True)

        # lines 17-18 convert the data to a string
        self.usernameStr = StringVar()
        self.passwordStr = StringVar()

        # lines 14-17 place the text for username and password in the GUI
        self.lblUsername = ttk.Label(loginFrame, text='Username', font=("Helvetica", 12))
        self.lblUsername.grid(row=0, column=0, ipady=5)
        self.lblpassword = ttk.Label(loginFrame, text='Password', font=("Helvetica", 12))
        self.lblpassword.grid(row=1, column=0, ipady=5)

        # Lines 20-24 put the entry box in the GUI
        self.inpUsername = ttk.Entry(loginFrame, textvariable=self.usernameStr, width=30)
        self.inpUsername.grid(row=0, column=1, ipady=5, padx=5)
        self.inpPassword = ttk.Entry(loginFrame, textvariable=self.passwordStr, width=30, show="*")
        self.inpPassword.grid(row=1, column=1, ipady=5, padx=5)

        # Lines 62-29 put the buttons in the GUI
        self.btnLogin = ttk.Button(loginFrame, text='Login', command=self.login, width=20)
        self.btnLogin.grid(row=2, column=1, pady=5, padx=10)
        self.btnRegister = ttk.Button(loginFrame, text='Create an account', command=self.newWindow, width=20)
        self.btnRegister.grid(row=3, column=1, pady=5, padx=10)

        self.master.bind('<Return>', self.login)

    # this function opens the register window
    def newWindow(self):
        self.newWindow = Toplevel(self.master)
        self.app = registerWindow(self.newWindow)
        self.master.withdraw()

    def login(self, failures=[1]):
        global username
        maxAttempts = 4

        username = (self.usernameStr.get())
        password = (self.passwordStr.get())
        with sqlite3.connect("ManyMusicDB.db") as db:
            cursor = db.cursor()
        findUser = ("SELECT * FROM Users WHERE username = ? AND password = ? ")
        cursor.execute(findUser, [(username), (password)])
        results = cursor.fetchall()  # this function asks for the user's input and vcalidates to the database's version to grant the user acess to the program

        if results:
            self.newWindow = Toplevel(self.master)
            self.app = mainWindow(self.newWindow, username)
            self.master.withdraw()
        else:
            response = messagebox.askyesno("username and password not recognised", "Do you want to try again?")
            if response == 0:
                self.usernameStr.set("")
                self.passwordStr.set("")
                self.inpUsername.focus()

            else:
                failures.append(1)
            if sum(failures) >= maxAttempts:
                messagebox.showerror("Login Error", "Used up all attempts program will terminate")
                time.sleep(1)
                self.master.destroy()


class registerWindow:  # this class holds the GUI for the register window
    def __init__(self, master):
        self.master = master
        registerFrame = Frame(master)
        self.master.title("ManyMusic Register")
        self.master.geometry('350x300')
        self.master.configure(bg="#423f3e")
        registerFrame.pack(expand=True)
        registerFrame.configure(bg="#423f3e")

        self.usernameStr = StringVar()
        self.passwordStr = StringVar()
        self.passwordConfirmStr = StringVar()

        # lines 14-17 place the text for username and password in the GUI
        self.lblUsername = ttk.Label(registerFrame, text='Username', font=("Helvetica", 12))
        self.lblUsername.grid(row=1, column=0, ipady=5)
        self.lblpassword = ttk.Label(registerFrame, text='Password', font=("Helvetica", 12))
        self.lblpassword.grid(row=2, column=0, ipady=5)
        self.lblpasswordConfirm = ttk.Label(registerFrame, text='Confirm password', font=("Helvetica", 12))
        self.lblpasswordConfirm.grid(row=3, column=0, ipady=5)

        # Lines 20-24 put the entry box in the GUI
        self.inpUsername = ttk.Entry(registerFrame, textvariable=self.usernameStr, width=30)
        self.inpUsername.grid(row=1, column=1, ipady=3, padx=5)
        self.inpPassword = ttk.Entry(registerFrame, textvariable=self.passwordStr, width=30, show="*")
        self.inpPassword.grid(row=2, column=1, ipady=3, padx=5)
        self.inpPassword = ttk.Entry(registerFrame, textvariable=self.passwordConfirmStr, width=30, show="*")
        self.inpPassword.grid(row=3, column=1, ipady=3, padx=5)

        # Lines 62-29 put the buttons in the GUI
        self.btnRegisterr = ttk.Button(registerFrame, text='Sign-up', command=self.newUser, width=20)
        self.btnRegisterr.grid(row=4, column=0, columnspan=10, pady=5, padx=10)

        self.master.bind('<Return>', self.newUser)

    def newUser(self):
        global username
        username = (self.usernameStr.get())
        with sqlite3.connect("ManyMusicDB.db") as db:
            cursor = db.cursor()
        findUser = ("SELECT * FROM users WHERE username = ?")
        cursor.execute(findUser, [(username)])

        if cursor.fetchall():
            Rresponse2 = messagebox.showerror("Already exists", "Username taken, please try again")

        else:  # This function registers a new user, it asks for a username and checks if it alreday exists in the database then it asks for a password and confirms it
            username = (self.usernameStr.get())

        password = (self.passwordStr.get())
        password1 = (self.passwordConfirmStr.get())
        if password != password1:
            messagebox.showerror("Password Error", "your passwords did not match. please try again")
        else:
            password = (self.passwordStr.get())
            password1 = (self.passwordConfirmStr.get())
            insertData = '''INSERT INTO Users(username,password)
            VALUES(?,?)'''
            cursor.execute(insertData, [(username), (password)])
            db.commit()
            self.newWindow = Toplevel(self.master)
            self.app = mainWindow(self.newWindow, username)
            self.master.withdraw()


class mainWindow():  # this class holds the GUI for the main application
    def __init__(self, master, username):
        middleFrame = Frame(master)
        topFrame = Frame(master)
        bottomFrame = Frame(master)
        rboxFrame = Frame(middleFrame, relief=SUNKEN)
        self.username = username
        self.master = master
        self.master.title("ManyMusic")
        self.master.configure(bg="#423f3e")
        middleFrame.pack(fill=X)
        topFrame.pack()
        rboxFrame.pack(side=LEFT)
        bottomFrame.pack(side=BOTTOM, fill=X)

        middleFrame.configure(bg="#423f3e")
        topFrame.configure(bg="#423f3e")
        bottomFrame.configure(bg="#423f3e")
        rboxFrame.configure(bg="#423f3e")

        # menubar
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)

        # submenus
        self.subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.subMenu)
        self.subMenu.add_command(label="Open music", command=self.browse_file)
        self.subMenu.add_command(label="Open playlist", command=self.browse_playlist_file)
        self.subMenu.add_command(label="Exit", command=self.master.destroy)

        self.subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.subMenu)
        self.subMenu.add_command(label="About Us", command=self.about_us)

        # the audio control widgets of the mainwindow
        self.playPhoto = PhotoImage(file='play.png')
        self.playBtn = ttk.Button(bottomFrame, image=self.playPhoto, command=self.play_music)
        self.playBtn.grid(row=0, column=3, padx=10)
        self.stopPhoto = PhotoImage(file='stop.png')
        self.stopBtn = ttk.Button(bottomFrame, image=self.stopPhoto, command=self.stop_music)
        self.stopBtn.grid(row=0, column=4, padx=10)
        self.pausePhoto = PhotoImage(file='pause.png')
        self.pauseBtn = ttk.Button(bottomFrame, image=self.pausePhoto, command=self.pause_music)
        self.pauseBtn.grid(row=0, column=5, padx=10)
        self.forwardPhoto = PhotoImage(file='forward.png')
        self.forwardBtn = ttk.Button(bottomFrame, image=self.forwardPhoto, command=self.next_music)
        self.forwardBtn.grid(row=0, column=6, padx=10)
        self.previousPhoto = PhotoImage(file='previous.png')
        self.previousBtn = ttk.Button(bottomFrame, image=self.previousPhoto, command=self.prev_music)
        self.previousBtn.grid(row=0, column=7, padx=10)

        self.scale = ttk.Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol)
        self.scale.set(70)
        mixer.music.set_volume(0.7)
        self.scale.grid(row=0, column=9, pady=15, padx=20)
        self.rewindPhoto = PhotoImage(file='rewind.png')
        self.rewindBtn = ttk.Button(bottomFrame, image=self.rewindPhoto, command=self.rewind_music)
        self.rewindBtn.grid(row=0, column=8)
        self.mutePhoto = PhotoImage(file='mute.png')
        self.volumePhoto = PhotoImage(file='volume.png')
        self.volumeBtn = ttk.Button(bottomFrame, image=self.volumePhoto, command=self.mute_music)
        self.volumeBtn.grid(row=0, column=10)

        self.statusbar = ttk.Label(self.master, text="Welcome to ManyMusic", relief=SUNKEN)
        self.statusbar.pack(side=BOTTOM, fill=X)

        self.lengthLabel = ttk.Label(bottomFrame, text="Total Length : --:--")
        self.lengthLabel.grid(row=0, pady=5, column=1)
        self.currentTimeLabel = ttk.Label(bottomFrame, text="Current Time : --:--", relief=GROOVE)
        self.currentTimeLabel.grid(row=0)

        self.recommendBox = Listbox(rboxFrame, width=40, height=20, relief=SUNKEN)
        self.recommendBox.grid(row=1, column=0, padx=10)
        self.recommendBoxLabel = ttk.Label(rboxFrame, text="Recommended", font=("Helvetica", 9))
        self.recommendBoxLabel.grid(row=0)

        self.master.bind('<space>', self.pause_music)

        self.master.protocol("WM_DELETE_WINDOW", self.close_windwow)

        self.playlistBtn = ttk.Button(bottomFrame, text="Playlist", command=self.newWindow)
        self.playlistBtn.grid(sticky=E, column=11, row=0, padx=10)

        self.playlist = []
        self.filename = ""
        self.pauseFlag = False
        self.songAdded = False
        self.ip = 0
        self.sgid = int()
        self.usrid = int()
        self.trigger = 4

        self.load_to_recommendbox()

    # this function opens the playlist window
    def newWindow(self):
        self.newWindow = Toplevel(self.master)
        self.app = playlistWindow(self.newWindow, username)

    # play music function
    def play_music(self, recommendList=[1]):
        if self.songAdded == False:
            print("First add some Music")
        else:
            try:
                if self.pauseFlag:
                    mixer.music.unpause()
                    self.statusbar["text"] = "Music Resumed"
                    self.pauseFlag = False
                else:
                    self.stop_music()
                    print("Playing")
                    mixer.music.load(self.playingsong)
                    mixer.music.play()
                    self.guiSongName = os.path.basename(self.playingsong)
                    self.songname = self.guiSongName[:-4]
                    self.statusbar["text"] = "Playing " + self.songname
                    self.show_details(self.playingsong)
                    recommendList.append(1)
                if sum(recommendList) == self.trigger:
                    self.add_to_db()
                    recommendList.clear()
                    print("song added to favourites")
            except:
                print("Could not play the music")

    def play_music_playlist(self):
        if self.songAdded == False:
            print("First add some Music")
        else:
            try:
                if self.pauseFlag == True:
                    mixer.music.unpause()
                    self.statusbar["text"] = "Music Resumed"
                    self.pauseFlag = False
                else:
                    self.stop_music()
                    print("Playing")
                    mixer.music.load(self.playlist[self.ip])
                    mixer.music.play()
                    self.guisongname = os.path.basename(self.playlist[self.ip])
                    self.songname = self.guisongname[:-4]
                    self.statusbar["text"] = "Playing " + self.songname
                    self.show_details(self.playlist[self.ip])
            except:
                print("Could not play the music")

    # stop music function
    def stop_music(self):
        mixer.music.stop()
        self.statusbar["text"] = "Music Stopped"

    # pause function
    def pause_music(self):
        if self.songAdded == False:
            print("First add some Music")
        else:
            try:
                self.pauseFlag = True
                mixer.music.pause()
                self.statusbar["text"] = "Music Paused"
            except:
                print("could not pause music")

    # volume function
    def set_vol(self, val):
        volume = float(val) / 100
        mixer.music.set_volume(volume)

    # rewind function
    def rewind_music(self):
        self.play_music()
        self.statusbar['text'] = "Music Rewinded"

    # mute function
    muted = FALSE

    def mute_music(self):
        global muted
        if self.muted:
            mixer.music.set_volume(0.7)
            self.volumeBtn.configure(image=self.volumePhoto)
            self.scale.set(70)
            self.muted = FALSE
        else:
            mixer.music.set_volume(0)
            self.volumeBtn.configure(image=self.mutePhoto)
            self.scale.set(0)
            self.muted = TRUE

    def show_details(self, play_song):
        self.file_data = os.path.splitext(play_song)

        if self.file_data[1] == '.mp3':
            self.audio = MP3(play_song)
            self.total_length = self.audio.info.length
        else:
            self.a = mixer.Sound(play_song)
            self.total_length = self.a.get_length()

        self.mins, self.secs = divmod(self.total_length, 60)
        self.mins = round(self.mins)
        self.secs = round(self.secs)
        self.timeformat = '{:02d}:{:02d}'.format(self.mins, self.secs)
        self.lengthLabel["text"] = "Total Length" + " - " + self.timeformat

        self.t1 = threading.Thread(target=self.start_count, args=(self.total_length,))
        self.t1.start()

    def start_count(self, t):
        self.current_time = 0
        while self.current_time <= t and mixer.music.get_busy():
            if self.pauseFlag:
                continue
            else:
                self.mins, self.secs = divmod(self.current_time, 60)
                self.mins = round(self.mins)
                self.secs = round(self.secs)
                self.timeformat = '{:02d}:{:02d}'.format(self.mins, self.secs)
                self.currentTimeLabel["text"] = "Current Time" + " - " + self.timeformat
                time.sleep(1)
                self.current_time += 1

    # about us information
    def about_us(self):
        messagebox.showinfo("About MannyMusic",
                            "This is ManyMusic's music player. ManyMusic is record label that was founded in 1991 ")

    def browse_file(self):
        try:
            self.songAdded = True
            self.filename = filedialog.askopenfilename(initialdir="/", title="Select your music track", filetypes=(
                ("mp3 Music Files", "*.mp3"), ("m4a Music Files", "*.m4a")))
            self.playingsong = self.filename
            print(" Added " + self.filename)
        except:
            print("Cannot load the music")

    def browse_playlist_file(self):
        try:
            self.songAdded = True
            self.filename = filedialog.askopenfilename(
                initialdir="/C:/Users/andre/PycharmProjects/Python-Music-player-with-a-Databse/",
                title="Select your playlist", filetypes=(
                    ("Python File", ".py"), ("Text File", ".txt")))
            self.input = open(self.filename, 'rb')
            self.playlist = pickle.load(self.input)
            self.input.close()
            print(" Added " + self.filename)
            try:
                if self.pauseFlag:
                    mixer.unpause()
                else:
                    self.stop_music()
                    print("Playing")
                    mixer.music.load(self.playlist[self.ip])
                    mixer.music.play()
                    self.guisongname = os.path.basename(self.playlist[self.ip])
                    self.songname = self.guisongname[:-4]
                    self.statusbar["text"] = "Playing " + self.songname
                    self.show_details(self.playlist[self.ip])
                    mixer.music.queue(self.playlist[self.ip + 1])
            except:
                print("Could not play the music")
        except:
            print("Cannot load the music")

    def next_music(self):
        if self.songAdded == False:
            print("Add music first")
        else:
            try:
                if self.playlist[self.ip]:
                    self.ip += 1
                    self.play_music_playlist()
                else:
                    self.ip -= 1
            except:
                print("End of playlist, add more songs")

    def prev_music(self):
        if self.songAdded == False:
            print("Add music first")
        else:
            try:
                if self.playlist[self.ip - 1]:
                    self.ip -= 1
                    self.play_music_playlist()
                else:
                    print("No previous songs")
            except:
                self.stop_music()
                print("No previous song")

    def search_songid_sql(self):
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        self.song_titleRaw = os.path.basename(self.filename)
        self.song_title = self.song_titleRaw[:-4]
        self.findSong_id = ("SELECT song_id FROM songs WHERE song_title == ?")
        c.execute(self.findSong_id, [(self.song_title)])
        rows2 = c.fetchall()
        for p in rows2:
            self.sgid = int(''.join(map(str, p)))
        conn.commit()
        conn.close()

    def search_userid_sql(self):
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        self.usernamecopy = self.username
        self.findUser_id = ("SELECT user_id FROM users WHERE username == ?")
        c.execute(self.findUser_id, [(self.usernamecopy)])
        rows = c.fetchall()
        for h in rows:
            self.usrid = int(''.join(map(str, h)))
        conn.commit()
        conn.close()

    def add_to_db(self):
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        self.search_userid_sql()
        self.search_songid_sql()
        insertData = '''INSERT INTO favourites(user_id,song_id)
        VALUES(?,?)'''
        c.execute(insertData, [(self.usrid), (self.sgid)])
        conn.commit()
        conn.close()

    def load_to_recommendbox(self):
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        self.search_userid_sql()
        self.loadData = '''SELECT songs.song_title FROM songs INNER JOIN favourites ON songs.song_id = favourites.song_id AND favourites.user_id == ?'''
        c.execute(self.loadData, [(self.usrid)])
        rrows = c.fetchall()
        self.index = 0
        for z in rrows:
            self.recommendBox.insert(self.index, z)
            self.index += 1
        conn.commit()
        conn.close()

    def close_windwow(self):
        self.stop_music()
        self.master.destroy()


class playlistWindow:
    def __init__(self, master, username):
        self.master = master
        boxFrame = Frame(master)
        rightFrame = Frame(master)
        buttonFrame = Frame(boxFrame)
        self.master.title("ManyMusic Playlist")
        self.master.configure(bg="#423f3e")
        boxFrame.pack(side=LEFT)
        buttonFrame.pack(side=BOTTOM, fill=X)
        rightFrame.pack(side=RIGHT)

        boxFrame.configure(bg="#423f3e")
        rightFrame.configure(bg="#423f3e")
        buttonFrame.configure(bg="#423f3e")

        self.master.bind('<Return>', self.submit_playlist_changes)

        self.username = username
        self.playlist_nameStr = StringVar()

        self.playlist_name = ttk.Entry(rightFrame, textvariable=self.playlist_nameStr)
        self.playlist_name.grid(row=1, column=1, ipady=5, padx=5)

        self.playlist_nameLbl = ttk.Label(rightFrame, text="Enter the name of your playlist: ", width=28)
        self.playlist_nameLbl.grid(row=1, column=0, ipady=5)

        self.submitBtn = ttk.Button(rightFrame, text="Submit", command=self.submit_playlist_changes)
        self.submitBtn.grid(row=2, column=1, ipady=5, padx=5)

        self.playlistBox = Listbox(boxFrame, width=40, height=20, relief=SUNKEN)
        self.playlistBox.pack()

        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.subMenu)
        self.subMenu.add_command(label="Open playlist", command=self.delSong_file_open)
        self.subMenu.add_command(label="New playlist", command=self.new_playlist)
        self.subMenu.add_command(label="Delete playlist", command=self.delete_playlist)

        self.addBtn = ttk.Button(buttonFrame, text="+ Add", command=self.browse_song_for_playlist, width=20)
        self.addBtn.grid(column=0, row=1)
        self.delBtn = ttk.Button(buttonFrame, text="- Del", command=self.del_song, width=20)
        self.delBtn.grid(column=1, row=1)

        self.res1 = int()
        self.res2 = int()

        self.playlist = []

    def new_playlist2(self):
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        playlist_name = (self.playlist_nameStr.get())
        findUser_id = ("SELECT user_id FROM users WHERE username == ?")
        c.execute(findUser_id, [(self.username)])
        rows = c.fetchall()
        for row in rows:
            res = int(''.join(map(str, row)))
        insertData = '''INSERT INTO playlist(playlist_name,user_id)
        VALUES(?,?)'''
        c.execute(insertData, [(playlist_name), (res)])
        conn.commit()
        conn.close()

    def new_playlist(self):
        self.playListFileO = filedialog.asksaveasfilename(title="Re-enter the name for your new playlist",
                                                          filetypes=(("Python File", ".py"), ("Text File", ".txt")),
                                                          initialdir="C:/Users/andre/PycharmProjects/Python-Music-player-with-a-Databse/")
        output = open(self.playListFileO, 'wb')
        pickle.dump(self.playlist, output, -1)
        self.new_playlist2()
        messagebox.showinfo("Playlist created", "You have successfully created a playlist")

    def submit_playlist_changes(self):
        self.playListFileO = filedialog.asksaveasfilename(title="Enter the name of your playlist",
                                                          filetypes=(("Python File", ".py"), ("Text File", ".txt")),
                                                          initialdir="/")
        output = open(self.playListFileO, 'wb')
        pickle.dump(self.playlist, output, -1)

    def browse_song_for_playlist(self, ):
        global filename
        filename = filedialog.askopenfilename(initialdir="/", title="Select your song",
                                              filetypes=(("mp3 Music Files", "*.mp3"), ("m4a Music Files", "*.m4a")))
        self.add_to_playlist_box(filename)
        messagebox.showinfo("Song added", "The song has been successfully added to your playlist")

    def add_to_playlist_sql2(self, filename):
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        self.song_title = os.path.splitext(filename)[0]
        self.findSong_id = ("SELECT song_id FROM songs WHERE song_title == ?")
        c.execute(self.findSong_id, [(self.song_title)])
        rows2 = c.fetchall()
        for row in rows2:
            self.res2 = int(''.join(map(str, row)))

    def add_to_playlist_sql1(self):
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        self.playlist_name = (self.playlist_nameStr.get())
        self.findPlaylsit_id = ("SELECT playlist_id FROM playlist WHERE playlist_name == ?")
        c.execute(self.findPlaylsit_id, [(self.playlist_name)])
        rows1 = c.fetchall()
        for i in rows1:
            self.res1 = int(''.join(map(str, i)))

    # add song to playlist
    def add_to_playlist_box(self, filename):

        filename = os.path.basename(filename)
        self.index = 0
        self.playlistBox.insert(self.index, filename)
        self.playlist.insert(self.index, filename)
        self.index += 1
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        self.add_to_playlist_sql1()
        self.add_to_playlist_sql2(filename)
        insertData = '''INSERT INTO compound(playlist_id,song_id)
        VALUES(?,?)'''
        c.execute(insertData, [(self.res1), (self.res2)])
        conn.commit()

        conn.close()

    def delSong_file_open(self):
        global filename
        filename = filedialog.askopenfilename(initialdir="/", title="Select your playlist",
                                              filetypes=(("mp3 Music Files", "*.mp3"), ("m4a Music Files", "*.m4a")))
        self.input = open(filename, 'rb')
        self.playlist = pickle.load(self.input)
        self.input.close()
        self.index = 0
        for item in self.playlist:
            self.playlistBox.insert(self.index, item)
            self.index += 1

    def sql_del_song(self):
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        self.value = self.playlistBox.get(self.playlistBox.curselection())
        self.song_title = self.value[:-4]
        self.findSong_id = ("SELECT song_id FROM songs WHERE song_title == ?")
        c.execute(self.findSong_id, [(self.song_title)])
        rowsx = c.fetchall()
        for j in rowsx:
            self.idOfSong = int(''.join(map(str, j)))

    def del_song(self):
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        self.add_to_playlist_sql1()
        self.sql_del_song()
        deleteData = '''DELETE FROM compound WHERE playlist_id == ? AND song_id == ?'''
        c.execute(deleteData, [(self.res1), (self.idOfSong)])
        conn.commit()
        conn.close()
        self.selected_song = self.playlistBox.curselection()
        self.selected_song = int(self.selected_song[0])
        self.playlistBox.delete(self.selected_song)
        self.playlist.pop(self.selected_song)
        messagebox.showinfo("Song deleted", "The song you selected haas been successfully deleted from your playlist")

    def delete_playlist(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select the playlist you want to delete",
                                              filetypes=(("Python File", ".py"), ("Text File", ".txt")))
        os.remove(filename)
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        self.add_to_playlist_sql1()
        self.playlist_name_delete = (self.playlist_nameStr.get())
        deleteData2 = '''DELETE FROM compound WHERE playlist_id == ?'''
        c.execute(deleteData2, [(self.res1)])
        deleteplaylistData = '''DELETE FROM playlist WHERE playlist_name == ?'''
        c.execute(deleteplaylistData, [(self.playlist_name_delete)])
        conn.commit()
        conn.close()


if __name__ == '__main__':  # this statement keeps the GUI constantly displaying on the users screen
    main()
