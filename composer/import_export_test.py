import sys
sys.path.append("..")
sys.path.append("../..")
import os
import composer
from optimizer import optimizer
from analyzer.analyzer import usersong

songs_path = os.path.join("..", "testmp3s")

song_a = usersong.UserSong(os.path.join(songs_path, "110bpm_8bars.mp3"), True)
song_b = usersong.UserSong(os.path.join(songs_path, "120bpm_8bars.mp3"), True)
song_c = usersong.UserSong(os.path.join(songs_path, "125bpm_8bars.mp3"), True)

mix = optimizer.Optimizer.generate_3_track(song_a, song_b, song_c)

c = composer.composer_parser(mix)
c.compose()

