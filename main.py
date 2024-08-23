import tkinter as tk
import time

from gui import Window, MainMenu

# Defaults
SCREEN_SIZE = 600


class SnakeApplication:

    def __init__(self, screen_size=SCREEN_SIZE):
        # Application output
        self.canvas = tk.Canvas(bg="black", width=screen_size, height=screen_size)

        # Window manager (actually there is only one window at any time :D)
        self.window: Window = MainMenu(self.canvas)

        # Screen resize manager
        self.paddingx = 0
        self.paddingy = 0
        self.screen_size = screen_size
        self.last_x = screen_size
        self.last_y = screen_size

        # Fps limiter
        self.last_frame_time = time.monotonic()

        # Key press handler
        self.last_key_pressed = None

    def run(self):
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind_all("<Key>", self.on_key_press)

        self.start_resize_manager()
        self.process()

        self.canvas.mainloop()

    def start_resize_manager(self):
        x = self.canvas.winfo_width()
        y = self.canvas.winfo_height()

        if x != self.last_x or y != self.last_y:
            self.screen_size = min(x, y)

            if x >= y:
                (self.paddingx) = (x - self.screen_size) / 2
                self.paddingy = 0
            else:
                self.paddingx = 0
                self.paddingy = (y - self.screen_size) / 2

            self.last_x = x
            self.last_y = y

        self.canvas.after(100, self.start_resize_manager)

    # The main event loop
    def process(self):
        key_pressed = self.last_key_pressed
        self.last_key_pressed = None

        self.window.process_frame(key_pressed)
        self.window.display_frame()

        # Calculate delay to cap at 30 FPS
        current_time = time.monotonic()
        elapsed_time = current_time - self.last_frame_time
        delay = max(0, int((1 / 30 - elapsed_time) * 1000))

        # Schedule next frame update
        self.last_frame_time = current_time
        self.canvas.after(delay, self.process)

    def on_key_press(self, event):
        self.last_key_pressed = event.keysym


if __name__ == "__main__":
    app = SnakeApplication(screen_size=SCREEN_SIZE)
    app.run()
