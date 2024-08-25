from game_engine import Level, Engine
from utils import load_level
from scenes import Scene


# Exit message values:
#  0 - Exit level
#  1-16 - Finished level 1-16
class Game(Scene):
    def __init__(self, canvas, level_number):
        super().__init__(canvas)

        self.level_number = level_number

        # Camera offset because you only ever see a part of the level
        self.level, self.offsetx, self.offsety = load_level(level_number)

        # To calculate the camera offset
        self.level_width = self.level.width
        self.level_height = self.level.height

        self.engine = Engine(self.level)

    def process_frame(self, key_press):
        # Level finished succcessfully
        if self.engine.level_finished:
            return self.level_number

        # Exit level
        if key_press == "Escape":
            self.is_running = False
            self.exit_message = 0

        # Move the snake
        if key_press == "Left":
            self.update_camera_offset(Engine.Action.MOVE_LEFT)
            self.engine.process_frame(Engine.Action.MOVE_LEFT)
        elif key_press == "Right":
            self.update_camera_offset(Engine.Action.MOVE_RIGHT)
            self.engine.process_frame(Engine.Action.MOVE_RIGHT)
        elif key_press == "Up":
            self.update_camera_offset(Engine.Action.MOVE_UP)
            self.engine.process_frame(Engine.Action.MOVE_UP)
        elif key_press == "Down":
            self.update_camera_offset(Engine.Action.MOVE_DOWN)
            self.engine.process_frame(Engine.Action.MOVE_DOWN)

        # Let game process even when snake is not moving
        else:
            self.engine.process_frame(Engine.Action.DO_NOTHING)

    def display_frame(self, paddingx, paddingy, screen_size) -> None:
        self.prepare_frame(paddingx, paddingy, screen_size)

        # 17 blocks should fit on the screen
        block_size = screen_size / 17

        # Total padding takes in account the window padding and camera offset in the level
        entity_paddingx = paddingx + self.offsetx*block_size
        entity_paddingy = paddingy + self.offsety*block_size

        # 17 block size screen
        self.level.snake.draw(self.canvas, entity_paddingx, entity_paddingy, block_size)
        for entity in self.level.static + self.level.dynamic:
            entity.draw(self.canvas, entity_paddingx, entity_paddingy, block_size)

    # This does not take into account if the snake actually moved - intentional
    def update_camera_offset(self, action):
        snake_position = self.level.snake.blocks[0]
        x, y = snake_position

        # Does some checks so that the offset looks smooth (trial and error :D)
        if action == Engine.Action.MOVE_LEFT \
                and self.offsetx < -1 and x + self.offsetx < 8:
            self.offsetx += 1
        elif action == Engine.Action.MOVE_RIGHT \
                and self.offsetx > 16 - self.level_width and x + self.offsetx > 8:
            self.offsetx -= 1
        elif action == Engine.Action.MOVE_UP \
                and self.offsety < -1 and y + self.offsety < 8:
            self.offsety += 1
        elif action == Engine.Action.MOVE_DOWN \
                and self.offsety > 16 - self.level_height and y + self.offsety > 8:
            self.offsety -= 1
