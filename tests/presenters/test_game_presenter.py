from typing import TYPE_CHECKING

import pytest

from wordee.constants import WordeeCellColor
from wordee.models.wordee_game_creation import WordeeGameFactory
from wordee.presenters.game_presenter import GamePresenter
from wordee.state import DailyGameState
from wordee.views.main_window import MainWindow

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
    from pytestqt.qtbot import QtBot

DAILY_GRID: list[list[tuple[str, WordeeCellColor | None]]] = [
    [
        ("S", "green"),
        ("H", "gray"),
        ("E", "yellow"),
        ("E", "gray"),
        ("P", "gray"),
    ],
    [("", "gray")] * 5,
    [("", "gray")] * 5,
    [("", "gray")] * 5,
    [("", "gray")] * 5,
    [("", "gray")] * 5,
]

LETTER_STATUSES: dict[str, WordeeCellColor | None] = {
    "s": "green",
    "h": "gray",
    "e": "yellow",
    "p": "gray",
}


@pytest.fixture
def game_presenter(mocker: MockerFixture, qtbot: QtBot) -> GamePresenter:
    state = DailyGameState()

    return GamePresenter(
        MainWindow(),
        WordeeGameFactory({"sheep"}, {"stray", "sheep"}, "sheep"),
        state,
    )


def test_guess_row_number(game_presenter: GamePresenter) -> None:
    assert game_presenter.guess_row_number == 1
    game_presenter.model._guesses_left = 5
    assert game_presenter.guess_row_number == 2
    game_presenter.model._guesses_left = 4
    assert game_presenter.guess_row_number == 3
    game_presenter.model._guesses_left = 3
    assert game_presenter.guess_row_number == 4
    game_presenter.model._guesses_left = 2
    assert game_presenter.guess_row_number == 5
    game_presenter.model._guesses_left = 1
    assert game_presenter.guess_row_number == 6


def test_sync_daily_state(game_presenter: GamePresenter) -> None:
    game_presenter.current_game_mode = "daily"

    game_presenter.view.wordee_grid.update_wordee_grid(DAILY_GRID)
    game_presenter.view.right_game_area.letter_statuses.update_letter_statuses(
        LETTER_STATUSES
    )

    game_presenter.model._guesses_left = 3
    game_presenter.view.right_game_area.game_stats.set_time_elapsed(20)

    game_presenter.sync_daily_state()

    assert game_presenter.state.daily_board == DAILY_GRID
    assert game_presenter.state.daily_letter_statuses["s"] == "green"
    assert game_presenter.state.daily_letter_statuses["h"] == "gray"
    assert game_presenter.state.daily_letter_statuses["e"] == "yellow"
    assert game_presenter.state.daily_letter_statuses["p"] == "gray"
    assert game_presenter.state.daily_guesses_left == 3
    assert game_presenter.state.daily_time_elapsed == 20


def test_restore_daily_view(game_presenter: GamePresenter) -> None:
    game_presenter.state.daily_board = DAILY_GRID
    game_presenter.state.daily_letter_statuses = LETTER_STATUSES
    game_presenter.state.daily_guesses_left = 3
    game_presenter.state.daily_time_elapsed = 20
    game_presenter.state.daily_game_status = "playing"
    game_presenter.state.daily_puzzle_number = 42

    game_presenter.restore_daily_view()

    assert game_presenter.view.wordee_grid.get_wordee_grid() == DAILY_GRID

    letter_statuses = (
        game_presenter.view.right_game_area.letter_statuses.get_letter_statuses()
    )
    assert letter_statuses["s"] == "green"
    assert letter_statuses["h"] == "gray"
    assert letter_statuses["e"] == "yellow"
    assert letter_statuses["p"] == "gray"

    assert game_presenter.view.right_game_area.game_stats.seconds_elapsed == 20


def test_restore_daily_view_with_default_board_and_letter_statuses_values(
    game_presenter: GamePresenter,
) -> None:
    original_grid = game_presenter.view.wordee_grid.get_wordee_grid()
    original_letter_statuses = (
        game_presenter.view.right_game_area.letter_statuses.get_letter_statuses()
    )
    game_presenter.state.daily_guesses_left = 3
    game_presenter.state.daily_time_elapsed = 20
    game_presenter.state.daily_puzzle_number = 42

    game_presenter.restore_daily_view()

    assert game_presenter.view.wordee_grid.get_wordee_grid() == original_grid
    assert (
        game_presenter.view.right_game_area.letter_statuses.get_letter_statuses()
        == original_letter_statuses
    )

    assert game_presenter.view.right_game_area.game_stats.seconds_elapsed == 20
    assert "42" in game_presenter.view.right_game_area.puzzle_number_label.text()


def test_handle_enter_key_does_nothing_if_game_not_playing(
    game_presenter: GamePresenter,
) -> None:
    game_presenter.model._game_state = "win"

    # if it didnt get stopped by the if check,
    # it would raise a ValueError since the guess is empty
    game_presenter.handle_enter_key()


def test_handle_switch_modes_between_daily_and_unlimited(
    game_presenter: GamePresenter,
) -> None:
    game_presenter.state.daily_game_status = "win"
    game_presenter.model._game_state = "win"
    game_presenter.current_game_mode = "daily"

    game_presenter.handle_switch_modes()

    # mypy is fucking stupid
    assert game_presenter.current_game_mode == "unlimited"  # type: ignore[comparison-overlap]
    assert "UNLIMITED" in game_presenter.view.right_game_area.puzzle_number_label.text()

    # since the user hasn't done shit in the 'game' yet
    # it should be able to switch
    game_presenter.handle_switch_modes()

    assert game_presenter.current_game_mode == "daily"
    assert game_presenter.view.right_game_area.game_stats.seconds_elapsed == 0


def test_handle_switch_modes_calls_block_dialog_if_unavailable(
    game_presenter: GamePresenter, mocker: MockerFixture
) -> None:
    game_presenter.current_game_mode = "daily"

    block_dialog = mocker.patch(
        "wordee.presenters.game_presenter.BlockSwitchModeDialog"
    )

    game_presenter.handle_switch_modes()
    block_dialog.assert_called_once()

    assert game_presenter.current_game_mode == "daily"


def test_handle_alphabet_key_updates_daily_state(
    game_presenter: GamePresenter,
) -> None:
    game_presenter.current_game_mode = "daily"

    game_presenter.handle_alphabet_key("a")

    assert game_presenter.view.wordee_grid.get_wordee_row_text(1) == "A"
    assert game_presenter.state.daily_board == (
        game_presenter.view.wordee_grid.get_wordee_grid()
    )


def test_handle_backspace_key_updates_daily_state(
    game_presenter: GamePresenter,
) -> None:
    game_presenter.current_game_mode = "daily"

    game_presenter.handle_alphabet_key("a")
    game_presenter.handle_alphabet_key("b")
    game_presenter.handle_backspace_key()

    assert game_presenter.view.wordee_grid.get_wordee_row_text(1) == "A"
    assert game_presenter.state.daily_board == (
        game_presenter.view.wordee_grid.get_wordee_grid()
    )


def test_handle_enter_key_submits_guess_and_updates_view(
    game_presenter: GamePresenter,
) -> None:
    game_presenter.current_game_mode = "daily"

    for letter in "stray":
        game_presenter.handle_alphabet_key(letter)

    game_presenter.handle_enter_key()

    assert game_presenter.model.guesses_left == 5
    assert game_presenter.view.wordee_grid.get_wordee_row_text(1) == "STRAY"
    assert game_presenter.state.daily_guesses_left == 5
    assert game_presenter.state.daily_game_status == game_presenter.model.game_state


def test_handle_enter_key_shows_game_over_dialog_on_loss(
    game_presenter: GamePresenter,
    mocker: MockerFixture,
) -> None:
    game_presenter.current_game_mode = "daily"

    game_over_dialog = mocker.patch("wordee.presenters.game_presenter.GameOverDialog")

    assert game_presenter.model._target_word == "sheep"
    assert game_presenter.guess_row_number == 1
    for letter in "sheep":
        game_presenter.handle_alphabet_key(letter)
    assert game_presenter.view.wordee_grid.get_wordee_row_text(1) == "SHEEP"

    game_presenter.handle_enter_key()

    assert game_presenter.model.game_state == "win"
    game_over_dialog.assert_called_once()
    game_over_dialog.return_value.exec.assert_called_once()


def test_handle_give_up_ends_game(
    game_presenter: GamePresenter,
    mocker: MockerFixture,
) -> None:
    game_presenter.current_game_mode = "daily"

    game_over_dialog = mocker.patch("wordee.presenters.game_presenter.GameOverDialog")

    game_presenter.view.right_game_area.enable_give_up_button()
    game_presenter.handle_give_up()

    assert game_presenter.model.game_state == "loss"
    assert game_presenter.state.daily_game_status == "loss"
    game_over_dialog.assert_called_once()


def test_handle_give_up_does_nothing_when_button_disabled(
    game_presenter: GamePresenter,
    mocker: MockerFixture,
) -> None:
    game_over_dialog = mocker.patch("wordee.presenters.game_presenter.GameOverDialog")

    game_presenter.handle_give_up()

    assert game_presenter.model.game_state == "playing"
    game_over_dialog.assert_not_called()
