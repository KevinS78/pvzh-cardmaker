# PvZH Card Image Maker

A Python script for generating images of custom cards, in a format similar to as they would appear in-game. Use the "preview image" button to update the image preview with any changes, and use the "save image" button to save the card image as a file.

You need to manually choose where to split the card and flavor text into multiple lines, the program can't do that automatically yet.

Currently does not support formatting (e.g. bold text, colored text, etc.) or icons (e.g. keyword symbols, plus/minus attack/hp symbols, etc.) in the card text.

This script requires a reasonably up to date Python environment to function properly. I'm not good enough at Python to know exactly what versions are required, but following a reasonably recent tutorial for installing Python and PIL should do the job.

I have only tested the program on macOS so there is a small chance that it doesn't work as expected on other systems.

## Requirements

- Python and tkinter (which should be included with Python)
- PIL library, which can be installed in Command Line/Terminal with ```pip install pillow``` (assuming pip is installed).

## Running the Program

Run the app using Command Line/Terminal with ```python image_generator.py``` while in the folder containing ```generator.py```. Make sure the location of image assets is not changed relative to the Python script.