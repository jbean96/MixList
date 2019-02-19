import sys
sys.path.append("..")
sys.path.append("../..")
from composer import compose
from optimizer import optimizer
from analyzer.analyzer import usersong

song_a = usersong.UserSong('/home/jwcruz/Desktop/481testsongs/songs/edm/Boomerang.mp3', True)
song_b = usersong.UserSong('/home/jwcruz/Desktop/481testsongs/songs/edm/1-01 Limbo.mp3', True)
song_c = usersong.UserSong('/home/jwcruz/Desktop/481testsongs/songs/edm/1-01 Meet In The Middle Ekali Remix.mp3', True)

mix = optimizer.generate_3_track(song_a, song_b, song_c)

c = compose(mix)
c.compose