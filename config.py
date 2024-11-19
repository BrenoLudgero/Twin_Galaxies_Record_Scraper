import os
import sys

# Determines the current path for the script or executable
if getattr(sys, "frozen", False):
    current_directory = os.path.dirname(sys.executable)
elif __file__:
    current_directory = os.path.dirname(__file__)

FOLDER_NAME = "TG Records"
RECORDS_FOLDER_DIRECTORY = os.path.join(current_directory, FOLDER_NAME)

# Creates the records folder if not found
if not os.path.isdir(RECORDS_FOLDER_DIRECTORY):
    os.makedirs(RECORDS_FOLDER_DIRECTORY)
