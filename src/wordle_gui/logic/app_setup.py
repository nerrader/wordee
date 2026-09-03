import sys
from pathlib import Path

from httpx import Client as httpx_client
from loguru import logger
from PySide6.QtCore import QFile, QIODevice, QTextStream
from PySide6.QtGui import QFontDatabase

from wordle_gui.logic import cache


def setup_logger(logging_path: Path, verbose_mode: bool = False) -> None:
    logger.remove()
    logger.add(sink=logging_path, diagnose=False, retention=0, rotation="00:00")
    if verbose_mode:
        logger.add(sink=sys.stderr, level="DEBUG", diagnose=False)


def load_words_data(cache_dirpath: Path) -> tuple[set[str], set[str]]:
    """Loads and syncs the possible_solutions and valid_guesses cache.

    Args:
        cache_dirpath: The path to the cache/ directory.

    Returns:
        tuple[set[str], set[str]]: The possible_solutions and valid_guesses in a tuple.
    """
    cache_dirpath.mkdir(parents=True, exist_ok=True)

    possible_solutions: set[str] = cache.read_cache("possible_solutions", cache_dirpath)
    valid_guesses: set[str] = cache.read_cache("valid_guesses", cache_dirpath)

    return (possible_solutions, valid_guesses)


def sync_caches(cache_dirpath: Path, user_agent: str) -> None:
    cache_dirpath.mkdir(parents=True, exist_ok=True)

    with httpx_client(headers={"User-Agent": user_agent}) as client:
        cache.sync_cache("possible_solutions", cache_dirpath, client)
        cache.sync_cache("valid_guesses", cache_dirpath, client)


def load_application_font(font_path: str) -> None:
    """Loads a font for the application from font_path.

    Args:
        font_path (str): The virtual path to the font, found in assets/resources.qrc

    Raises:
        FileNotFoundError: Raised if the font was not loaded.
    """
    font_id = QFontDatabase.addApplicationFont(font_path)

    if font_id == -1:
        logger.error(f"Failed to load [{font_path}], font ID: {font_id}")
        raise FileNotFoundError(f"{font_path} failed to load with a font ID of -1.")

    logger.debug(f"Loaded [{font_path}] with an ID of {font_id}")


def get_stylesheet_contents(stylesheet_path: str) -> str:
    """Returns the full stylesheet contents in the stylesheet path.

    Args:
        stylesheet_path (str): The virtual path to the stylesheet made in assets/resources.qrc

    Raises:
        FileNotFoundError: Raised if the file was not found in the virtual path.
    """
    # for some reason qfile doesnt support the with statement in python so
    file = QFile(stylesheet_path)
    if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        stream = QTextStream(file)
        stylesheet: str = stream.readAll()
        file.close()
        logger.debug(f"Successfully loaded stylesheet: {stylesheet_path}")
        return stylesheet
    else:
        logger.error(f"Stylesheet path: [{stylesheet_path}] could not be loaded.")
        raise FileNotFoundError(
            "ERROR: Could not read file for :/style.qss. Closing the application..."
        )
