import sys
sys.path.append("..")
sys.path.append("../..")
import os
import composer
from analyzer.analyzer import usersong, analysis

"""
Songs are in decreasing order of bpm
"""
songs_path = os.path.join(os.path.abspath(".."), "testmp3s")
filepaths = [os.path.join(songs_path, '140bpm_8bars.mp3'),
             os.path.join(songs_path, '130bpm_8bars.mp3'),
             os.path.join(songs_path, '125bpm_8bars.mp3'),
             os.path.join(songs_path, '120bpm_8bars.mp3'),
             os.path.join(songs_path, '110bpm_8bars.mp3')]

song_a = usersong.UserSong(filepaths[0], True)
song_b = usersong.UserSong(filepaths[1], True)
song_c = usersong.UserSong(filepaths[2], True)
song_d = usersong.UserSong(filepaths[3], True)
song_e = usersong.UserSong(filepaths[4], True)

# get beat 16 beats from the end of Song a for transition 2
beat_a_0 = len(song_a.get_analysis_feature(analysis.Feature.BEATS)) - 13
beat_b_1 = len(song_b.get_analysis_feature(analysis.Feature.BEATS)) - 13
beat_c_1 = len(song_c.get_analysis_feature(analysis.Feature.BEATS)) - 13
beat_d_1 = len(song_d.get_analysis_feature(analysis.Feature.BEATS)) - 13
beat_e_1 = len(song_e.get_analysis_feature(analysis.Feature.BEATS)) - 13

# length in beats
length = 12
# pass transition type
t_1 = "crossfade"
t_2 = "tempomatch"
mix = [
        {"song_a": song_a, "song_b": song_b, "start_a": 0, "start_b": 0, "sections":
            [{"offset": 0, "length": length, "type": [t_1, t_2]}]
        },
        {"song_a": song_b, "song_b": song_c, "start_a": beat_b_1, "start_b": 0, "sections":
            [{"offset": 0, "length": length, "type": [t_1, t_2]}]
        },
        {"song_a": song_c, "song_b": song_d, "start_a": beat_c_1, "start_b": 0, "sections":
            [{"offset": 0, "length": length, "type": [t_1, t_2]}]
        },
        {"song_a": song_d, "song_b": song_e, "start_a": beat_d_1, "start_b": 0, "sections":
            [{"offset": 0, "length": length, "type": [t_1, t_2]}]
        }
    ]

c = composer.composer_parser(mix, filepaths)
c.compose()