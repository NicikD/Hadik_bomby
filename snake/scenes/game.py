from copy import deepcopy
from collections import deque
from time import monotonic

from game_engine import Action, Level, Engine
from ai import SnakeAI, get_reach, remove_invalid_neighbors
from utils import load_level
from scenes import Scene

FREEZE_FRAMES = 10


# Exit message values:
#  0 - Exit level
#  1-16 - Finished level 1-16
class Game(Scene):
    def __init__(self, canvas, level_number, autoplay, debug):
        super().__init__(canvas)

        # Whether the AI or the player is controlling the snake
        self.autoplay = autoplay

        self.debug = debug
        self.level_number = level_number

        # Camera offset because you only ever see a part of the level
        self.level, self.offsetx, self.offsety = load_level(level_number)

        # Copy of the level for restarting - just loads from here
        self.level_copy = deepcopy(self.level)
        self.offsetx_copy, self.offsety_copy = self.offsetx, self.offsety

        # Displays level number when level is started
        self.displayed_level_number = False

        # To calculate the camera offset
        self.level_width = self.level.width
        self.level_height = self.level.height

        # To calculate FPS
        self.first_frame_time = monotonic()
        self.frame_count = 0

        self.engine = Engine(self.level)

        if autoplay:
            self.ai = SnakeAI(self.level, self.engine.static_engine)
        else:
            self.ai = None
        self.ai_solution: deque[Action] = deque()
        # When the AI finds the correct path it will play it back but input slowly so the user can see the solution
        self.playback = False
        self.level_finish_frame_countdown = FREEZE_FRAMES

    def process_frame(self, key_press):
        # Playing back the AI solution
        if self.playback:
            if self.ai_solution:
                if self.level_finish_frame_countdown == 0:
                    action = self.ai_solution.popleft()
                    self.update_camera_offset(action)
                    self.engine.process_frame(action)
                    self.level_finish_frame_countdown = FREEZE_FRAMES
                else:
                    # Do nothing for this frame
                    self.level_finish_frame_countdown -= 1
                    return
                return

        # Level finished successfully (by the player)
        if self.engine.level_finished:
            self.is_running = False
            self.exit_message = self.level_number

        # Level finished successfully (by the AI)
        if self.ai and self.ai.level_finished and not self.playback:
            self.ai_solution = self.ai.final_path
            self.restart_level()
            self.playback = True

        # Exit level
        if key_press == "Escape":
            self.is_running = False
            self.exit_message = 0
            return

        move_snake = False

        if self.autoplay:
            # Let """AI""" decide what to do
            #  but not too fast because it will try to move before the level number is shown
            if self.displayed_level_number and not self.ai.level_finished:
                action = self.ai.get_next_move()

                if action in [Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.MOVE_UP, Action.MOVE_DOWN]:
                    move_snake = True
            else:
                action = Action.DO_NOTHING

        else:
            # Let game process even when snake is not moving
            action = Action.DO_NOTHING

            # Move the snake
            if key_press == "Left":
                action = Action.MOVE_LEFT
                move_snake = True
            elif key_press == "Right":
                action = Action.MOVE_RIGHT
                move_snake = True
            elif key_press == "Up":
                action = Action.MOVE_UP
                move_snake = True
            elif key_press == "Down":
                action = Action.MOVE_DOWN
                move_snake = True

            # Debug features
            # TODO remove for release
            elif key_press == "n":
                action = Action.STOP_MOVEMENT
            elif key_press == "m":
                action = Action.UNDO_MOVEMENT

        if move_snake:
            self.update_camera_offset(action)
        self.engine.process_frame(action)

        # Update camera offset when snake is falling or undoing movement or such
        if action not in [Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.MOVE_UP, Action.MOVE_DOWN] \
                and self.engine.movement_happened:
            self.update_camera_offset(self.engine.last_movement)

    def display_frame(self, paddingx, paddingy, screen_size) -> None:
        self.prepare_frame(paddingx, paddingy, screen_size)

        if not self.displayed_level_number:
            self.display_level_number(paddingx, paddingy, screen_size)
            self.displayed_level_number = True
            return

        # 17 blocks should fit on the screen
        block_size = screen_size / 17

        # Total padding takes in account the window padding and camera offset in the level
        entity_paddingx = paddingx + self.offsetx*block_size
        entity_paddingy = paddingy + self.offsety*block_size

        for entity in self.level.static + self.level.dynamic:
            entity.draw(self.canvas, entity_paddingx, entity_paddingy, block_size)
        self.level.snake.draw(self.canvas, entity_paddingx, entity_paddingy, block_size)

        # This should not be here, it's just for debugging (maybe remove later)
        if self.debug:
            if self.ai:
                self.ai.display_debug(self.canvas, entity_paddingx, entity_paddingy, block_size)
            if self.level.snake.blocks:
                first_block = self.level.snake.blocks[0]
                self.canvas.create_text(paddingx + 60, paddingy + 20, text=f"x: {first_block[0]}, y: {first_block[1]}"
                                        , font="Arial 20", fill="red")

            self.canvas.create_text(paddingx + 130, paddingy + 40, text=f"Movement stopped: {self.engine.movement_stopped}"
                                    , font="Arial 20", fill="red")

            self.canvas.create_text(paddingx + 80, paddingy + 60, text=f"Autoplay: {self.autoplay}",
                                    font="Arial 20", fill="red")

            self.canvas.create_text(paddingx + 50, paddingy + 80,
                                    text=f"FPS: {int(self.frame_count/(monotonic() - self.first_frame_time))}",
                                    font="Arial 20", fill="red")
            self.frame_count += 1

            if self.level.snake.blocks:
                reach = get_reach(self.level.snake.blocks[0], self.engine.static_engine, len(self.level.snake.blocks))
                for x, y in reach:
                    self.canvas.create_rectangle(entity_paddingx + block_size*(x + 0.3)
                                                 , entity_paddingy + block_size*(y + 0.3)
                                                 , entity_paddingx + block_size*(x + 0.7)
                                                 , entity_paddingy + block_size*(y + 0.7)
                                                 , fill="red", outline="")
                for x, y in remove_invalid_neighbors(reach, self.engine.static_engine, self.level.width, self.level.height):
                    self.canvas.create_rectangle(entity_paddingx + block_size*(x + 0.3)
                                                 , entity_paddingy + block_size*(y + 0.3)
                                                 , entity_paddingx + block_size*(x + 0.7)
                                                 , entity_paddingy + block_size*(y + 0.7)
                                                 , fill="blue", outline="")

        self.canvas.create_rectangle(0, 0, paddingx, paddingy + screen_size, fill="black", outline="black")
        self.canvas.create_rectangle(0, 0, paddingx + screen_size, paddingy, fill="black", outline="black")
        self.canvas.create_rectangle(paddingx, paddingy + screen_size
                                     , 2*paddingx + screen_size, 2*paddingy + screen_size - 1, fill="black", outline="black")
        self.canvas.create_rectangle(paddingx + screen_size, paddingy
                                     , 2*paddingx + screen_size, 2*paddingy + screen_size - 1, fill="black", outline="black")

    def display_level_number(self, paddingx, paddingy, screen_size) -> None:
        font = f"Arial {int(screen_size/2)}"

        self.canvas.delete("all")
        self.canvas.create_rectangle(paddingx, paddingy, paddingx + screen_size, paddingy + screen_size
                                     , fill="black", outline="black")
        self.canvas.create_text(paddingx + screen_size/2, paddingy + screen_size/2,
                                text=str(self.level_number), font=font, fill="white")
        self.canvas.update()
        self.canvas.after(800)

    def restart_level(self):
        self.level = deepcopy(self.level_copy)
        self.offsetx = self.offsetx_copy
        self.offsety = self.offsety_copy

        self.engine = Engine(self.level)

    # This does not take into account if the snake actually moved - intentional
    def update_camera_offset(self, action):
        if self.level.snake.blocks:
            snake_position = self.level.snake.blocks[0]
            x, y = snake_position

            # Does some checks so that the offset looks smooth (made by trial and error :D)
            if action == Action.MOVE_LEFT and self.offsetx < -1 and x + self.offsetx < 8:
                self.offsetx += 1
            elif action == Action.MOVE_RIGHT and self.offsetx > 16 - self.level_width and x + self.offsetx > 8:
                self.offsetx -= 1
            elif action == Action.MOVE_UP and self.offsety < -1 and y + self.offsety < 8:
                self.offsety += 1
            elif action == Action.MOVE_DOWN and self.offsety > 16 - self.level_height and y + self.offsety > 8:
                self.offsety -= 1
