import pytest
from PySide6.QtWidgets import QApplication

from wordee import app_setup

# this import is required for the .qrc :/ virtual filepaths to work
from wordee.assets import resources_rc  # noqa: F401


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
