from tkinter import Canvas
from abc import ABC, abstractmethod


class Window(ABC):
    @abstractmethod
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    # Return values specific to each window
    @abstractmethod
    def process_frame(self, key_press: str) -> int:
        pass

    @abstractmethod
    def display_frame(self) -> None:
        pass
