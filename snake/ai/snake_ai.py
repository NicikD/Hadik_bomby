from collections import deque
from tkinter import Canvas
from math import hypot

from game_engine.entities import Food, Finish
from game_engine import Level, StaticEngine, Action, Interaction
from ai import get_reach, FindPathStatic, FindPathForce


# "AI" is a strong name for this almost brute force algorithm but whatever
class SnakeAI:
    def __init__(self, level: Level, engine: StaticEngine):
        self.level: Level = level
        self.engine: StaticEngine = engine

        # The path from start to finish
        self.final_path: deque[Action] = deque()

        # Finds path and splits it into simple parts that can get reached with brute force
        self.find_path: FindPathStatic = FindPathStatic(self.engine, self.level.width, self.level.height)
        # The path to the nearest interesting point (food or finish)
        self.path: deque[tuple[int, int]] | None = None

        # Brute force path to the next block in the path
        self.find_path_force: FindPathForce | None = None

        # The victory square, not used for pathfinding but for when to stop pathfinding and return the solution
        self.victory_square: tuple[int, int] | None = None
        self.level_finished = False

        # First move is always down because the snake does not start on the ground
        self.first_move = True

    def get_next_move(self):
        # First move is always down because the snake does not start on the ground - too lazy to account for this
        if self.first_move:
            self.first_move = False
            self.final_path.append(Action.MOVE_DOWN)
            return Action.MOVE_DOWN

        if self.find_path_force:
            if self.find_path_force.is_finished:
                self.find_path_force = None

                return self.get_next_move()
            else:
                # Continue with brute force
                move = self.find_path_force.get_next_move()

                # Save move to reconstruct the path
                if move == Action.UNDO_MOVEMENT:
                    self.final_path.pop()
                elif move in [Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.MOVE_UP, Action.MOVE_DOWN]:
                    self.final_path.append(move)

                # If the snake is about to win stops pathfinding and shows the final AI solution
                if self.about_to_win():
                    self.level_finished = True
                    return Action.DO_NOTHING

                return move

        snake_head = self.level.snake.blocks[0]

        # Go to the next block in the path
        if self.path:
            self.find_path_force = FindPathForce(snake_head, self.path.popleft(), self.engine,
                                                 len(self.level.snake.blocks), self.level.width, self.level.height)
            return self.get_next_move()

        # Update length if the snake just ate food
        self.find_path.update_lenght(len(self.level.snake.blocks))

        # Find path to the nearest food
        nearest_food = self.get_nearest_food()
        if nearest_food:
            # There is food on the map, try to find a path to it

            self.path = self.find_path.astar(snake_head, nearest_food)
            return self.get_next_move()

        # All food eaten, find path to the finish
        nearest_finish = self.get_nearest_finish()
        self.victory_square = nearest_finish
        self.path = self.find_path.astar(snake_head, nearest_finish)
        return self.get_next_move()

    # Returns the nearest food to the current snake head
    def get_nearest_food(self) -> tuple[int, int] | None:
        all_food = [
            entity for entity in self.level.static
            if isinstance(entity, Food)
            and Interaction.FOOD in self.engine.get_interactions(entity.x, entity.y)
                    ]

        if all_food:
            snake_head = self.level.snake.blocks[0]
            all_food.sort(key=lambda food: hypot(food.x - snake_head[0], food.y - snake_head[1]))

            return all_food[0].get_interact_coords()[0]
        else:
            return None

    def get_nearest_finish(self) -> tuple[int, int]:
        all_finish = list(filter(lambda entity: isinstance(entity, Finish), self.level.static))[0].get_interact_coords()
        snake_head = self.level.snake.blocks[0]

        all_finish.sort(key=lambda finish: hypot(finish[0] - snake_head[0], finish[1] - snake_head[1]))

        return all_finish[0]

    # All reachable positions from the snake head
    def get_reach(self) -> list[tuple[int, int]]:
        snake_head = self.level.snake.blocks[0]
        return get_reach(snake_head[0], snake_head[1], len(self.level.snake.blocks))

    def about_to_win(self):
        if not self.victory_square:
            return False
        else:
            snake_head = self.level.snake.blocks[0]
            return abs(snake_head[0] - self.victory_square[0]) + abs(snake_head[1] - self.victory_square[1]) == 1
