import tkinter as tk
import time

from scenes import Scene, MainMenu, Game, LevelSelect, Settings, End
from utils import PlayerData, load_player_data, save_player_data


class SnakeApplication:
    def __init__(self, screen_size=700, fps=60, force_fullscreen=False, force_autoplay=False, debug=False):
        self.debug = debug

        # Player data
        self.player_data: PlayerData = load_player_data()
        if force_fullscreen:
            self.player_data.fullscreen = True
        if force_autoplay:
            self.player_data.autoplay = True

        # Application output
        self.root = tk.Tk()
        self.root.title("Snake")
        self.root.minsize(100, 100)
        self.root.geometry(f"{screen_size}x{screen_size}")
        if self.player_data.fullscreen:
            self.root.attributes("-fullscreen", True)
            self.root.state("zoomed")
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
                    self.scene = Game(self.canvas, 1, self.player_data.autoplay, self.debug)
                # Open level select menu
                if message == 2:
                    self.scene = LevelSelect(self.canvas, self.player_data)
                # Open settings menu
                if message == 3:
                    self.scene = Settings(self.canvas, self.player_data, self.root)
                # Show end screen and exit application in 3 seconds
                elif message == 4:
                    self.scene = End(self.canvas)

            elif isinstance(self.scene, Game):
                # Start main menu
                if message == 0:
                    self.scene = MainMenu(self.canvas)
                # Start next level
                elif 0 < message < 16:
                    self.player_data.levels[message] = True
                    save_player_data(self.player_data)
                    self.scene = Game(self.canvas, message + 1, self.player_data.autoplay, self.debug)
                # Return to menu after finishing the game
                elif message == 16:
                    self.player_data.levels[message] = True
                    save_player_data(self.player_data)
                    self.scene = MainMenu(self.canvas)

            elif isinstance(self.scene, LevelSelect):
                # Exit to main menu
                if message == 0:
                    self.scene = MainMenu(self.canvas)
                # Start chosen level
                elif 0 < message < 17:
                    self.scene = Game(self.canvas, message, self.player_data.autoplay, self.debug)

            elif isinstance(self.scene, Settings):
                # Exit to main menu
                if message == 0:
                    save_player_data(self.player_data)
                    self.scene = MainMenu(self.canvas)

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
    app = SnakeApplication(debug=True)
    app.run()
