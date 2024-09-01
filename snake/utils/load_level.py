from os import path

import utils
import game_engine


#  Returns the level info and the starting camera offset
def load_level(level_number) -> tuple[game_engine.Level, int, int]:
    level_width, level_height = 0, 0
    offsetx, offsety = 0, 0
    snake = None
    entities = []

    level_path = f"{utils.get_resources_path()}/{level_number}.hadik"

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
                snake = game_engine.entities.Snake([
                    (x, y),
                    (x, y + 1),
                    (x + 1, y + 1),
                    (x + 1, y)
                ])

            elif "WALL" in line:
                line = f.readline()

                while ";" in line:
                    x, y, width, height = ([int(x) for x in line.strip().split(";")])
                    entities.append(game_engine.entities.Wall(x, y, width, height))

                    line = f.readline()
                continue

            elif "FOOD" in line:
                line = f.readline()

                while ";" in line:
                    x, y = ([int(x) for x in line.strip().split(";")])
                    # Ugly init because Foox expects a list of blocks but its only one block
                    entities.append(game_engine.entities.Food(x, y))

                    line = f.readline()
                continue

            elif "FINISH" in line:
                x, y = ([int(x) for x in f.readline().strip().split(";")])
                entities.append(game_engine.entities.Finish(x, y))

            line = f.readline()

    return game_engine.Level(level_width, level_height, snake, entities), offsetx, offsety
