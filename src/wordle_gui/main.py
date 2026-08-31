import sys

from PySide6.QtWidgets import QApplication

from wordle_gui import constants as const

# this import is required for the .qrc :/ virtual filepaths to work
from wordle_gui.assets import resources_rc  # noqa: F401
from wordle_gui.logic import app_setup, nyt
from wordle_gui.models.wordee_game_creation import WordeeGameFactory
from wordle_gui.presenters.game_presenter import GamePresenter
from wordle_gui.state import WordeeState
from wordle_gui.views.main_window import MainWindow


def main() -> None:
    app_setup.setup_logger(const.LOG_FILE_PATH)

    possible_solutions, valid_guesses = app_setup.load_words_data(const.CACHE_DIR_PATH)

    app = QApplication(sys.argv)

    window = MainWindow()

    # i dont need to assign it to anything since all the connecting stuff is in __init__()
    presenter = GamePresenter(  # noqa: F841
        window,
        WordeeGameFactory(
            possible_solutions,
            valid_guesses | possible_solutions,
            nyt.fetch_wordle_solution(const.USER_AGENT),
        ),
        WordeeState(),
    )

    app_setup.load_application_font(":/fonts/RobotoMono.ttf")
    app.setStyleSheet(app_setup.get_stylesheet_contents(":/style.qss"))
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
