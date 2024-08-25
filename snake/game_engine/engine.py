from enum import Enum, auto

from game_engine.entities import Snake
from game_engine import Level, StaticEngine, Interaction

FALLING_FREEZE_FRAMES = 6


class Engine:
    class Action(Enum):
        DO_NOTHING = auto()
        MOVE_LEFT = auto()
        MOVE_RIGHT = auto()
        MOVE_UP = auto()
        MOVE_DOWN = auto()
        RESTART = auto()

    def __init__(self, level: Level):
        self.level: Level = level

        self.static_engine = StaticEngine(level.static)

        # Falling takes a bit longer than normal movement, just for visual effect
        self.falling_animation = False
        self.falling_frame_countdown = FALLING_FREEZE_FRAMES

        self.level_finished = False

    def process_frame(self, action: "Engine.Action"):
        # Does nothing while falling
        if self.falling_animation:
            self.falling_frame_countdown -= 1
            if self.falling_frame_countdown == 0:
                self.falling_frame_countdown = FALLING_FREEZE_FRAMES
            else:
                return

        #self.process_automatic_movement()
        if  not self.falling_animation:
            self.process_player_movement(action)
        self.process_gravity()
        # TODO elektrika
        # TODO self.process_hazards()
        # TODO process interakcie return

    def process_player_movement(self, action: "Engine.Action"):
        if action is Engine.Action.DO_NOTHING:
            return

        eat_food = False

        dx, dy = 0, 0
        if action == Engine.Action.MOVE_LEFT:
            dx = -1
        elif action == Engine.Action.MOVE_RIGHT:
            dx = 1
        elif action == Engine.Action.MOVE_UP:
            dy = -1
        elif action == Engine.Action.MOVE_DOWN:
            dy = 1

        # (x, y) of where the snake tries to move to
        first_block = self.level.snake.blocks[0]
        x, y = first_block[0] + dx, first_block[1] + dy

        # If movement is within the level
        if 0 < x < self.level.width + 1 and 0 < y < self.level.height + 1:

            static_interactions = self.static_engine.get_interactions(x, y)
            if Interaction.WALL in static_interactions:
                # Cannot move there
                return
            elif Interaction.FINISH in static_interactions:
                # Finish line - ends the level
                self.level_finished = True
                return
            elif Interaction.FOOD in static_interactions:
                self.static_engine.update_eaten_food(x, y)
                eat_food = True

            # Check if the snake tries to move in its own body
            block_at_position = None
            for i, (block) in enumerate(self.level.snake.blocks):
                if (x, y) == block:
                    block_at_position = i

            # If the snake tries to move to a new position delete its tail (if not eating food)
            if block_at_position is None and not eat_food:
                self.level.snake.blocks.pop()
            # If the snake tries to move in its own body moves block order
            elif block_at_position is not None:
                del self.level.snake.blocks[block_at_position]
            self.level.snake.blocks.appendleft((x, y))

    def process_gravity(self):
        # If the snake is not on the ground it will fall
        if not any(Interaction.WALL in self.static_engine.get_interactions(x, y)
                   for x, y in self.level.snake.get_gravity_coords()):
            self.level.snake = Snake([(x, y + 1) for x, y in self.level.snake.blocks])
            self.falling_animation = True
        else:
            self.falling_animation = False
