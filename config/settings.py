import os
from pathlib import Path
from BetterFileExplorer.core import load

APP_NAME = "BetterFileExplorer"
VERSION = "1.1"

ROOT_DIR = Path(__file__).parent.parent
DATA_PATH = os.path.join(ROOT_DIR, "config/data")

SETTINGS_PATH = os.path.join(DATA_PATH, "settings.json")
CURRENT_PROFILE_PATH = os.path.join(DATA_PATH, "current_hierarchy_profile.json")
RECENT_FILE_PATH = os.path.join(DATA_PATH, "recent_files.json")

CONTEXT_MENU_QSS = "QPushButton{background:#666;border-radius:3px;min-height:20px;padding:0 10px}QPushButton:hover{background:#5285a6}QPushButton:pressed{background:#28658d}"


# TODO Maybe its better those 2 functions end up in load module
def get_current_hierarchy_profile():
    return load.open_json(SETTINGS_PATH)["current_hierarchy_profile"]
