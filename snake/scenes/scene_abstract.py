from tkinter import Canvas
from abc import ABC, abstractmethod


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
    def process_frame(self, key_press: str) -> None:
        pass

    @abstractmethod
    def display_frame(self, paddingx: int, paddingy: int, screen_size: int) -> None:
        pass

    @staticmethod
    def normalize_to_frame(x, y, paddingx, paddingy, screen_size):
        return paddingx + x*screen_size, paddingy + y*screen_size
