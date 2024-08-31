from astar import AStar
from collections import deque

from utils import get_connected_blocks
from ai import get_reach


# Only computed a couple of times per level
class FindPathStatic(AStar):
    def __init__(self, engine, level_width, level_height):
        super().__init__()

        self.snake_length = 4
        self.width = level_width
        self.height = level_height
        self.engine = engine

    def astar(self, start, goal, reversePath=False):
        path = super().astar(start, goal, reversePath)

        # Casts to deque from list_reversegenerator
        return deque(path)

    def neighbors(self, current):
        neighbors = self.get_reach(current)

        # Remove groups that do not contain the snake (unreachable)
        #  tuple instead of list because it needs to be hashable for the astar library
        neighbor_groups: list[list[tuple[int, int]]] = get_connected_blocks(neighbors)
        neighbors = list(filter(lambda group: (current[0], current[1]) in group, neighbor_groups))

        # If there is a group of reachable blocks that the snake is in
        if neighbors:
            return neighbors[0]
        else:
            return []

    def heuristic_cost_estimate(self, current, goal) -> float:
        return self.distance_between(current, goal)

    def distance_between(self, a, b) -> float:
        # Euclidean distance (I don't care if this is slow, only happens a couple of times per level)
        return (a[0] - b[0])**2 + (a[1] - b[1])**2

    def is_goal_reached(self, current, goal) -> bool:
        return current == goal

    # Update when snake eats food
    def update_lenght(self, snake_lenght):
        self.snake_length = snake_lenght

    def get_reach(self, current: tuple[int, int]) -> list[tuple[int, int]]:
        return get_reach(current, self.engine, self.snake_length, self.width, self.height)
