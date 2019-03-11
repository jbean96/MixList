import sys
import os

sys.path.append("..")
from composer import composer
from analyzer import usersong, analysis
from composer.audio_effect_types import Transition_Types

"""
BPM of songs mixed
110 -> 120 -> 125 -> 130 -> 140
"""
songs_path = os.path.join(os.path.abspath(".."), "testmp3s")
filepaths = [os.path.join(songs_path, '110bpm_8bars.mp3'),
             os.path.join(songs_path, '120bpm_8bars.mp3'),
             os.path.join(songs_path, '125bpm_8bars.mp3'),
             os.path.join(songs_path, '130bpm_8bars.mp3'),
             os.path.join(songs_path, '140bpm_8bars.mp3')]

song_a = usersong.UserSong(filepaths[0])
song_b = usersong.UserSong(filepaths[1])
song_c = usersong.UserSong(filepaths[2])
song_d = usersong.UserSong(filepaths[3])
song_e = usersong.UserSong(filepaths[4])

usersong.batch_analyze_user_songs([song_a, song_b, song_c, song_d, song_e])

# get beat 16 beats from the end of Song a for transition 2
beat_a_0 = len(song_a.get_analysis_feature(analysis.Feature.BEATS)) - 13
beat_b_1 = len(song_b.get_analysis_feature(analysis.Feature.BEATS)) - 13
beat_c_1 = len(song_c.get_analysis_feature(analysis.Feature.BEATS)) - 13
beat_d_1 = len(song_d.get_analysis_feature(analysis.Feature.BEATS)) - 13
beat_e_1 = len(song_e.get_analysis_feature(analysis.Feature.BEATS)) - 13

# length in beats
length = 12
# pass transition type
t_1 = Transition_Types.CROSSFADE
t_2 = Transition_Types.TEMPO_MATCH
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

c = composer.composer_parser(mix)
c.compose()