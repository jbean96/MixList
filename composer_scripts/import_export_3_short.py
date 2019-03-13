import sys
import os

sys.path.append("..")
from analyzer import usersong, analysis
from composer import composer
from composer.audio_effect_types import Transition_Types, Effect_Types


"""
110 bpm -> 140 bpm -> 120 bpm
"""
songs_path = os.path.join(os.path.abspath(".."), "testmp3s")
filepaths = [os.path.join(songs_path, '110bpm_8bars.mp3'),
             os.path.join(songs_path, '140bpm_8bars.mp3'),
             os.path.join(songs_path, '120bpm_8bars.mp3')]

song_a = usersong.UserSong(filepaths[0])
song_b = usersong.UserSong(filepaths[1])
song_c = usersong.UserSong(filepaths[2])

usersong.batch_analyze_user_songs([song_a, song_b, song_c])

# get beat 16 beats from the end of Song a for transition 2
beat_a_0 = len(song_a.get_analysis_feature(analysis.Feature.BEATS)) - 9
# start beat 0 for Song b on transition 0
beat_b_0 = 0
# start beat 16 beats from end of Song b for transition 1
beat_b_1 = len(song_b.get_analysis_feature(analysis.Feature.BEATS)) - 9
# start beat 0 for Song c on transition 1
beat_c_1 = 0
# length in beats
length = 8
# pass transition type
t_1 = Transition_Types.CROSSFADE
t_2 = Transition_Types.TEMPO_MATCH
mix = [
        {"song_a": song_a, "song_b": song_b, "start_a": beat_a_0,"start_b": beat_b_0, "sections":
            [{"offset": 0, "length": length, "type": [t_1, t_2]}]
        },
        {"song_a": song_b, "song_b": song_c, "start_a": beat_b_1, "start_b": beat_c_1, "sections":
            [{"offset": 0, "length": length, "type": [t_1, t_2]}]
        }
    ]


"""
effects_list = [[effect_1, effect_2, ...]
    effect: {start_offset: integer, length: integer, type: effect_type}
"""

effect_list = [[{'start_offset': 0, 'length': 4, 'type': Effect_Types.FADEOUT}],
               [{'start_offset': 0, 'length': 4, 'type': Effect_Types.FADEOUT}],
               [{'start_offset': 0, 'length': 4, 'type': Effect_Types.FADEOUT}]]

c = composer.composer_parser(mix, effect_list)
c.compose()