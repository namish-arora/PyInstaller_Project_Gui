# pyinstaller_gui_packager/main.py

import sys
import os

# Add the src folder to sys.path so relative imports inside src modules work
SRC_DIR = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, SRC_DIR)

# Now import the GUI launcher from src/gui/main_window.py
from src.gui.main_window import launch_gui

if __name__ == "__main__":
    launch_gui()
