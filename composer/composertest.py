from composer import composer

song0 = {
    'start_intro': 0.030,
    'end_intro': 0.030,
    'start_outro': 4.32,
    'end_outro' : 8.69,
    'tempo' : 110,
    'offset' : 0
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
songs = [song0, song1, song2]

c = composer(songs)
c.new()
c.importaudio()
c.alignsongs()

for i in range(len(songs) - 1):
    c.crossfade(i, i+1, songs[i], songs[i+1])
    c.tempomatch(i, i+1, songs[i], songs[i+1])

