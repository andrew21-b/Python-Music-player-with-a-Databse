from tkinter import *#the modules needed to use the libaries
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import time
from pygame import mixer
import os
import threading




def main():#this defines the program to make the windows
    root = Tk()
    app = loginWindow(root)
    mixer.init()



class loginWindow:#this class holds the GUI for the login window
    def __init__(self, master):
        self.master = master
        self.master.title("ManyMusic Login")
        self.master.geometry('300x300')

        #lines 17-18 convert the data to a string
        self.usernameStr = StringVar()
        self.passwordStr = StringVar()

        #lines 14-17 place the text for username and password in the GUI
        self.lblUsername = Label(self.master, text = 'username' ,)
        self.lblUsername.grid(row=1,column=0, padx=10)
        self.lblpassword = Label(self.master, text='password', )
        self.lblpassword.grid(row=2, column=0)

        #Lines 20-24 put the entry box in the GUI
        self.inpUsername = Entry(self.master, textvariable=self.usernameStr)
        self.inpUsername.grid(row=1,column=1)
        self.inpPassword = Entry(self.master, textvariable=self.passwordStr)
        self.inpPassword.grid(row=2,column=1)

        #Lines 62-29 put the buttons in the GUI
        self.btnLogin = Button(self.master, text = 'login', command = self.login)
        self.btnLogin.grid(row=3,column = 0,columnspan=10, pady=5)
        self.btnRegister = Button(self.master, text= 'create an account',command=self.newWindow)
        self.btnRegister.grid(column=0,columnspan=10)



    # this function opens the register window
    def newWindow(self):
        self.newWindow = Toplevel(self.master)
        self.app = registerWindow(self.newWindow)
        root.withdraw()



    def login(self,failures=[1]):
        maxAttempts = 4
        sumo = sum(failures)

        username = (self.usernameStr.get())
        password = (self.passwordStr.get())
        with sqlite3.connect("ManyMusicDB.db") as db:
            cursor = db.cursor()
        findUser = ("SELECT * FROM Users WHERE username = ? AND password = ? ")
        cursor.execute(findUser, [(username), (password)])
        results = cursor.fetchall()  # this function asks for the user's input and vcalidates to the database's version to grant the user acess to the program

        if results:
            self.newWindow = Toplevel(self.master)
            self.app = mainWindow(self.newWindow)
            self.master.withdraw()
        else:
            response = messagebox.askyesno("username and password not recognised","Do you want to try again?")
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
        self.btnRegisterr = Button(self.master, text='sign-up',command=self.newUser)
        self.btnRegisterr.grid(row=4, column=0, columnspan=10, pady=5)



    def newUser(self):
        username = (self.usernameStr.get())
        with sqlite3.connect("ManyMusicDB.db") as db:
            cursor = db.cursor()
        findUser = ("SELECT * FROM users WHERE username = ?")
        cursor.execute(findUser, [(username)])

        if cursor.fetchall():
            Rresponse2=messagebox.showerror("Already exists","Username taken, please try again")

        else:               # This function registers a new user, it asks for a username and checks if it alreday exists in the database then it asks for a password and confirms it
            username = (self.usernameStr.get())


        password = (self.passwordStr.get())
        password1 = (self.passwordConfirmStr.get())
        if password != password1:
            messagebox.showerror("Password Error","your passwords did not match. please try again")
        else:
            password = (self.passwordStr.get())
            password1 = (self.passwordConfirmStr.get())
            insertData = '''INSERT INTO Users(username,password)
            VALUES(?,?)'''
            cursor.execute(insertData, [(username), (password)])
            db.commit()
            self.newWindow = Toplevel(self.master)
            self.app = mainWindow(self.newWindow)
            self.master.withdraw()



class mainWindow:#this class holds the GUI for the main application
    def __init__(self, master):
        self.master = master

        self.master.title("ManyMusic")
        self.master.geometry('300x300')

        #menubar
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)

        #submenus
        self.subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.subMenu)
        self.subMenu.add_command(label="Open", command=self.browse_file)
        self.subMenu.add_command(label="Exit", command=root.destroy)

        self.subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.subMenu)
        self.subMenu.add_command(label="About Us",command=self.about_us)


        #the audio control widgets of the mainwindow
        self.playPhoto = PhotoImage(file='play.png')
        self.playBtn = Button(self.master,image=self.playPhoto ,command=self.play_music)
        self.playBtn.grid()
        self.stopPhoto = PhotoImage(file='stop.png')
        self.stopBtn = Button(self.master, image=self.stopPhoto, command=self.stop_music)
        self.stopBtn.grid()
        self.pausePhoto = PhotoImage(file='pause.png')
        self.pauseBtn = Button(self.master, image=self.pausePhoto, command=self.pause_music)
        self.pauseBtn.grid()

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
        self.statusbar.grid(sticky=S,columnspan=1)

        self.lengthLabel = Label(self.master, text="Total Length : --:--")
        self.lengthLabel.grid()
        self.currentTimeLabel = Label(self.master, text="Current Time : --:--", relief=GROOVE)
        self.currentTimeLabel.grid()

        self.playlistBox = Listbox(self.master)
        self.playlistBox.grid()

        self.addBtn = Button(self.master, text="+ Add", command=self.browse_file)
        self.addBtn.grid()
        self.delBtn = Button(self.master, text="- Del", command=self.del_song)
        self.delBtn.grid()

        self.master.protocol("WM_DELETE_WINDOW", self.close_windwow)

        self.playlist = []



    #play music function
    def play_music(self):
        global paused

        if self.paused:
            mixer.music.unpause()
            self.statusbar["text"] = "Music Resumed"
            paused = FALSE
        else:
            try:
                self.stop_music()
                time.sleep(1)
                self.selected_song = self.playlistBox.curselection()
                self.selected_song = int(self.selected_song[0])
                self.play_it = self.playlist[self.selected_song]
                mixer.music.load(self.play_it)
                mixer.music.play()
                self.statusbar["text"] = "Playing music"+"-"+os.path.basename(self.play_it)
                self.show_details(self.play_it)
            except:
                messagebox.showerror("File not found", "ManyMusIc could not find the file name. Please try again")

    #stop music function
    def stop_music(self):
        mixer.music.stop()
        self.statusbar["text"] = "Music Stopped"
    #pause function
    paused = FALSE
    def pause_music(self):
        global paused
        paused = TRUE
        mixer.music.pause()
        self.statusbar["text"] = "Music Paused"
    #volume function
    def set_vol(self,val):
        volume = int(val)/100
        mixer.music.set_volume(volume)
    #rewind function
    def rewind_music(self):
        self.play_music()
        self.statusbar['text'] = "Music Rewinded"
    #mute function
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
        self.a = mixer.Sound(play_song)
        self.total_length = self.a.get_length()
        self.mins, self.secs = divmod(self.total_length, 60)
        self.mins = round(self.mins)
        self.secs = round(self.secs)
        self.timeformat = '{:02d}:{:02d}'.format(self.mins, self.secs)
        self.lengthLabel["text"] = "Total Length" + " - " + self.timeformat

        self.t1 = threading.Thread(target=self.start_count, args=(self.total_length,))
        self.t1.start()

    def start_count(self,t):
        global paused
        self.current_time = 0
        while self.current_time <= t and mixer.music.get_busy():
            if self.paused:
                continue
            else:
                self.mins, self.secs = divmod(self.current_time, 60)
                self.mins = round(self.mins)
                self.secs = round(self.secs)
                self.timeformat = '{:02d}:{:02d}'.format(self.mins, self.secs)
                self.currentTimeLabel["text"] = "Current Time" + " - " + self.timeformat
                time.sleep(1)
                self.current_time += 1

    #about us information
    def about_us(self):
        messagebox.showinfo("About MannyMusic", "This is ManyMusic's music player. ManyMusic is record label that was founded in 1991 ")

    #file function
    def browse_file(self):
        global filename_path
        filename_path = filedialog.askopenfilename()
        self.add_to_playlist(filename_path)
    #add song to playlist
    def add_to_playlist(self,filename):
        filename = os.path.basename(filename)
        self.index = 0
        self.playlistBox.insert(self.index, filename)
        self.playlist.insert(self.index, filename_path)
        self.index += 1
    #delte a song from the playlist
    def del_song(self):
        self.selected_song = self.playlistBox.curselection()
        self.selected_song = int(self.selected_song[0])
        self.playlistBox.delete(self.selected_song)
        self.playlist.pop(self.selected_song)

    def close_windwow(self):
        self.stop_music()
        self.master.destroy()






if __name__=='__main__':#this statement keeps the GUI constantly displaying on the users screen
    root = Tk()
    mixer.init()
    application =loginWindow(root)
    root.mainloop()