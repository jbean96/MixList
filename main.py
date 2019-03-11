import argparse
import os
import subprocess
from enum import auto, Enum
from tkinter import filedialog
from tkinter import *

from analyzer.analyzer import usersong
from optimizer.optimizer import Optimizer
from optimizer.mix_goal import MixGoal
from composer import composer

class Action(Enum):
    TEST_AUDACITY = auto()
    LOAD_SONGS = auto()
    MIX = auto()
    DELETE_SONGS = auto()
    ANALYZE_SONGS = auto()

class MixListGui:
    WIDTH = 400
    HEIGHT = 500
    BORDER_WIDTH = 3
    NUM_SECTIONS = 2

    def __init__(self, master : Tk, cache_path : str, debug : bool):
        """
        Constructs the MixListGui object

        @param master: The Tk object that the gui will belong to
        @param cache_path: The path to the folder that we will look for/save static analyses
            for mixed songs
        @param debug: bool indicating whether or not we should log things to the command line
        
        """
        self.master = master
        self.master.title("MixList")

        self.debug = debug

        self.cache_path = cache_path

        self.COMMAND_MAP = {
            Action.TEST_AUDACITY : self.test_audacity,
            Action.LOAD_SONGS : self.load_songs,
            Action.MIX : self.mix,
            Action.DELETE_SONGS : self.delete_songs,
            Action.ANALYZE_SONGS : self.analyze_songs
        }

        ### VARIABLES ###

        self.message = StringVar()
        self.message.set("Let's make a mix!")
        
        self.loaded_songs = []

        ### FRAMES ###

        self.main_frame = Frame(self.master, width=MixListGui.WIDTH + MixListGui.BORDER_WIDTH * 2, \
             height=MixListGui.HEIGHT + MixListGui.BORDER_WIDTH * MixListGui.NUM_SECTIONS * 2, borderwidth=0)
        self.nav_frame = Frame(self.main_frame, width=MixListGui.WIDTH, \
            height=MixListGui.HEIGHT * 3.0 / 8, borderwidth=MixListGui.BORDER_WIDTH)
        self.song_frame = Frame(self.main_frame, width=MixListGui.WIDTH, \
            height=MixListGui.HEIGHT * 5.0 / 8, borderwidth=MixListGui.BORDER_WIDTH, relief="sunken")

        self.master.bind("<Delete>", lambda _: self.delete_songs())

        for frame in [self.main_frame, self.nav_frame, self.song_frame]:
            frame.pack(expand=True, fill=BOTH)
            frame.pack_propagate(0)

        self.song_listbox = Listbox(self.song_frame, selectmode=EXTENDED)
        self.song_listbox.pack(expand=True, fill=BOTH)

        self.draw_nav_frame(self.nav_frame)

        ### WIDGETS ###

        self.message_label = Label(self.nav_frame,  textvariable=self.message)
        self.message_label.pack(expand=True, fill=BOTH)

    def draw_nav_frame(self, parent : Frame):
        self.buttons = {
            Action.TEST_AUDACITY : Button(parent, text="Test Audacity", command=self.COMMAND_MAP[Action.TEST_AUDACITY]),
            Action.LOAD_SONGS : Button(parent, text="Load songs", command=self.COMMAND_MAP[Action.LOAD_SONGS]),
            Action.MIX : Button(parent, text="MIX!", command = self.COMMAND_MAP[Action.MIX]),
            Action.DELETE_SONGS : Button(parent, text="Remove selected songs", command=self.COMMAND_MAP[Action.DELETE_SONGS]),
            Action.ANALYZE_SONGS : Button(parent, text="Analyze songs", command=self.COMMAND_MAP[Action.ANALYZE_SONGS])
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
        new_songs = list(map(usersong.UserSong, list(file_paths)))
        ### NEED TO TURN INTO SONG OBJECTS ###
        self.loaded_songs.extend(new_songs)
        for song in new_songs:
            self.song_listbox.insert(END, song.get_name())

        self.log_songs()

    def analyze_songs(self):
        self.log_message("Analyzing songs")
        usersong.batch_analyze_user_songs(self.loaded_songs, cache_path=self.cache_path)
        self.log_message("Writing analysis files to: %s" % self.cache_path)
        for s in self.loaded_songs:
            s.write_analysis_to_folder(self.cache_path)
        self.message.set("Songs analyzed!")

    def mix(self):
        if len(self.loaded_songs) == 0:
            self.message.set("No loaded songs...")
            return
        first_goal = MixGoal(self.loaded_songs[0], 0.0)
        goals = [first_goal]
        self.analyze_songs()
        dj = Optimizer(self.loaded_songs, goals)
        mix = dj.generate_mixtape()
        self.log_message(mix)
        comp = composer.composer_parser(mix)
        comp.compose()

    def log_songs(self):
        if not self.debug:
            return
        
        if len(self.loaded_songs) > 1:
            print("Currently loaded songs:")
            for song in self.loaded_songs:
                print(song.get_name())
        else:
            print("No songs currently loaded")

    def log_message(self, message: str):
        if not self.debug:
            return

        print(message)

def _main(args: argparse.Namespace):
    root = Tk()
    cache_path = os.path.abspath(args.cache_path)
    if not os.path.isdir(cache_path):
        os.mkdir(cache_path)
    MixListGui(root, cache_path, args.debug)
    root.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Main program for the MixList project.")
    parser.add_argument("--cache", "-c", type=str, dest="cache_path", default="mixlist_cache", help="The folder to store analyses in")
    parser.add_argument("--debug", "-d", dest="debug", action="store_true")
    parser.set_defaults(debug=False)

    args = parser.parse_args()
    _main(args)