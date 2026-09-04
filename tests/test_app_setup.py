from pathlib import Path
from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QApplication

from wordee import app_setup

# this import is required for the .qrc :/ virtual filepaths to work
from wordee.assets import resources_rc  # noqa: F401


def test_load_words_data(tmp_path: Path) -> None:
    possible_solutions = {"arise", "crane"}
    valid_guesses = {"arise", "crane", "apple"}

    with patch("wordee.words.cache.read_cache") as read_cache:
        read_cache.side_effect = [possible_solutions, valid_guesses]

        result = app_setup.load_words_data(tmp_path)

    assert result == (possible_solutions, valid_guesses)

    assert read_cache.call_count == 2
    read_cache.assert_any_call("possible_solutions", tmp_path)
    read_cache.assert_any_call("valid_guesses", tmp_path)


@pytest.fixture(scope="session", autouse=True)
def qapplication() -> QApplication:
    return QApplication()


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
