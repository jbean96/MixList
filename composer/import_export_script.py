import sys
sys.path.append("..")
sys.path.append("../..")
import os
import composer
from optimizer import optimizer
from analyzer.analyzer import usersong

songs_path = os.path.join("..", "testmp3s", "songs", "edm")
filepaths = [os.path.join(songs_path, 'Feel_The_Love(Mike_Williams_Remix).mp3'),
             os.path.join(songs_path, 'Dusk_Till_Dawn(Brooks_Extended_Mix).mp3'),
             os.path.join(songs_path, 'Show&Tell.mp3')]

song_a = usersong.UserSong(filepaths[0], True)
song_b = usersong.UserSong(filepaths[1], True)
song_c = usersong.UserSong(filepaths[2], True)

mix = optimizer.Optimizer.generate_3_track(song_a, song_b, song_c)

c = composer.composer_parser(mix, filepaths)
c.compose()
