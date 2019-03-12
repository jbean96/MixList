from enum import Enum
"""
A numpy.array interpretted to
quanitify the outcome of a mix
OR  
a DJ's style.

Uses features [TEMPO, KEY, DANCEABILITY, ENERGY, VALENCE] enumerized Cue.
"""
class Cue(Enum):
    TEMPO = 0
    KEY = 1
    DANCE = 2
    ENERGY = 3
    VALENCE = 4