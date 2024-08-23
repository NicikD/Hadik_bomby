import tkinter as tk

from generic_window import Window


class MainMenu(Window):
    def __init__(self, canvas):
        super().__init__(canvas)



    # Return values:
    #     0 - Keep running
    #     1 - Start new game
    #     2 - Open level editor
    #     3 - Open settings
    #     4 - Exit application
    def process_frame(self, key_press):
        pass

    def display_frame(self):
        pass
