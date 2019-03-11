import sys
import os

sys.path.append("..")
from composer import composer
from analyzer import analysis, usersong
from composer.audio_effect_types import Transition_Types


songs_path = os.path.join("..", "testmp3s", "songs", "edm")
filepaths = [os.path.join(songs_path, 'Feel_The_Love(Mike_Williams_Remix).mp3'),
             os.path.join(songs_path, 'Dusk_Till_Dawn(Brooks_Extended_Mix).mp3'),
             os.path.join(songs_path, 'Show&Tell.mp3')]

song_a = usersong.UserSong(filepaths[0])
song_b = usersong.UserSong(filepaths[1])
song_c = usersong.UserSong(filepaths[2])

usersong.batch_analyze_user_songs([song_a, song_b, song_c])

# get beat 16 beats from the end of Song a for transition 2
beat_a_0 = len(song_a.get_analysis_feature(analysis.Feature.BEATS)) - 33
# start beat 0 for Song b on transition 0
beat_b_0 = 0
# start beat 16 beats from end of Song b for transition 1
beat_b_1 = len(song_b.get_analysis_feature(analysis.Feature.BEATS)) - 34
# start beat 0 for Song c on transition 1
beat_c_1 = 32
# transition is length is always 16
length = 32
# pass transition type
t_1 = Transition_Types.CROSSFADE
t_2 = Transition_Types.TEMPO_MATCH
mix = [
    {"song_a": song_a, "song_b": song_b, "start_a": beat_a_0,"start_b": beat_b_0, "sections":
        [{"offset": 0, "length": 32, "type": [t_1, t_2]}]
    },
    {"song_a": song_b, "song_b": song_c, "start_a": beat_b_1, "start_b": beat_c_1, "sections":
        [{"offset": 0, "length": 32, "type": [t_1, t_2]}]
    }
]

c = composer.composer_parser(mix)
c.compose()