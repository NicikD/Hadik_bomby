import os
import sys


class PlayerData:
    def __init__(self):
        # Levels that the player has finished (indexed from 1)
        self.levels = [None] + [False for _ in range(16)]

        self.fullscreen = False
        self.autoplay = False


def load_player_data():
    path = f"{os.path.dirname(sys.modules["__main__"].__file__)}/resources/player_data.save"

    # A save does not exist, use default
    if not os.path.exists(path):
        return PlayerData()

    with open(path, "r") as f:
        data = PlayerData()

        line = f.readline()
        while line:

            if "FULLSCREEN" in line:
                data.fullscreen = True if f.readline().strip() == "True" else False

            elif "AUTOPLAY" in line:
                data.autoplay = True if f.readline().strip() == "True" else False

            elif "LEVELS" in line:
                for level in f.readline().strip().split(";"):
                    if level:
                        data.levels[int(level)] = True

            line = f.readline()

    return data


def save_player_data(data):
    levels = [str(i) for i in range(17) if data.levels[i] and i != 0]

    with open(f"{os.path.dirname(sys.modules["__main__"].__file__)}/resources/player_data.save", "w") as f:
        f.write("FULLSCREEN"                                + "\n")
        f.write(("True" if data.fullscreen else "False")    + "\n\n")
        f.write("AUTOPLAY"                                  + "\n")
        f.write(("True" if data.autoplay else "False")      + "\n\n")
        f.write("LEVELS"                                    + "\n")
        f.write(";".join([str(level) for level in levels])  + "\n\n")
