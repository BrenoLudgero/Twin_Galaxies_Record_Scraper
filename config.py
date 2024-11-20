import os
import sys

FOLDER_NAME = "TG Records"

# Determines the current path for the script or executable
def get_current_directory():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(__file__)

def get_records_folder_path():
    return os.path.join(get_current_directory(), FOLDER_NAME)

def create_records_folder():
    records_folder = get_records_folder_path()
    if not os.path.isdir(records_folder):
        os.makedirs(records_folder)

INSTRUCTIONS = """HOW TO USE:

Insert the link to each page you want to extract the recors from in Links List. For example:

www.twingalaxies.com/game/tetris
www.twingalaxies.com/game/galaga/arcade

Alternatively, you may insert just the values that follow "game/":

tetris
galaga/arcade

Each link must be in a new line"""
