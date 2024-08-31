import tkinter as tk
import time
from collections import deque

from scenes import Scene, MainMenu, Game, LevelMenu, LevelSelect, Settings, Transition
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

        # Running scenes that process user input and display on canvas
        #  main menu is the root and should never be popped
        self.scenes: deque[Scene] = deque([MainMenu(self.canvas)])

        # Screen resize manager
        self.paddingx = 0
        self.paddingy = 0
        self.screen_size = screen_size
        self.last_x = screen_size
        self.last_y = screen_size

        # Fps limiter
        self.fps = fps
        self.last_frame_time = time.monotonic()

        # For doing pretty transitions
        self.first_half_of_transition_done = False

        # Key press handler
        self.last_key_pressed = None

    # Entry point
    def run(self):
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind_all("<Key>", self.on_key_press)

        self.start_resize_manager()
        self.process()

        self.canvas.mainloop()

    # Resizes objects to fit the screen and manages fullscreen
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

        # If fullscreen was toggled from the window and not from the settings menu
        fullscreen = self.root.attributes("-fullscreen")
        if fullscreen and not self.player_data.fullscreen:
            self.player_data.fullscreen = True
            save_player_data(self.player_data)
        elif not fullscreen and self.player_data.fullscreen:
            self.player_data.fullscreen = False
            save_player_data(self.player_data)

        self.canvas.after(100, self.start_resize_manager)

    # Main event loop
    def process(self):
        top_scene = self.scenes[-1]
        key_pressed = self.last_key_pressed
        self.last_key_pressed = None

        # Sends user input to the top most scene
        top_scene.process_frame(key_pressed)

        if top_scene.is_running:
            self.display_scenes()
        # Process exit message
        else:
            message = top_scene.exit_message

            if isinstance(top_scene, MainMenu):
                # Start new game
                if message == 1:
                    self.append_with_transition(top_scene,
                                                Game(self.canvas, 1, self.player_data.autoplay, self.debug),
                                                False, 1)
                # Open level select menu
                if message == 2:
                    self.append_with_transition(top_scene, LevelSelect(self.canvas, self.player_data), True)
                # Open settings menu
                if message == 3:
                    top_scene.is_running = True
                    self.scenes.append(Settings(self.canvas, self.player_data, self.root, True))
                # Show end screen and exit application in 3 seconds
                elif message == 4:
                    top_scene.is_running = True
                    self.scenes.append(Transition(self.canvas, Transition.Type.END_APPLICATION))

            elif isinstance(top_scene, Game):
                # Open level menu
                if message == 0:
                    top_scene.is_running = True
                    self.scenes.append(LevelMenu(self.canvas))
                # Start next level
                elif 0 < message < 16:
                    self.player_data.levels[message] = True
                    save_player_data(self.player_data)
                    self.next_level_with_transition(top_scene, message + 1, self.player_data.autoplay, self.debug)
                # Does not start next level after finishing the game
                elif message == 16:
                    self.pop_with_transition(top_scene)
                    self.player_data.levels[message] = True
                    save_player_data(self.player_data)
                # Exit level
                elif message == 17:
                    self.pop_with_transition(top_scene)

            elif isinstance(top_scene, LevelMenu):
                # Resume level
                if message == 0:
                    self.scenes.pop()
                # Exit level
                elif message == 1:
                    self.scenes.pop()
                    game = self.scenes[-1]
                    game.is_running = False
                    game.exit_message = 17
                # Restart level
                elif message == 2:
                    self.scenes.pop()
                    game = self.scenes[-1]
                    game.restart_level(True)
                # Open settings
                elif message == 3:
                    top_scene.is_running = True
                    self.scenes.append(Settings(self.canvas, self.player_data, self.root, False))

            elif isinstance(top_scene, LevelSelect):
                # Exit to main menu
                if message == 0:
                    self.pop_with_transition(top_scene)
                # Start chosen level
                elif 0 < message < 17:
                    self.append_with_transition(top_scene,
                                                Game(self.canvas, message, self.player_data.autoplay, self.debug),
                                                False, message)

            elif isinstance(top_scene, Settings):
                # Save settings
                if message == 0:
                    self.scenes.pop()
                    save_player_data(self.player_data)

            elif isinstance(top_scene, Transition):
                self.scenes.pop()

                # Exit application
                if message == 0:
                    self.root.destroy()

        # Calculate delay to cap at 30 FPS
        current_time = time.monotonic()
        elapsed_time = current_time - self.last_frame_time
        delay = max(0, int((1 / self.fps - elapsed_time) * 1000))

        # Schedule next frame update
        self.last_frame_time = current_time
        self.canvas.after(delay, self.process)

    def display_scenes(self):
        # Prepares the canvas for the new frame - creates a white square in the middle of the canvas
        self.canvas.delete("all")
        self.canvas.create_rectangle(self.paddingx,
                                     self.paddingy,
                                     self.paddingx + self.screen_size,
                                     self.paddingy + self.screen_size,
                                     fill="white")

        # Pops from scenes stack until there is a non-transparent scene that will take up the whole screen
        scenes_to_draw = deque()
        while True:
            scene = self.scenes.pop()
            scenes_to_draw.append(scene)
            if not scene.transparent:
                break

        # Displays scenes in reverse order and adds them back to the scenes stack
        while scenes_to_draw:
            scene = scenes_to_draw.pop()
            scene.display_frame(self.paddingx, self.paddingy, self.screen_size)
            self.scenes.append(scene)

        self.canvas.update()

    # Append scene to the scenes stack but with a transition
    def append_with_transition(self, current: Scene, new: Scene, generic: bool, level_number: int | None = None):
        if self.first_half_of_transition_done:
            self.first_half_of_transition_done = False
            current.is_running = True

            self.scenes.append(new)
            if generic:
                self.scenes.append(Transition(self.canvas, Transition.Type.GENERIC_SECOND_HALF))
            else:
                self.scenes.append(Transition(self.canvas, Transition.Type.START_LEVEL_SECOND_HALF, level_number))

        else:
            self.first_half_of_transition_done = True

            if generic:
                self.scenes.append(Transition(self.canvas, Transition.Type.GENERIC_FIRST_HALF))
            else:
                self.scenes.append(Transition(self.canvas, Transition.Type.START_LEVEL_FIRST_HALF, level_number))

    # Pops scene from the scenes stack but with a transition
    def pop_with_transition(self, current: Scene):
        if self.first_half_of_transition_done:
            self.first_half_of_transition_done = False
            current.is_running = True

            self.scenes.pop()
            self.scenes.append(Transition(self.canvas, Transition.Type.GENERIC_SECOND_HALF))

        else:
            self.first_half_of_transition_done = True
            self.scenes.append(Transition(self.canvas, Transition.Type.GENERIC_FIRST_HALF))

    # Something between pop_with_transition and append_with_transition
    def next_level_with_transition(self, current: Scene, level_number: int, autplay: bool, debug: bool):
        if self.first_half_of_transition_done:
            self.first_half_of_transition_done = False
            current.is_running = True

            self.scenes.pop()
            self.scenes.append(Game(self.canvas, level_number, autplay, debug))
            self.scenes.append(Transition(self.canvas, Transition.Type.START_LEVEL_SECOND_HALF, level_number))

        else:
            self.first_half_of_transition_done = True
            self.scenes.append(Transition(self.canvas, Transition.Type.START_LEVEL_FIRST_HALF, level_number))

    def on_key_press(self, event):
        self.last_key_pressed = event.keysym


if __name__ == "__main__":
    app = SnakeApplication(debug=True)
    app.run()
