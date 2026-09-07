from typing import TYPE_CHECKING

import pytest

from wordee.views.wordee_grid import WordeeGrid

if TYPE_CHECKING:
    from PySide6.QtWidgets import QApplication

    from wordee.constants import WordeeCellColor


@pytest.fixture
def wordee_grid(qapp: QApplication) -> WordeeGrid:
    return WordeeGrid()


def test_add_and_delete_letter_to_grid(wordee_grid: WordeeGrid) -> None:
    wordee_grid.add_letter_to_grid("A", 1)
    wordee_grid.add_letter_to_grid("B", 1)
    wordee_grid.add_letter_to_grid("C", 1)
    wordee_grid.add_letter_to_grid("D", 1)
    wordee_grid.add_letter_to_grid("E", 1)

    # invalid one right here
    wordee_grid.add_letter_to_grid("F", 1)

    assert wordee_grid.get_wordee_row_text(1) == "ABCDE"

    wordee_grid.delete_last_grid_letter(1)
    wordee_grid.delete_last_grid_letter(1)
    wordee_grid.delete_last_grid_letter(1)

    assert wordee_grid.get_wordee_row_text(1) == "AB"


# test made by AI cuz too fucking lazy
# why write repetitive tests when ai can do it for me
def test_wordee_grid_state_round_trip(wordee_grid: WordeeGrid) -> None:
    wordee_grid.add_letter_to_grid("A", 1)
    wordee_grid.add_letter_to_grid("B", 1)
    wordee_grid.add_letter_to_grid("C", 1)
    wordee_grid.add_letter_to_grid("D", 1)
    wordee_grid.add_letter_to_grid("E", 1)

    colors: list[WordeeCellColor] = [
        "green",
        "yellow",
        "gray",
        "green",
        "yellow",
    ]
    wordee_grid.update_wordee_row_cell_colors(1, colors)

    saved_board = wordee_grid.get_wordee_grid()

    wordee_grid.reset_wordee_cells()

    assert wordee_grid.get_wordee_grid() != saved_board

    wordee_grid.update_wordee_grid(saved_board)

    assert wordee_grid.get_wordee_grid() == saved_board
