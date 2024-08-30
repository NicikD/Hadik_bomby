from enum import Enum, auto


class Action(Enum):
    DO_NOTHING = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    RESTART = auto()
    # Debug features
    STOP_MOVEMENT = auto()
    UNDO_MOVEMENT = auto()
