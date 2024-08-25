import os
import sys

from game_engine.entities import Snake, Wall, Food, Finish
from game_engine import Level


#  Returns the level info and the starting camera offset
def load_level(level_number) -> tuple[Level, int, int]:
    level_width, level_height = 0, 0
    offsetx, offsety = 0, 0
    snake = None
    static_entities, dynamic_entities = [], []

    # Path to resources relative to main.py, I dont know if there is a better way to do it but it seems wrong
    with open(f"{os.path.dirname(sys.modules["__main__"].__file__)}/resources/{level_number}.hadik", "r") as f:
        line = f.readline()
        while line:

            if "DIMENSIONS" in line:
                level_width, level_height = ([int(x) for x in f.readline().strip().split(";")])

            if "CAMERA_OFFSET" in line:
                offsetx, offsety = ([int(x) for x in f.readline().strip().split(";")])

            elif "SNAKE" in line:
                x, y = ([int(x) for x in f.readline().strip().split(";")])
                snake = Snake([
                    (x, y),
                    (x, y + 1),
                    (x + 1, y + 1),
                    (x + 1, y)
                ])

            elif "WALL" in line:
                line = f.readline()

                while ";" in line:
                    x, y, width, height = ([int(x) for x in line.strip().split(";")])
                    static_entities.append(Wall(x, y, width, height))

                    line = f.readline()
                continue

            elif "FOOD" in line:
                line = f.readline()

                while ";" in line:
                    x, y = ([int(x) for x in line.strip().split(";")])
                    # Ugly init because Foox expects a list of blocks but its only one block
                    static_entities.append(Food([(x, y)]))

                    line = f.readline()
                continue

            elif "FINISH" in line:
                x, y = ([int(x) for x in f.readline().strip().split(";")])
                static_entities.append(Finish(x, y))

            line = f.readline()

    return Level(level_width, level_height, snake, static_entities, dynamic_entities), offsetx, offsety
