import enum


class Action(enum.Enum):
    DO_NOTHING = enum.auto()
    MOVE_LEFT = enum.auto()
    MOVE_RIGHT = enum.auto()
    MOVE_UP = enum.auto()
    MOVE_DOWN = enum.auto()
    # Only used by the AI
    STOP_MOVEMENT = enum.auto()
    UNDO_MOVEMENT = enum.auto()
