from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from wordee import app_setup

# this import is required for the .qrc :/ virtual filepaths to work
from wordee.assets import resources_rc  # noqa: F401

if TYPE_CHECKING:
    from PySide6.QtWidgets import QApplication


def test_load_words_data(tmp_path: Path, qapp: QApplication) -> None:
    possible_solutions = {"arise", "crane"}
    valid_guesses = {"arise", "crane", "apple"}

    with patch("wordee.logic.word_files.read_word_file") as read_word_file:
        read_word_file.side_effect = [possible_solutions, valid_guesses]

        result = app_setup.load_words_data()

    assert result == (possible_solutions, valid_guesses)

    assert read_word_file.call_count == 2
    read_word_file.assert_any_call("possible_solutions")
    read_word_file.assert_any_call("valid_guesses")


def test_load_valid_application_font() -> None:
    app_setup.load_application_font(":/fonts/RobotoMono.ttf")


def test_load_nonexistant_application_font() -> None:
    with pytest.raises(FileNotFoundError):
        app_setup.load_application_font(":/fonts/NotARealFont.ttf")


def test_load_stylesheet() -> None:
    stylesheet_contents = app_setup.get_stylesheet_contents(":/style.qss")

    assert stylesheet_contents is not None
    assert "background-color" in stylesheet_contents
    assert "QPushButton" in stylesheet_contents
    assert "LetterStatuses" in stylesheet_contents


def test_load_nonexistant_stylesheet() -> None:
    with pytest.raises(FileNotFoundError):
        app_setup.get_stylesheet_contents(":/stylesheets/not-a-real-stylesheet.qss")
