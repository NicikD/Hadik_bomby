import scenes


# Exit message values:
#  0 - Resume level
#  1 - Exit level
#  2 - Restart level
#  3 - Open settings
class LevelMenu(scenes.Scene):
    def __init__(self, canvas):
        super().__init__(canvas, True)

        # Menu is 2x2 grid
        self.menu_selection_x = 0
        self.menu_selection_y = 0

    def process_frame(self, key_press: scenes.KeyboardInput | None):
        # Esc to exit level
        if key_press is scenes.KeyboardInput.ESC:
            self.is_running = False
            self.exit_message = 1

        # Move menu selection
        if key_press is scenes.KeyboardInput.UP:
            self.menu_selection_y = max(0, self.menu_selection_y - 1)
        elif key_press is scenes.KeyboardInput.DOWN:
            self.menu_selection_y = min(1, self.menu_selection_y + 1)
        elif key_press is scenes.KeyboardInput.LEFT:
            self.menu_selection_x = max(0, self.menu_selection_x - 1)
        elif key_press is scenes.KeyboardInput.RIGHT:
            self.menu_selection_x = min(1, self.menu_selection_x + 1)

        # Choose selected option
        if key_press is scenes.KeyboardInput.ENTER:
            x = self.menu_selection_x
            y = self.menu_selection_y

            self.is_running = False
            self.exit_message = x + 2*y

    def display_frame(self, paddingx, paddingy, screen_size) -> None:
        c = self.canvas
        # Norming map from 508x508 to square in the middle of the screen of any size
        # GUI made for 508x508 screen originally
        n = lambda x, y: scenes.Scene.normalize_to_frame(x, y, paddingx, paddingy, screen_size / 508)

        font = f"Arial {int(screen_size / 25)}"
        fill = "white"
        outline = "black"

        c.create_rectangle(n(115, 115),
                           n(395, 395),
                           width=5, fill=fill, outline=outline)

        c.create_rectangle(n(125, 125),
                           n(250, 250),
                           width=4, fill=fill, outline=outline)
        c.create_rectangle(n(260, 125),
                           n(385, 250),
                           width=4, fill=fill, outline=outline)
        c.create_rectangle(n(125, 260),
                           n(250, 385),
                           width=4, fill=fill, outline=outline)
        c.create_rectangle(n(260, 260),
                           n(385, 385),
                           width=4, fill=fill, outline=outline)

        c.create_text(n(188, 188)
                      , text="Resume", font=font, fill=outline)
        c.create_text(n(323, 188)
                      , text="Exit", font=font, fill=outline)
        c.create_text(n(188, 323)
                      , text="Restart", font=font, fill=outline)
        c.create_text(n(323, 323)
                      , text="Settings", font=font, fill=outline)

        x, y = self.menu_selection_x, self.menu_selection_y
        c.create_rectangle(n(123 + 135 * x, 123 + 135 * y),
                           n(252 + 135 * x, 252 + 135 * y),
                           fill="", outline=outline, width=11)
