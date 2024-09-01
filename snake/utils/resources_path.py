import os
import sys


def get_resources_path():
    # Path to resources relative to main.py, I don't know if there is a better way to do it, but it seems wrong
    return f"{os.path.dirname(sys.modules['__main__'].__file__)}/resources"
