from tkinter import Tk

from scenes import Scene
from utils import PlayerData

# Exit message values:
#  0 - Exit to main menu
class Settings(Scene):
    def __init__(self, canvas, player_data: PlayerData, root: Tk):
        super().__init__(canvas)

        self.player_data = player_data
        self.root = root

    def process_frame(self, key_press):
        # Exit to main menu
        if key_press == "Escape":
            self.is_running = False
            self.exit_message = 0

        elif key_press == "Return":
            self.player_data.fullscreen = not self.player_data.fullscreen
            self.set_fullscreen(self.player_data.fullscreen)

    def display_frame(self, paddingx, paddingy, screen_size) -> None:
        c = self.canvas
        # Norming map from 508x508 to square in the middle of the screen of any size
        # GUI made for 508x508 screen originally, too lazy to change it
        n = lambda x, y: Scene.normalize_to_frame(x, y, paddingx, paddingy, screen_size / 508)

        font = f"Arial {int(screen_size/15)}"

        self.prepare_frame(paddingx, paddingy, screen_size)

        c.create_text(n(150, 254), text="Fullscreen", font=font, fill="black")
        c.create_rectangle(n(410, 234), n(450, 274), width=7, outline="black")

        if self.player_data.fullscreen:
            c.create_line(n(410, 234), n(450, 274), width=7, fill="black")
            c.create_line(n(410, 274), n(450, 234), width=7, fill="black")

    def set_fullscreen(self, fullscreen):
        self.root.attributes("-fullscreen", fullscreen)
        self.root.state("zoomed" if fullscreen else "normal")
