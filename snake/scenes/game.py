from game_engine import Level, Engine
from utils import load_level
from scenes import Scene


# Exit message values:
#  0 - Exit level
#  1-16 - Finished level 1-16
class Game(Scene):
    def __init__(self, canvas, level_number, debug):
        super().__init__(canvas)

        self.debug = debug
        self.level_number = level_number

        # Camera offset because you only ever see a part of the level
        self.level, self.offsetx, self.offsety = load_level(level_number)

        # Displays level number when level is started
        self.displayed_level_number = False

        # To calculate the camera offset
        self.level_width = self.level.width
        self.level_height = self.level.height

        self.engine = Engine(self.level)

    def process_frame(self, key_press):
        # Level finished succcessfully
        if self.engine.level_finished:
            self.is_running = False
            self.exit_message = self.level_number

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
        # Debug features
        # TODO remove for release
        elif key_press == "n":
            self.engine.process_frame(Engine.Action.STOP_MOVEMENT)
        elif key_press == "m":
            self.engine.process_frame(Engine.Action.UNDO_MOVEMENT)

        # Let game process even when snake is not moving
        else:
            self.engine.process_frame(Engine.Action.DO_NOTHING)

        # Update camera offset when snake is falling or undoing movement or such
        if key_press not in ["Left", "Right", "Up", "Down"] and self.engine.movement_happened:
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
            if self.level.snake.blocks:
                first_block = self.level.snake.blocks[0]
                self.canvas.create_text(paddingx + 60, paddingy + 20, text=f"x: {first_block[0]}, y: {first_block[1]}"
                                        , font="Arial 20", fill="red")

            self.canvas.create_text(paddingx + 120, paddingy + 40, text=f"Movement stopped: {self.engine.movement_stopped}"
                                    , font="Arial 20", fill="red")

            for x in range(self.level.width):
                for y in range(self.level.height):
                    groups = self.engine.static_engine._position_hash[(x, y)]
                    self.canvas.create_text(entity_paddingx + (x + 0.5)*block_size
                                            , entity_paddingy + (y + 0.5)*block_size
                                            , text=groups, font="Arial 20", fill="red")

    def display_level_number(self, paddingx, paddingy, screen_size) -> None:
        font = f"Arial {int(screen_size/2)}"

        self.canvas.delete("all")
        self.canvas.create_rectangle(paddingx, paddingy, paddingx + screen_size, paddingy + screen_size
                                     , fill="black", outline="black")
        self.canvas.create_text(paddingx + screen_size/2, paddingy + screen_size/2,
                                text=str(self.level_number), font=font, fill="white")
        self.canvas.update()
        self.canvas.after(800)

    # This does not take into account if the snake actually moved - intentional
    def update_camera_offset(self, action):
        if self.level.snake.blocks:
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
