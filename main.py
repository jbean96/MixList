import os
import subprocess
from enum import auto, Enum
from tkinter import filedialog
from tkinter import *

DEBUG = True

class Action(Enum):
    TEST_AUDACITY = auto()
    LOAD_SONGS = auto()
    MIX = auto()
    DELETE_SONGS = auto()

class MixListGui:
    MIN_SONGS = 5
    COLUMNS = ["Song Name"]

    WIDTH = 400
    HEIGHT = 500
    BORDER_WIDTH = 3
    NUM_SECTIONS = 3

    def __init__(self, master : Tk):
        self.master = master
        self.master.title("MixList")

        self.COMMAND_MAP = {
            Action.TEST_AUDACITY : self.test_audacity,
            Action.LOAD_SONGS : self.load_songs,
            Action.MIX : self.mix,
            Action.DELETE_SONGS : self.delete_songs
        }

        ### VARIABLES ###

        self.message = StringVar()
        self.message.set("Let's make a mix!")
        
        self.loaded_songs = []

        ### FRAMES ###

        self.main_frame = Frame(self.master, width=MixListGui.WIDTH + MixListGui.BORDER_WIDTH * 2, \
             height=MixListGui.HEIGHT + MixListGui.BORDER_WIDTH * MixListGui.NUM_SECTIONS * 2, borderwidth=0)
        self.nav_frame = Frame(self.main_frame, width=MixListGui.WIDTH, \
            height=MixListGui.HEIGHT / 4, borderwidth=MixListGui.BORDER_WIDTH)
        self.song_frame = Frame(self.main_frame, width=MixListGui.WIDTH, \
            height=MixListGui.HEIGHT * 3.0 / 4, borderwidth=MixListGui.BORDER_WIDTH, relief="sunken")

        self.master.bind("<Delete>", lambda _: self.delete_songs())

        for frame in [self.main_frame, self.nav_frame, self.song_frame]:
            frame.pack(expand=True, fill=BOTH)
            frame.pack_propagate(0)

        self.song_listbox = Listbox(self.song_frame, selectmode=EXTENDED)
        self.song_listbox.pack(expand=True, fill=BOTH)

        self.draw_nav_frame(self.nav_frame, self.song_listbox)

        ### WIDGETS ###

        self.message_label = Label(self.nav_frame,  textvariable=self.message)
        self.message_label.pack(expand=True, fill=BOTH)

    def draw_nav_frame(self, parent : Frame, song_list_box : Listbox):
        self.buttons = {
            Action.TEST_AUDACITY : Button(parent, text="Test Audacity", command=self.COMMAND_MAP[Action.TEST_AUDACITY]),
            Action.LOAD_SONGS : Button(parent, text="Load songs", command=self.COMMAND_MAP[Action.LOAD_SONGS]),
            Action.MIX : Button(parent, text="MIX!", command = self.COMMAND_MAP[Action.MIX]),
            Action.DELETE_SONGS : Button(parent, text="Remove selected songs", command=self.COMMAND_MAP[Action.DELETE_SONGS])
        }
        for button in self.buttons.values():
            button.pack(expand=True, fill='x')

    def test_audacity(self):
        result = subprocess.run(["python", "pipe_test.py"])
        if result.returncode == 1:
            self.message.set("Audacity test didn't work, make sure mod-script-pipe is enabled.")
        else:
            self.message.set("Audacity is good to go!")

    def delete_songs(self):
        indices = list(map(int, self.song_listbox.curselection()))
        indices.sort(reverse=True)
        for index in indices:
            self.song_listbox.delete(index)
            del self.loaded_songs[index]
        self.message.set("Removed %d songs from list" % len(indices))

        self.log_songs()

    def load_songs(self):
        file_paths = filedialog.askopenfilenames(initialdir=os.path.curdir, title="Select song files", filetypes=(("mp3 files", "*.mp3"), ("wav files", "*.wav")))
        new_songs = list(file_paths)
        ### NEED TO TURN INTO SONG OBJECTS ###
        self.loaded_songs.extend(new_songs)
        for song in new_songs:
            self.song_listbox.insert(END, song)

        self.log_songs()

    def mix(self):
        ### TODO: Call methods to create mix here ###
        self.message.set("MIX")

    ### DEBUG METHODS ###

    def log_songs(self):
        if not DEBUG:
            return
        
        if len(self.loaded_songs) > 1:
            print("Currently loaded songs:")
            for song in self.loaded_songs:
                print(song)
        else:
            print("No songs currently loaded")

def _main():
    root = Tk()
    MixListGui(root)
    root.mainloop()

if __name__ == '__main__':
    _main()