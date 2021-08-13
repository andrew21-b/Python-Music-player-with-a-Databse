from tkinter import *  # the modules needed to use the libaries
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import time
from pygame import mixer
import os
import threading
import pickle
from mutagen.mp3 import  MP3

def main():  # this defines the program to make the windows
    root = Tk()
    app = loginWindow(root)
    mixer.init()


class loginWindow:  # this class holds the GUI for the login window

    def __init__(self, master):
        self.master = master
        self.master.title("ManyMusic Login")
        self.master.geometry('300x300')

        # lines 17-18 convert the data to a string
        self.usernameStr = StringVar()
        self.passwordStr = StringVar()

        # lines 14-17 place the text for username and password in the GUI
        self.lblUsername = Label(self.master, text='username', )
        self.lblUsername.grid(row=1, column=0, padx=10)
        self.lblpassword = Label(self.master, text='password', )
        self.lblpassword.grid(row=2, column=0)

        # Lines 20-24 put the entry box in the GUI
        self.inpUsername = Entry(self.master, textvariable=self.usernameStr)
        self.inpUsername.grid(row=1, column=1)
        self.inpPassword = Entry(self.master, textvariable=self.passwordStr)
        self.inpPassword.grid(row=2, column=1)

        # Lines 62-29 put the buttons in the GUI
        self.btnLogin = Button(self.master, text='login', command=self.login)
        self.btnLogin.grid(row=3, column=0, columnspan=10, pady=5)
        self.btnRegister = Button(self.master, text='create an account', command=self.newWindow)
        self.btnRegister.grid(column=0, columnspan=10)

    # this function opens the register window
    def newWindow(self):
        self.newWindow = Toplevel(self.master)
        self.app = registerWindow(self.newWindow)
        root.withdraw()

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
                root.destroy()


class registerWindow:  # this class holds the GUI for the register window
    def __init__(self, master):
        self.master = master
        self.master.title("ManyMusic Register")
        self.master.geometry('300x300')

        self.usernameStr = StringVar()
        self.passwordStr = StringVar()
        self.passwordConfirmStr = StringVar()

        # lines 14-17 place the text for username and password in the GUI
        self.lblUsername = Label(self.master, text='username', )
        self.lblUsername.grid(row=1, column=0, padx=10)
        self.lblpassword = Label(self.master, text='password', )
        self.lblpassword.grid(row=2, column=0)
        self.lblpasswordConfirm = Label(self.master, text='confirm password', )
        self.lblpasswordConfirm.grid(row=3, column=0)

        # Lines 20-24 put the entry box in the GUI
        self.inpUsername = Entry(self.master, textvariable=self.usernameStr)
        self.inpUsername.grid(row=1, column=1)
        self.inpPassword = Entry(self.master, textvariable=self.passwordStr)
        self.inpPassword.grid(row=2, column=1)
        self.inpPassword = Entry(self.master, textvariable=self.passwordConfirmStr)
        self.inpPassword.grid(row=3, column=1)

        # Lines 62-29 put the buttons in the GUI
        self.btnRegisterr = Button(self.master, text='sign-up', command=self.newUser)
        self.btnRegisterr.grid(row=4, column=0, columnspan=10, pady=5)

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
        self.username = username
        self.master = master

        self.master.title("ManyMusic")
        self.master.geometry('300x300')

        # menubar
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)

        # submenus
        self.subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.subMenu)
        self.subMenu.add_command(label="Open music", command=self.browse_file)
        self.subMenu.add_command(label="Open playlist", command=self.browse_playlist_file)
        self.subMenu.add_command(label="Exit", command=root.destroy)

        self.subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.subMenu)
        self.subMenu.add_command(label="About Us", command=self.about_us)

        # the audio control widgets of the mainwindow
        self.playPhoto = PhotoImage(file='play.png')
        self.playBtn = Button(self.master, image=self.playPhoto, command=self.play_music)
        self.playBtn.grid()
        self.stopPhoto = PhotoImage(file='stop.png')
        self.stopBtn = Button(self.master, image=self.stopPhoto, command=self.stop_music)
        self.stopBtn.grid()
        self.pausePhoto = PhotoImage(file='pause.png')
        self.pauseBtn = Button(self.master, image=self.pausePhoto, command=self.pause_music)
        self.pauseBtn.grid()
        self.forwardBtn = Button(self.master, text="Forward", command=self.next_music)
        self.forwardBtn.grid()
        self.previousBtn = Button(self.master, text="Previous", command=self.prev_music)
        self.previousBtn.grid()

        self.scale = Scale(self.master, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol)
        self.scale.set(70)
        mixer.music.set_volume(0.7)
        self.scale.grid()
        self.rewindPhoto = PhotoImage(file='rewind.png')
        self.rewindBtn = Button(self.master, image=self.rewindPhoto, command=self.rewind_music)
        self.rewindBtn.grid()
        self.mutePhoto = PhotoImage(file='mute.png')
        self.volumePhoto = PhotoImage(file='volume.png')
        self.volumeBtn = Button(self.master, image=self.volumePhoto, command=self.mute_music)
        self.volumeBtn.grid()

        self.statusbar = Label(self.master, text="Welcome to ManyMusic", relief=SUNKEN)
        self.statusbar.grid(sticky=S, columnspan=1)

        self.lengthLabel = Label(self.master, text="Total Length : --:--")
        self.lengthLabel.grid()
        self.currentTimeLabel = Label(self.master, text="Current Time : --:--", relief=GROOVE)
        self.currentTimeLabel.grid()

        self.recommendBox = Listbox(self.master)
        self.recommendBox.grid()

        self.addBtn = Button(self.master, text="+ Add", command=self.browse_file)
        self.addBtn.grid()
        self.delBtn = Button(self.master, text="- Del")
        self.delBtn.grid()

        self.master.protocol("WM_DELETE_WINDOW", self.close_windwow)

        self.testBtn = Button(self.master, text="new", command=self.newWindow)
        self.testBtn.grid()

        self.playlist = []
        self.filename = ""
        self.pauseFlag = False
        self.songAdded = False
        self.ip = 0
        self.sgid = int()
        self.usrid = int()
        self.trigger = 3

        self.load_to_recommendbox()

    # this function opens the register window
    def newWindow(self):
        self.newWindow = Toplevel(self.master)
        self.app = playlistWindow(self.newWindow)
        self.master.withdraw()

    # play music function
    def play_music(self, recommendList=[1]):
        if self.songAdded == False:
            print("First add some Music")
        else:
            try:
                if self.pauseFlag:
                    self.statusbar["text"] = "Music Resumed"
                    self.pauseFlag = False
                else:
                    self.stop_music()
                    print("Playing")
                    mixer.music.load(self.playingsong)
                    mixer.music.play()
                    self.guisongname = os.path.basename(self.playingsong)
                    self.songname = self.guisongname[:-4]
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
        volume = int(val) / 100
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
            self.filename = filedialog.askopenfilename(initialdir="/", title="Select your cool music track", filetypes=(
            ("mp3 Music Files", "*.mp3"), ("m4a Music Files", "*.m4a")))
            self.playingsong = self.filename
            print(" Added " + self.filename)
        except:
            print("Cannot load the music")

    def browse_playlist_file(self):
        try:
            self.songAdded = True
            self.filename = filedialog.askopenfilename(initialdir="/", title="Select your cool music track", filetypes=(
            ("mp3 Music Files", "*.mp3"), ("m4a Music Files", "*.m4a")))
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
    def __init__(self, master):
        self.master = master
        self.master.title("ManyMusic Playlist")
        self.master.geometry('300x300')

        self.playlist_nameStr = StringVar()
        self.usernameStr = StringVar()

        self.playlist_name = Entry(self.master, textvariable=self.playlist_nameStr)
        self.playlist_name.grid()
        self.username = Entry(self.master, textvariable=self.usernameStr)
        self.username.grid()

        self.playlist_nameLbl = Label(self.master, text="Enter the name of your playlist: ")
        self.playlist_nameLbl.grid()
        self.usernameLbl = Label(self.master, text="Enter your username: ")
        self.usernameLbl.grid()
        self.submitBtn = Button(self.master, text="Submit", command=self.new_playlist)
        self.submitBtn.grid()

        self.playlistBox = Listbox(self.master)
        self.playlistBox.grid()

        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.subMenu)
        self.subMenu.add_command(label="Open playlist", command=self.delSong_file_open)

        self.addBtn = Button(self.master, text="+ Add", command=self.browse_song_for_playlist)
        self.addBtn.grid()
        self.delBtn = Button(self.master, text="- Del", command=self.del_song)
        self.delBtn.grid()

        self.res1 = int()
        self.res2 = int()

        self.playlist = []

    def new_playlist2(self):
        conn = sqlite3.connect("ManyMusicDB.db")
        c = conn.cursor()
        playlist_name = (self.playlist_nameStr.get())
        username = (self.usernameStr.get())
        findUser_id = ("SELECT user_id FROM users WHERE username == ?")
        c.execute(findUser_id, [(username)])
        rows = c.fetchall()
        for row in rows:
            res = int(''.join(map(str, row)))
        insertData = '''INSERT INTO playlist(playlist_name,user_id)
        VALUES(?,?)'''
        c.execute(insertData, [(playlist_name), (res)])
        conn.commit()
        conn.close()

    def new_playlist(self):
        self.playListFileO = filedialog.asksaveasfilename(title="Give a name to your playlist",
                                                          filetypes=(("Python File", ".py"), ("Text File", ".txt")),
                                                          initialdir="/")
        output = open(self.playListFileO, 'wb')
        pickle.dump(self.playlist, output, -1)

    def browse_song_for_playlist(self, ):
        global filename
        filename = filedialog.askopenfilename(initialdir="/", title="Select your song",
                                              filetypes=(("mp3 Music Files", "*.mp3"), ("m4a Music Files", "*.m4a")))
        self.add_to_playlist_box(filename)
        print("done")

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
        filename = filedialog.askopenfilename(initialdir="/", title="Select your song",
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


if __name__ == '__main__':  # this statement keeps the GUI constantly displaying on the users screen
    root = Tk()
    mixer.init()
    application = loginWindow(root)
    root.mainloop()
