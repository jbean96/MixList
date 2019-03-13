from enum import Enum, auto


class Transition_Types(Enum):
    CROSSFADE = auto()
    TEMPO_MATCH = auto()
    NONE = auto()


class Effect_Types(Enum):
    FADEIN = auto()
    FADEOUT = auto()
    NONE = auto()
