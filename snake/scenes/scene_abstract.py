from tkinter import Canvas
from abc import ABC, abstractmethod


class Scene(ABC):

    @abstractmethod
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

        # Stop processing when this is False
        self.is_running: bool = True
        # Only read after self.is_running==False
        # Values specific for each scene
        self.exit_message: int = 0

    @abstractmethod
    def process_frame(self, key_press: str) -> None:
        pass

    @abstractmethod
    def display_frame(self, paddingx: int, paddingy: int, screen_size: int) -> None:
        pass

    def prepare_frame(self, paddingx, paddingy, screen_size):
        self.canvas.delete("all")
        self.canvas.create_rectangle(paddingx, paddingy, paddingx + screen_size, paddingy + screen_size, fill="white")

    @staticmethod
    def normalize_to_frame(x, y, paddingx, paddingy, screen_size):
        return paddingx + x * screen_size, paddingy + y * screen_size
