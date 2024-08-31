from os import path
import sys

from game_engine.entities import StaticEntity, DynamicEntity, Snake, Wall, Food, Finish
from game_engine import Level


#  Returns the level info and the starting camera offset
def load_level(level_number) -> tuple[Level, int, int]:
    level_width, level_height = 0, 0
    offsetx, offsety = 0, 0
    snake = None
    static_entities, dynamic_entities = [], []

    # Path to resources relative to main.py, I don't know if there is a better way to do it, but it seems wrong
    level_path = f"{path.dirname(sys.modules['__main__'].__file__)}/resources/{level_number}.hadik"

    # TODO implement all levels
    if not path.exists(level_path):
        raise NotImplementedError(f"Level {level_number} not implemented")

    with open(level_path, "r") as f:
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
                    static_entities.append(Food(x, y))

                    line = f.readline()
                continue

            elif "FINISH" in line:
                x, y = ([int(x) for x in f.readline().strip().split(";")])
                static_entities.append(Finish(x, y))

            line = f.readline()

    assert all(isinstance(entity, StaticEntity) for entity in static_entities)
    assert all(isinstance(entity, DynamicEntity) for entity in dynamic_entities)
    return Level(level_width, level_height, snake, static_entities, dynamic_entities), offsetx, offsety
