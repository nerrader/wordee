from PySide6.QtWidgets import QApplication
import pytest

from wordle_gui import app_setup

# this import is required for the .qrc :/ virtual filepaths to work
from wordle_gui.assets import resources_rc  # noqa: F401


@pytest.fixture(scope="session", autouse=True)
def qapplication() -> QApplication:
    return QApplication()


def test_load_valid_application_font():
    app_setup.load_application_font(":/fonts/RobotoMono.ttf")


def test_load_nonexistant_application_font():
    with pytest.raises(FileNotFoundError):
        app_setup.load_application_font(":/fonts/NotARealFont.ttf")


def test_load_stylesheet():
    stylesheet_contents = app_setup.get_stylesheet_contents(":/style.qss")

    assert stylesheet_contents is not None
    assert "background-color" in stylesheet_contents
    assert '[class="grid_label"]' in stylesheet_contents


def test_load_nonexistant_stylesheet():
    with pytest.raises(FileNotFoundError):
        app_setup.get_stylesheet_contents(":/stylesheets/not-a-real-stylesheet.qss")
