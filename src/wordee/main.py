import sys

from httpx import ConnectError
from PySide6.QtWidgets import QApplication

from wordee import app_setup, state
from wordee import constants as const

# this import is required for the .qrc :/ virtual filepaths to work
from wordee.assets import resources_rc  # noqa: F401
from wordee.logic import nyt
from wordee.models.wordee_game_creation import WordeeGameFactory
from wordee.presenters.game_presenter import GamePresenter
from wordee.views.dialogs import NoInternetDialog
from wordee.views.main_window import MainWindow


def main() -> None:
    app_setup.setup_logger(const.LOG_FILE_PATH, True)

    wordee_state = state.load_or_create_daily_state(const.STATE_PATH)

    possible_solutions, valid_guesses = app_setup.load_words_data(const.CACHE_DIR_PATH)

    app = QApplication(sys.argv)
    app_setup.load_application_font(":/fonts/RobotoMono.ttf")
    app.setStyleSheet(app_setup.get_stylesheet_contents(":/style.qss"))

    try:
        target_word, puzzle_number = nyt.fetch_wordle_solution(const.USER_AGENT)
    except ConnectError:
        NoInternetDialog().exec()
        return

    window = MainWindow()
    wordee_state.daily_puzzle_number = puzzle_number

    # i dont need to assign it to anything since all the connecting stuff is in __init__()
    presenter = GamePresenter(  # noqa: F841
        window,
        WordeeGameFactory(
            possible_solutions, valid_guesses | possible_solutions, target_word
        ),
        wordee_state,
    )

    app.aboutToQuit.connect(
        lambda: save_state(
            wordee_state, window.right_game_area.game_stats.seconds_elapsed
        )
    )

    window.showMaximized()
    sys.exit(app.exec())


def save_state(wordee_state: state.DailyGameState, seconds_elapsed: int) -> None:
    # if the daily game is not done yet
    if wordee_state.daily_time_elapsed == 0:
        wordee_state.daily_time_elapsed = seconds_elapsed

    state.save_daily_state(const.STATE_PATH, wordee_state)


if __name__ == "__main__":
    main()
