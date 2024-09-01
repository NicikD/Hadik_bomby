import os
import sys

DEFAULT_FULLSCREEN = False
DEFAULT_AUTOPLAY = False

class PlayerData:
    def __init__(self):
        # Levels that the player has finished (indexed from 1)
        self.levels = [None] + [False for _ in range(16)]

        self.fullscreen = DEFAULT_FULLSCREEN
        self.autoplay = DEFAULT_AUTOPLAY

    def load(self):
        path = f"{os.path.dirname(sys.modules["__main__"].__file__)}/resources/player_data.save"

        # A save does not exist, use default
        if not os.path.exists(path):
            self.levels = [None] + [False for _ in range(16)]
            self.fullscreen = DEFAULT_FULLSCREEN
            self.autoplay = DEFAULT_AUTOPLAY

        with open(path, "r") as f:
            line = f.readline()
            while line:

                if "FULLSCREEN" in line:
                    self.fullscreen = True if f.readline().strip() == "True" else False

                elif "AUTOPLAY" in line:
                    self.autoplay = True if f.readline().strip() == "True" else False

                elif "LEVELS" in line:
                    for level in f.readline().strip().split(";"):
                        if level:
                            self.levels[int(level)] = True

                line = f.readline()

    def save(self):
        levels = [str(i) for i in range(17) if self.levels[i] and i != 0]

        with open(f"{os.path.dirname(sys.modules["__main__"].__file__)}/resources/player_data.save", "w") as f:
            f.write("FULLSCREEN" + "\n")
            f.write(("True" if self.fullscreen else "False") + "\n\n")
            f.write("AUTOPLAY" + "\n")
            f.write(("True" if self.autoplay else "False") + "\n\n")
            f.write("LEVELS" + "\n")
            f.write(";".join([str(level) for level in levels]) + "\n\n")
