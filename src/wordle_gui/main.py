import sys

from httpx import Client as httpx_client
from loguru import logger
from PySide6.QtWidgets import QApplication

from wordle_gui import constants as const
from wordle_gui import cache
from wordle_gui import nyt

from wordle_gui.views.main_window import MainWindow
from wordle_gui.models.game_logic import WordeeGame
from wordle_gui.presenters.game_presenter import GamePresenter

# this import is required for the .qrc :/ virtual filepaths to work
from wordle_gui.assets import resources_rc  # type: ignore # noqa: F401
from wordle_gui import app_setup


def setup_logger() -> None:
    logger.remove()
    logger.add(sink=const.LOG_FILE_PATH, diagnose=False, retention=0, rotation="00:00")


def main() -> None:
    setup_logger()

    const.CACHE_DIR_PATH.mkdir(parents=True, exist_ok=True)

    with httpx_client(timeout=10.0, headers={"User-Agent": const.USER_AGENT}) as client:
        cache.sync_cache("possible_solutions", const.CACHE_DIR_PATH, client)
        cache.sync_cache("valid_guesses", const.CACHE_DIR_PATH, client)
        target_word = nyt.fetch_wordle_solution(client)

    possible_solutions: set[str] = cache.read_cache(
        "possible_solutions", const.CACHE_DIR_PATH
    )
    valid_guesses: set[str] = cache.read_cache("valid_guesses", const.CACHE_DIR_PATH)
    all_allowed_words = possible_solutions | valid_guesses

    app = QApplication(sys.argv)

    game_logic_model = WordeeGame(target_word, all_allowed_words)
    window = MainWindow()

    # i dont need to assign it to anything since all the connecting stuff is in __init__()
    presenter = GamePresenter(window, game_logic_model)  # noqa: F841

    app_setup.load_application_font(":/fonts/RobotoMono.ttf")
    app.setStyleSheet(app_setup.get_stylesheet_contents(":/style.qss"))
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
