from enum import auto, Enum
from typing import List

class Mode(Enum):
    MINOR = 0
    MAJOR = 1

STRING_TO_MODE = {
    "major" : Mode.MAJOR,
    "minor" : Mode.MINOR
}

# Internal key representation
class Key(Enum):
    NO_KEY =  -1
    C =       0
    C_SHARP = 1
    D_FLAT =  1
    D =       2
    D_SHARP = 3
    E_FLAT =  3
    E =       4
    F =       5
    F_SHARP = 6
    G_FLAT =  6
    G =       7
    G_SHARP = 8
    A_FLAT =  8
    A =       9
    A_SHARP = 10
    B_FLAT =  10
    B =       11

STRING_TO_KEY = {
    "C" : Key.C,
    "C#" : Key.C_SHARP,
    "Db" : Key.D_FLAT,
    "D" : Key.D,
    "D#" : Key.D_SHARP,
    "Eb" : Key.E_FLAT,
    "E" : Key.E,
    "F" : Key.F,
    "F#" : Key.F_SHARP,
    "Gb" : Key.G_FLAT,
    "G" : Key.G,
    "G#" : Key.G_SHARP,
    "Ab" : Key.A_FLAT,
    "A" : Key.A,
    "A#" : Key.A_SHARP,
    "Bb" : Key.B_FLAT,
    "B" : Key.B
}

# Spotify value -> Internal mode
SPOTIFY_MODE = {
    0 : Mode.MINOR,
    1 : Mode.MAJOR
}

# Spotify value -> Internal key
SPOTIFY_KEYS = {
    -1 : Key.NO_KEY,
    0  : Key.C,
    1  : Key.C_SHARP,
    2  : Key.D,
    3  : Key.D_SHARP,
    4  : Key.E,
    5  : Key.F,
    6  : Key.F_SHARP,
    7  : Key.G,
    8  : Key.G_SHARP,
    9  : Key.A,
    10 : Key.A_SHARP,
    11 : Key.B
}

class KeyRelationship(Enum):
    EXACT = auto()
    RELATIVE_KEY = auto()
    PARALLEL_KEY = auto()
    PERFECT_FOURTH = auto()
    PERFECT_FIFTH = auto()
    NONE = auto()

KEY_RELATIONSHIP_SCORE = {
    KeyRelationship.EXACT : 1.0,
    KeyRelationship.PERFECT_FIFTH : 0.5,
    KeyRelationship.PERFECT_FOURTH : 0.5,
    KeyRelationship.RELATIVE_KEY : 0.3,
    KeyRelationship.PARALLEL_KEY : 0.2,
    KeyRelationship.NONE : 0.0
}

class Camelot:
    MODES = ['A', 'B']

    # For typing the class name has to be in strings if the entire class hasn't been evaluated yet
    def __init__(self, key: int, mode: str) -> 'Camelot':
        if mode not in Camelot.MODES:
            raise ValueError('Mode must be one of %s' % Camelot.MODES)
    
        self._key = key
        self._mode = mode

    def get_relationship(self, other: 'Camelot') -> KeyRelationship:
        """
        Gets the key relationship between this key and other

        @param other: The other Camelot key to compare to
        @return: The KeyRelationship enum describing the relationship
        """
        if self == other:
            return KeyRelationship.EXACT
        elif self.perfect_fifth() == other:
            return KeyRelationship.PERFECT_FIFTH
        elif self.perfect_fourth() == other:
            return KeyRelationship.PERFECT_FOURTH
        elif self.relative_key() == other:
            return KeyRelationship.RELATIVE_KEY
        elif self.parallel_key() == other:
            return KeyRelationship.PARALLEL_KEY
        else:
            return KeyRelationship.NONE

    def compare(self, other: 'Camelot') -> float:
        """
        Compares two Camelot keys and returns the comparison score as defined
        by the MIREX score weightings for comparing keys

        @param other: The other Camelot key to compare to
        @return: A float indicating the score from comparing these two keys
        """
        return KEY_RELATIONSHIP_SCORE[self.get_relationship(other)]

    def relative_key(self) -> 'Camelot':
        return self.change_mode()

    def parallel_key(self) -> 'Camelot':
        key_tup = INVERSE_CAMELOT_KEYS[self]
        if key_tup[1] == Mode.MAJOR:
            key_tup = (key_tup[0], Mode.MINOR)
        elif key_tup[1] == Mode.MINOR:
            key_tup = (key_tup[0], Mode.MAJOR)
        else:
            raise ValueError("%s is not a mode" % key_tup[1])
        return CAMELOT_KEYS[key_tup]

    def perfect_fifth(self) -> 'Camelot':
        return self.shift_up()

    def perfect_fourth(self) -> 'Camelot':
        return self.shift_down()

    def shift_up(self) -> 'Camelot':
        new_key = self._key + 1
        return Camelot(new_key if new_key <= 12 else 1, self._mode)
    
    def shift_down(self) -> 'Camelot':
        new_key = self._key - 1
        return Camelot(new_key if new_key >= 1 else 12, self._mode)

    def __str__(self) -> str:
        return str(self._key) + self._mode

    def change_mode(self) -> 'Camelot':
        new_mode = Camelot.MODES[(Camelot.MODES.index(self._mode) + 1) % len(Camelot.MODES)]
        return Camelot(self._key, new_mode)

    def get_key(self) -> int:
        return self._key
    
    def get_mode(self) -> int:
        return self._mode

    def get_adjacent_keys(self) -> List['Camelot']:
        return [self.shift_up(), self.shift_down(), self.change_mode()]

    def __hash__(self):
        return hash((self._key, self._mode))

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self._key == other._key and self._mode == other._mode

# Mapping of internal key representation (Key, Mode) to the corresponding Camelot Key
CAMELOT_KEYS = {
    # Mode.MINOR keys
    (Key.A_FLAT, Mode.MINOR)  : Camelot(1, 'A'),
    (Key.E_FLAT, Mode.MINOR)  : Camelot(2, 'A'),
    (Key.B_FLAT, Mode.MINOR)  : Camelot(3, 'A'),
    (Key.F, Mode.MINOR)       : Camelot(4, 'A'),
    (Key.C, Mode.MINOR)       : Camelot(5, 'A'),
    (Key.G, Mode.MINOR)       : Camelot(6, 'A'),
    (Key.D, Mode.MINOR)       : Camelot(7, 'A'),
    (Key.A, Mode.MINOR)       : Camelot(8, 'A'),
    (Key.E, Mode.MINOR)       : Camelot(9, 'A'),
    (Key.B, Mode.MINOR)       : Camelot(10, 'A'),
    (Key.F_SHARP, Mode.MINOR) : Camelot(11, 'A'),
    (Key.D_FLAT, Mode.MINOR)  : Camelot(12, 'A'),
    # Mode.MAJOR keys
    (Key.B, Mode.MAJOR)       : Camelot(1, 'B'),
    (Key.F_SHARP, Mode.MAJOR) : Camelot(2, 'B'),
    (Key.D_FLAT, Mode.MAJOR)  : Camelot(3, 'B'),
    (Key.A_FLAT, Mode.MAJOR)  : Camelot(4, 'B'),
    (Key.E_FLAT, Mode.MAJOR)  : Camelot(5, 'B'),
    (Key.B_FLAT, Mode.MAJOR)  : Camelot(6, 'B'),
    (Key.F, Mode.MAJOR)       : Camelot(7, 'B'),
    (Key.C, Mode.MAJOR)       : Camelot(8, 'B'),
    (Key.G, Mode.MAJOR)       : Camelot(9, 'B'),
    (Key.D, Mode.MAJOR)       : Camelot(10, 'B'),
    (Key.A, Mode.MAJOR)       : Camelot(11, 'B'),
    (Key.E, Mode.MAJOR)       : Camelot(12, 'B'),
    # No key
    (Key.NO_KEY, Mode.MAJOR)  : None,
    (Key.NO_KEY, Mode.MINOR)  : None
}

INVERSE_CAMELOT_KEYS = dict((v, k) for k, v in CAMELOT_KEYS.items() if v is not None)

def key_from_string(key_string: str) -> Camelot:
    """
    Takes a string of a key like 'C major' and turns it into the corresponding 
    Camelot key, valid strings are like
    """
    (key, mode) = key_string.split(" ")
    dict_key = (STRING_TO_KEY[key], STRING_TO_MODE[mode])
    if dict_key not in CAMELOT_KEYS:
        raise Exception("%s is not valid input" % key_string)
    return CAMELOT_KEYS[dict_key]
    
def spotify_to_camelot(key: int, mode: int) -> Camelot:
    """
    Takes the Spotify encoded key and mode and returns the camelot key string

    @param key: The key value returned by the Spotify API
    @param mode: The mode value returned by the Spotify API
    @return: The Camelot key value corresponding to the provided Spotify values, or None if one doesn't exist
    """
    internal_key = SPOTIFY_KEYS[key]
    internal_mode = SPOTIFY_MODE[mode]

    return CAMELOT_KEYS[(internal_key, internal_mode)]