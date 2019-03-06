import sys
import os
sys.path.append("..")
sys.path.append("../..")
import composer
from audio_effect_types import Transition_Types

songs_path = os.path.join("..", "testmp3s")

song0 = {
    'start_intro': 0.031,
    'end_intro': 0.031,
    'start_outro': 4.3965,
    'end_outro' : 8.7605,
    'tempo' : 110
    }
song1 = {
    'start_intro': 0.031,
    'end_intro': 4.031,
    'start_outro': 8.031,
    'end_outro': 12.031,
    'tempo': 120
    }
song2 = {
    'start_intro': 0.031,
    'end_intro': 3.87,
    'start_outro': 7.711,
    'end_outro': 11.551,
    'tempo': 125
    }
transition0 = {
    'leading_track': 0,
    'following_track': 1,
    'leading_tempo': 110,
    'following_tempo': 120,
    'types': [Transition_Types.CROSSFADE, Transition_Types.TEMPO_MATCH]
    }
transition1 = {
    'leading_track': 1,
    'following_track': 2,
    'leading_tempo': 120,
    'following_tempo': 125,
    'types': [Transition_Types.CROSSFADE, Transition_Types.TEMPO_MATCH]
    }

songs = [song0, song1, song2]
transitions = [transition0, transition1]
filepaths = [os.path.join(songs_path, "110bpm_8bars.mp3"),
             os.path.join(songs_path, "120bpm_8bars.mp3"),
             os.path.join(songs_path, "125bpm_8bars.mp3")]

c = composer.composer(songs, transitions, filepaths)
c.importaudio()
c.alignsongs()
c.applytransitions()
