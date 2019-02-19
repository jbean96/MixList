from composer import composer

song0 = {
    'start_intro': 0.030,
    'end_intro': 0.030,
    'start_outro': 4.32,
    'end_outro' : 8.69,
    'tempo' : 110
    }
song1 = {
    'start_intro': 0.030,
    'end_intro': 4.030,
    'start_outro': 8.03,
    'end_outro': 12.03,
    'tempo': 120
    }
song2 = {
    'start_intro': 0.030,
    'end_intro': 3.87,
    'start_outro': 3.87,
    'end_outro': 15.3,
    'tempo': 125
    }
transition0 = {
    'leading_track': 0,
    'following_track': 1,
    'start_transition': 4.32,
    'end_transition': 8.69,
    'leading_tempo': 110,
    'ending_tempo': 120,
    'types': ['tempomatch', 'crossfade']
    }
transition1 = {
    'leading_track': 1,
    'following_track': 2,
    'start_transition': 8.03,
    'end_transition' : 12.03,
    'leading_tempo' : 120,
    'ending_tempo' : 125,
    'types': ['tempomatch', 'crossfade']
    }

songs = [song0, song1, song2]
transitions = [transition0, transition1]

c = composer(songs, transitions)
c.new()
c.importaudio()
c.alignsongs()
c.applytransitions()

"""
for i in range(len(songs) - 1):
    c.tempomatch(i, i+1, songs[i], songs[i+1])
    c.crossfade(i, i+1, songs[i], songs[i+1])
"""
