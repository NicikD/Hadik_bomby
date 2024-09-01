from tkinter import Canvas
from abc import ABC, abstractmethod
from enum import Enum, auto


# Set to None when the key is not supported
class KeyboardInput(Enum):
    ENTER = auto()
    ESC = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    # Debug featues, the user should not use these for actually playing the game
    UNDO = auto()
    STOP_MOVEMENT = auto()


class Scene(ABC):

    @abstractmethod
    def __init__(self, canvas: Canvas, transparent: bool):
        self.canvas = canvas

        # Stop processing when this is False
        self.is_running: bool = True
        # Only read after self.is_running==False
        # Values specific for each scene
        self.exit_message: int = 0

        # Whether the scene is transparent (should display scenes behind it)
        self.transparent = transparent

    @abstractmethod
    def process_frame(self, key_press: KeyboardInput | None) -> None:
        pass

    @abstractmethod
    def display_frame(self, paddingx: int, paddingy: int, screen_size: int) -> None:
        pass

    @staticmethod
    def normalize_to_frame(x, y, paddingx, paddingy, screen_size):
        return paddingx + x*screen_size, paddingy + y*screen_size
