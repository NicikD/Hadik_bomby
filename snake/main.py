import tkinter as tk
import time

from scenes import Scene, MainMenu, Game, End

# Defaults
SCREEN_SIZE = 700
FPS = 30


class SnakeApplication:

    def __init__(self, screen_size=SCREEN_SIZE, fps=FPS):
        # Application output
        self.root = tk.Tk()
        self.root.title("Snake")
        self.root.minsize(100, 100)
        self.canvas = tk.Canvas(master=self.root, bg="black", width=screen_size, height=screen_size)

        # Running scene that processes user input and displays on canvas
        self.scene: Scene = MainMenu(self.canvas)

        # Screen resize manager
        self.paddingx = 0
        self.paddingy = 0
        self.screen_size = screen_size
        self.last_x = screen_size
        self.last_y = screen_size

        # Fps limiter
        self.fps = fps
        self.last_frame_time = time.monotonic()

        # Key press handler
        self.last_key_pressed = None

    # Entry point
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

    # Main event loop
    def process(self):
        key_pressed = self.last_key_pressed
        self.last_key_pressed = None

        self.scene.process_frame(key_pressed)

        if self.scene.is_running:
            self.scene.display_frame(self.paddingx, self.paddingy, self.screen_size)
            self.canvas.update()
        # Process exit message
        else:
            message = self.scene.exit_message

            if isinstance(self.scene, MainMenu):
                # Start new game
                if message == 1:
                    self.scene = Game(self.canvas, 1)
                # Show end screen and exit application in 3 seconds
                elif message == 4:
                    self.scene = End(self.canvas)

            elif isinstance(self.scene, Game):
                # Start main menu (0 - exit level, 16 - finished last level)
                if message == 0 or message == 16:
                    self.scene = MainMenu(self.canvas)
                # Start next level
                elif 0 < message < 16:
                    # TODO save progress
                    self.scene = Game(self.canvas, message + 1)

            elif isinstance(self.scene, End):
                # Exit application
                if message == 1:
                    self.root.destroy()

        # Calculate delay to cap at 30 FPS
        current_time = time.monotonic()
        elapsed_time = current_time - self.last_frame_time
        delay = max(0, int((1 / self.fps - elapsed_time) * 1000))

        # Schedule next frame update
        self.last_frame_time = current_time
        self.canvas.after(delay, self.process)

    def on_key_press(self, event):
        self.last_key_pressed = event.keysym


if __name__ == "__main__":
    app = SnakeApplication(screen_size=SCREEN_SIZE, fps=FPS)
    app.run()
