import copy
import collections
import time

import utils
import game_engine
import ai
import scenes

FREEZE_FRAMES = 8


# Exit message values:
#  0 - Open menu
#  1-16 - Finished level 1-16
#  17 - Exit level
class Game(scenes.Scene):
    def __init__(self, canvas, level_number: int, autoplay: bool, debug: bool):
        super().__init__(canvas, False)

        # Whether the AI or the player is controlling the snake
        self.autoplay = autoplay

        self.debug = debug
        self.level_number = level_number

        # Camera offset because you only ever see a part of the level
        self.level, self.offsetx, self.offsety = utils.load_level(level_number)

        # Copy of the level for restarting - just loads from here
        self.level_copy = copy.deepcopy(self.level)
        self.offsetx_copy, self.offsety_copy = self.offsetx, self.offsety

        # To calculate the camera offset
        self.level_width = self.level.width
        self.level_height = self.level.height

        # To calculate FPS (only visible in debug mode)
        self.first_frame_time = time.monotonic()
        self.frame_count = 0

        self.engine: game_engine.Engine = game_engine.Engine(self.level)

        self.ai = ai.SnakeAI(self.level, self.engine.static_engine) if self.autoplay else None
        self.ai_solution: collections.deque[game_engine.Action] = collections.deque()
        # When the AI finds the correct path it will play it back but input slowly so the user can see the solution
        self.playback = False
        self.level_finish_frame_countdown = FREEZE_FRAMES

    def process_frame(self, key_press: scenes.KeyboardInput | None):
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
            self.restart_level(False)
            self.playback = True

        # Exit level
        if key_press is scenes.KeyboardInput.ESC:
            self.is_running = False
            self.exit_message = 0
            return

        move_snake = False

        if self.autoplay:
            # Let """AI""" decide what to do
            if not self.ai.level_finished:
                action = self.ai.get_next_move()

                if action in [game_engine.Action.MOVE_LEFT, game_engine.Action.MOVE_RIGHT,
                              game_engine.Action.MOVE_UP, game_engine.Action.MOVE_DOWN]:
                    move_snake = True
            else:
                action = game_engine.Action.DO_NOTHING

        else:
            # Let game process even when snake is not moving
            action = game_engine.Action.DO_NOTHING

            # Move the snake
            if key_press is scenes.KeyboardInput.LEFT:
                action = game_engine.Action.MOVE_LEFT
                move_snake = True
            elif key_press is scenes.KeyboardInput.RIGHT:
                action = game_engine.Action.MOVE_RIGHT
                move_snake = True
            elif key_press is scenes.KeyboardInput.UP:
                action = game_engine.Action.MOVE_UP
                move_snake = True
            elif key_press is scenes.KeyboardInput.DOWN:
                action = game_engine.Action.MOVE_DOWN
                move_snake = True

            # Debug features, the user should not use these for actually playing the game
            elif key_press is scenes.KeyboardInput.STOP_MOVEMENT:
                action = game_engine.Action.STOP_MOVEMENT
            elif key_press is scenes.KeyboardInput.UNDO:
                action = game_engine.Action.UNDO_MOVEMENT

        if move_snake:
            self.update_camera_offset(action)
        self.engine.process_frame(action)

        # Update camera offset when snake is falling or undoing movement or such
        if action not in [game_engine.Action.MOVE_LEFT, game_engine.Action.MOVE_RIGHT,
                          game_engine.Action.MOVE_UP, game_engine.Action.MOVE_DOWN] \
                and self.engine.movement_happened:
            self.update_camera_offset(self.engine.last_movement)

    def display_frame(self, paddingx, paddingy, screen_size) -> None:
        # 17 blocks should fit on the screen
        block_size = screen_size / 17

        # Total padding takes in account the window padding and camera offset in the level
        entity_paddingx = paddingx + self.offsetx*block_size
        entity_paddingy = paddingy + self.offsety*block_size

        for entity in self.level.static + self.level.dynamic:
            entity.draw(self.canvas, entity_paddingx, entity_paddingy, block_size)
        self.level.snake.draw(self.canvas, entity_paddingx, entity_paddingy, block_size)

        if self.debug and not self.playback:
            self.display_debug(paddingx, paddingy, entity_paddingx, entity_paddingy, block_size)

        # Shows the user that the AI is playing back the solution
        if self.autoplay:
            font = f"Arial {int(screen_size / 20)}"
            if self.playback:
                self.canvas.create_text(paddingx + screen_size*0.7,
                                        paddingy + screen_size*0.05,
                                        text=f"Playing back solution",
                                        font=font, fill="black")
            else:
                self.canvas.create_text(paddingx + screen_size*0.8,
                                        paddingy + screen_size*0.05,
                                        text=f"Finding path...",
                                        font=font, fill="black")

        # Draws black on all but the screen - creates a border for the level
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

    def restart_level(self, delete_ai_progress):
        self.level = copy.deepcopy(self.level_copy)
        self.offsetx = self.offsetx_copy
        self.offsety = self.offsety_copy

        self.engine = game_engine.Engine(self.level)

        if delete_ai_progress:
            self.ai = ai.SnakeAI(self.level, self.engine.static_engine) if self.autoplay else None

    # This does not take into account if the snake actually moved - intentional
    def update_camera_offset(self, action):
        if self.level.snake.blocks:
            snake_position = self.level.snake.blocks[0]
            x, y = snake_position

            # Does some checks so that the offset looks smooth (made by trial and error :D)
            if action == game_engine.Action.MOVE_LEFT \
                    and self.offsetx < -1 and x + self.offsetx < 8:
                self.offsetx += 1
            elif action == game_engine.Action.MOVE_RIGHT \
                    and self.offsetx > 16 - self.level_width and x + self.offsetx > 8:
                self.offsetx -= 1
            elif action == game_engine.Action.MOVE_UP \
                    and self.offsety < -1 and y + self.offsety < 8:
                self.offsety += 1
            elif action == game_engine.Action.MOVE_DOWN \
                    and self.offsety > 16 - self.level_height and y + self.offsety > 8:
                self.offsety -= 1

    # Displays whatever I needed to get the thing running :D
    def display_debug(self, paddingx, paddingy, entity_paddingx, entity_paddingy, block_size):
        if self.ai:
            if self.ai.find_path_force:
                go_here = self.ai.find_path_force.destination
                self.canvas.create_rectangle(entity_paddingx + block_size * (go_here[0]),
                                             entity_paddingy + block_size * (go_here[1]),
                                             entity_paddingx + block_size * (go_here[0] + 1),
                                             entity_paddingy + block_size * (go_here[1] + 1),
                                             fill="blue", outline="")

            if self.ai.path:
                for x, y in self.ai.path:
                    self.canvas.create_rectangle(entity_paddingx + block_size * (x + 0.1),
                                                 entity_paddingy + block_size * (y + 0.1),
                                                 entity_paddingx + block_size * (x + 0.9),
                                                 entity_paddingy + block_size * (y + 0.9),
                                                 fill="blue", outline="")

        first_block = self.level.snake.blocks[0] if self.level.snake.blocks else (-1, -1)
        self.canvas.create_text(paddingx + 120, paddingy + 20,
                                text=f"Snake head x: {first_block[0]}, y: {first_block[1]}",
                                font="Arial 20", fill="red")
        self.canvas.create_text(paddingx + 130, paddingy + 40,
                                text=f"Camera offset x: {self.offsetx}, y: {self.offsety}",
                                font="Arial 20", fill="red")
        self.canvas.create_text(paddingx + 130, paddingy + 60,
                                text=f"Movement stopped: {self.engine.movement_stopped}",
                                font="Arial 20", fill="red")
        self.frame_count += 1
        self.canvas.create_text(paddingx + 50, paddingy + 80,
                                text=f"FPS: {int(self.frame_count/(time.monotonic() - self.first_frame_time))}",
                                font="Arial 20", fill="red")

        if self.level.snake.blocks:
            reach = ai.get_reach(self.level.snake.blocks[0], self.engine.static_engine
                              , len(self.level.snake.blocks), self.level.width, self.level.height)
            for x, y in reach:
                self.canvas.create_rectangle(entity_paddingx + block_size * (x + 0.3),
                                             entity_paddingy + block_size * (y + 0.3),
                                             entity_paddingx + block_size * (x + 0.7),
                                             entity_paddingy + block_size * (y + 0.7),
                                             fill="red", outline="")

        font = f"Arial {int(block_size * 17 / 45)}"
        for x in range(self.level.width):
            for y in range(self.level.height):
                # This should not be here but whatever it's just for debug
                groups = self.engine.static_engine._position_hash[(x, y)]
                self.canvas.create_text(entity_paddingx + (x + 0.5) * block_size
                                        , entity_paddingy + (y + 0.5) * block_size
                                        , text=groups, font=font, fill="blue")
