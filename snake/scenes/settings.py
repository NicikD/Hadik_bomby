import tkinter

import utils
import scenes


# Exit message values:
#  0 - Exit to main menu
class Settings(scenes.Scene):
    def __init__(self, canvas, player_data: utils.PlayerData, root: tkinter.Tk, started_from_main_menu: bool):
        super().__init__(canvas, True)

        self.player_data = player_data
        self.root = root
        self.started_from_main_menu = started_from_main_menu

        # Menu has 2 options
        self.menu_selection_y = 0

    def process_frame(self, key_press: scenes.KeyboardInput | None):
        # Exit and save settings
        if key_press is scenes.KeyboardInput.ESC:
            self.is_running = False
            self.exit_message = 0

        # Move menu selection
        if self.started_from_main_menu:
            if key_press is scenes.KeyboardInput.UP:
                self.menu_selection_y = max(0, self.menu_selection_y - 1)
            elif key_press is scenes.KeyboardInput.DOWN:
                self.menu_selection_y = min(1, self.menu_selection_y + 1)

        # Change selected option
        if key_press is scenes.KeyboardInput.ENTER:
            if self.menu_selection_y == 0:
                self.player_data.fullscreen = not self.player_data.fullscreen
                self.set_fullscreen(self.player_data.fullscreen)
            elif self.menu_selection_y == 1:
                self.player_data.autoplay = not self.player_data.autoplay

    def display_frame(self, paddingx, paddingy, screen_size) -> None:
        c = self.canvas
        # Norming map from 508x508 to square in the middle of the screen of any size
        # GUI made for 508x508 screen originally
        n = lambda x, y: scenes.Scene.normalize_to_frame(x, y, paddingx, paddingy, screen_size / 508)

        font = f"Arial {int(screen_size/15)}"

        c.create_rectangle(n(20, 194),
                           n(488, 294),
                           width=5, fill="white", outline="black")

        # Shows which control is selected with a triangle
        c.create_polygon(n(30, 210 + self.menu_selection_y*40),
                         n(60, 224 + self.menu_selection_y*40),
                         n(30, 240 + self.menu_selection_y*40),
                         fill="black")

        c.create_text(n(150, 224), text="Fullscreen", font=font, fill="black")
        c.create_rectangle(n(410, 204), n(450, 244), width=7, outline="black")
        if self.player_data.fullscreen:
            c.create_line(n(410, 204), n(450, 244), width=7, fill="black")
            c.create_line(n(410, 244), n(450, 204), width=7, fill="black")

        c.create_text(n(150, 264), text="Autoplay", font=font
                      , fill="black" if self.started_from_main_menu else "gray")
        c.create_rectangle(n(410, 244), n(450, 284), width=7, outline="black")
        if self.player_data.autoplay:
            c.create_line(n(410, 244), n(450, 284), width=7, fill="black")
            c.create_line(n(410, 284), n(450, 244), width=7, fill="black")

    def set_fullscreen(self, fullscreen):
        self.root.attributes("-fullscreen", fullscreen)
        self.root.state("zoomed" if fullscreen else "normal")
