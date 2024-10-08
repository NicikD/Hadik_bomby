import utils
import scenes


# Exit message values:
#  0 - Exit to main menu
#  1-16 - Start level 1-16
class LevelSelect(scenes.Scene):
    def __init__(self, canvas, player_data: utils.PlayerData):
        super().__init__(canvas, False)

        self.levels = player_data.levels
        self.levels[0] = True

        # Menu is 4x4 grid
        self.menu_selection_x = 0
        self.menu_selection_y = 0

    def process_frame(self, key_press: scenes.KeyboardInput | None):
        # Exit to main menu
        if key_press is scenes.KeyboardInput.ESC:
            self.is_running = False
            self.exit_message = 0

        # Move menu selection
        elif key_press is scenes.KeyboardInput.UP:
            self.menu_selection_y = max(0, self.menu_selection_y - 1)
        elif key_press is scenes.KeyboardInput.DOWN:
            self.menu_selection_y = min(3, self.menu_selection_y + 1)
        elif key_press is scenes.KeyboardInput.LEFT:
            self.menu_selection_x = max(0, self.menu_selection_x - 1)
        elif key_press is scenes.KeyboardInput.RIGHT:
            self.menu_selection_x = min(3, self.menu_selection_x + 1)

        # Start the level if it is unlocked
        elif key_press is scenes.KeyboardInput.ENTER and \
                (self.levels[self.level_number()] or (self.menu_selection_x == 0 and self.menu_selection_y == 0)):
            self.is_running = False
            self.exit_message = self.level_number()

    def display_frame(self, paddingx, paddingy, screen_size) -> None:
        c = self.canvas
        # Norming map from 508x508 to square in the middle of the screen of any size
        # GUI made for 508x508 screen originally
        n = lambda x, y: scenes.Scene.normalize_to_frame(x, y, paddingx, paddingy, screen_size / 508)

        font = f"Arial {int(screen_size/10)}"

        for dx in range(4):
            for dy in range(4):
                if self.levels[coords_to_number(dx, dy)] or (dx == 0 and dy == 0):
                    c.create_rectangle(n(22 + 122 * dx,                                      # :DDD
                                         22 + 122 * dy),
                                       n(122 + 122 * dx,
                                         122 + 122 * dy),
                                       width=5, outline="black")
                    c.create_text(n(72 + 122 * dx,
                                    72 + 122 * dy)
                                  , text=str(4*dy + dx + 1), font=font, fill="black")
                else:
                    c.create_rectangle(n(22 + 122 * dx,
                                         22 + 122 * dy),
                                       n(122 + 122 * dx,
                                         122 + 122 * dy),
                                       width=5, fill="black", outline="black")

        if self.levels[self.level_number()] or (self.menu_selection_x == 0 and self.menu_selection_y == 0):
            c.create_rectangle(n(20 + 122 * self.menu_selection_x,
                                 20 + 122 * self.menu_selection_y),
                               n(124 + 122 * self.menu_selection_x,
                                 124 + 122 * self.menu_selection_y),
                               width=11, outline="black")
        else:
            c.create_text(n(72 + 122 * self.menu_selection_x,
                            72 + 122 * self.menu_selection_y)
                          , text=str(self.level_number()), font=font, fill="white")

    # Returns the selected level number from x, y coords
    def level_number(self):
        return coords_to_number(self.menu_selection_x, self.menu_selection_y)


# Returns the selected level number from x, y coords
def coords_to_number(x, y):
    return 4*y + x + 1
