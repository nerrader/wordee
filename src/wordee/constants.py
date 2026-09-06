from pathlib import Path
from typing import Literal

from platformdirs import PlatformDirs

_dirs = PlatformDirs("wordee", appauthor="nerrader")
MAIN_DATA_PATH: Path = _dirs.user_data_path
STATE_PATH: Path = MAIN_DATA_PATH / "state.json"
LOG_FILE_PATH: Path = MAIN_DATA_PATH / "app.log"
CACHE_DIR_PATH: Path = MAIN_DATA_PATH / "cache"
SOLUTIONS_CACHE_PATH = CACHE_DIR_PATH / "possible_solutions.txt"

USER_AGENT = "WordleGUI (https://github.com/nerrader/wordee)"

GameMode = Literal["daily", "unlimited"]
WordeeCellColor = Literal["gray", "yellow", "green"]
GameStatus = Literal["win", "loss", "playing"]
