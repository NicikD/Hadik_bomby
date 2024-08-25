from enum import Enum, auto
from game_engine import Level, StaticEngine


# Exit message values:
#  0 - Return to main menu
#  1 - Finished level
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

        self.level_finished = False

    def process_frame(self, action: "Engine.Action"):
        if action is not Engine.Action.DO_NOTHING:
            self.process_snake_movement(action)

    def process_snake_movement(self, action: "Engine.Action"):
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

            # Check if the snake tries to move in its own body
            block_at_position = None
            for i, (block) in enumerate(self.level.snake.blocks):
                if (x, y) == block:
                    block_at_position = i

            # If the snake tries to move to a new position
            if block_at_position is None:
                self.level.snake.blocks.pop()
            # If the snake tries to move in its own body moves block order
            else:
                del self.level.snake.blocks[block_at_position]
            self.level.snake.blocks.appendleft((x, y))

