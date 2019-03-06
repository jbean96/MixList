from enum import Enum, auto


class Transition_Types(Enum):
    CROSSFADE = auto()
    TEMPO_MATCH = auto()
    TEMPO_MATCH2 = auto()
    NONE = auto()


class Effect_Types(Enum):
    FADEIN = auto()
    FADEOUT = auto()
    CHANGE_TEMPO = auto()
    SLIDING_STRECH = auto()
    NONE = auto()
