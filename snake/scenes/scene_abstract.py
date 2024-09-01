import tkinter
import abc
import enum


# Set to None when the key is not supported
class KeyboardInput(enum.Enum):
    ENTER = enum.auto()
    ESC = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()
    # Debug featues, the user should not use these for actually playing the game
    UNDO = enum.auto()
    STOP_MOVEMENT = enum.auto()


class Scene(abc.ABC):

    @abc.abstractmethod
    def __init__(self, canvas: tkinter.Canvas, transparent: bool):
        self.canvas = canvas

        # Stop processing when this is False
        self.is_running: bool = True
        # Only read after self.is_running==False
        # Values specific for each scene
        self.exit_message: int = 0

        # Whether the scene is transparent (should display scenes behind it)
        self.transparent = transparent

    @abc.abstractmethod
    def process_frame(self, key_press: KeyboardInput | None) -> None:
        pass

    @abc.abstractmethod
    def display_frame(self, paddingx: int, paddingy: int, screen_size: int) -> None:
        pass

    @staticmethod
    def normalize_to_frame(x, y, paddingx, paddingy, screen_size):
        return paddingx + x*screen_size, paddingy + y*screen_size
