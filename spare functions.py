# file function
def browse_file(self):
    global filename_path
    filename_path = filedialog.askopenfilename()
    self.add_to_playlist(filename_path)


# add song to playlist
def add_to_playlist(self, filename):
    filename = os.path.basename(filename)
    self.index = 0
    self.playlistBox.insert(self.index, filename)
    self.playlist.insert(self.index, filename_path)
    self.index += 1

    root = Tk()
    mixer.init()
    application = loginWindow(root)
    root.mainloop()