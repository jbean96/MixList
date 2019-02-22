import sys
sys.path.append("..")
sys.path.append("../..")
import composer

song0 = {
    'start_intro': 0.00,
    'end_intro': 0.00,
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
    'end_outro': 15.41,
    'tempo': 125
    }
transition0 = {
    'leading_track': 0,
    'following_track': 1,
    'start_transition': song0['start_outro'],
    'end_transition': song0['end_outro'],
    'leading_tempo': 110,
    'ending_tempo': 120,
    'types': ['tempomatch', 'crossfade']
    }
transition1 = {
    'leading_track': 1,
    'following_track': 2,
    'start_transition': song1['start_outro'],
    'end_transition' : song1['end_outro'],
    'leading_tempo' : 120,
    'ending_tempo' : 125,
    'types': ['tempomatch', 'crossfade']
    }

songs = [song0, song1, song2]
transitions = [transition0, transition1]

c = composer.composer(songs, transitions)
c.new()
c.importaudio()
c.alignsongs()
c.applytransitions()
