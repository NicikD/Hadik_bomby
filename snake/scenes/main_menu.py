from scenes import Scene


# Exit message values:
#  1 - Start new game
#  2 - Open level select menu
#  3 - Open settings
#  4 - Exit application
class MainMenu(Scene):
    def __init__(self, canvas):
        super().__init__(canvas)

        # Menu is 2x2 grid
        self.menu_selection_x = 0
        self.menu_selection_y = 0

    def process_frame(self, key_press):
        # Esc to exit application
        if key_press == "Escape":
            self.is_running = False
            self.exit_message = 4

        # Move menu selection
        elif key_press == "Up":
            self.menu_selection_y = max(0, self.menu_selection_y - 1)
        elif key_press == "Down":
            self.menu_selection_y = min(1, self.menu_selection_y + 1)
        elif key_press == "Left":
            self.menu_selection_x = max(0, self.menu_selection_x - 1)
        elif key_press == "Right":
            self.menu_selection_x = min(1, self.menu_selection_x + 1)

        elif key_press == "Return":
            self.is_running = False
            x = self.menu_selection_x
            y = self.menu_selection_y

            if x == 0 and y == 0:
                # Start new game
                self.exit_message = 1
            elif x == 1 and y == 0:
                # Open level select menu
                self.exit_message = 2
            elif x == 0 and y == 1:
                # Open settings
                self.exit_message = 3
            elif x == 1 and y == 1:
                # Exit application
                self.exit_message = 4

    def display_frame(self, paddingx, paddingy, screen_size) -> None:
        c = self.canvas
        # Norming map from 508x508 to square in the middle of the screen of any size
        # GUI made for 508x508 screen originally, too lazy to change it
        n = lambda x, y: Scene.normalize_to_frame(x, y, paddingx, paddingy, screen_size/508)

        font_enter = f"Arial {int(screen_size/30)}"
        font_menu = f"Arial {int(screen_size/25)}"
        font_arrows = f"Arial {int(screen_size/20)}"
        color = "black"

        self.prepare_frame(paddingx, paddingy, screen_size)

        c.create_rectangle(n(30, 30), n(240, 160), width=5, outline=color)
        c.create_rectangle(n(270, 30), n(480, 160), width=5, outline=color)
        c.create_rectangle(n(30, 190), n(240, 320), width=5, outline=color)
        c.create_rectangle(n(270, 190), n(480, 320), width=5, outline=color)
        c.create_text(n(135, 95), text="Start new game", font=font_menu, fill=color)
        c.create_text(n(375, 95), text="Level select", font=font_menu, fill=color)
        c.create_text(n(135, 255), text="Settings", font=font_menu, fill=color)
        c.create_text(n(375, 255), text="Exit", font=font_menu, fill=color)

        c.create_rectangle(n(270, 415), n(480, 480), width=5, outline=color)
        c.create_rectangle(n(340, 350), n(410, 480), width=5, outline=color)
        c.create_text(n(375, 375), text="↑", font=font_arrows, fill=color)
        c.create_text(n(375, 440), text="↓", font=font_arrows, fill=color)
        c.create_text(n(445, 442), text="→", font=font_arrows, fill=color)
        c.create_text(n(305, 442), text="←", font=font_arrows, fill=color)
        c.create_text(n(125, 380), text="ENTER", font=font_enter, fill=color)
        c.create_polygon(n(80, 350), n(170, 350), n(170, 480), n(100, 480), n(100, 410), n(80, 410)
                         , fill="", outline=color, width=5)

        menu_x = self.menu_selection_x
        menu_y = self.menu_selection_y
        c.create_rectangle(n(28 + 240 * menu_x, 28 + 160 * menu_y), n(242 + 240 * menu_x, 162 + 160 * menu_y)
                           , width=11, outline="black")
