from PySide6.QtWidgets import QApplication
import pytest

from wordle_gui import app_setup
from wordle_gui import constants as const
from wordle_gui.assets import resources_rc


@pytest.fixture(scope="session", autouse=True)
def qapplication() -> QApplication:
    return QApplication()


def test_load_valid_application_font():
    app_setup.load_application_font(":/fonts/RobotoMono.ttf")


def test_load_nonexistant_application_font():
    with pytest.raises(FileNotFoundError):
        app_setup.load_application_font(":/fonts/NotARealFont.ttf")


def test_load_stylesheet():
    assert (
        app_setup.get_stylesheet_contents(":/style.qss")
        == (const.ASSETS_DIR_PATH / "style.qss").read_text()
    )


def test_load_nonexistant_stylesheet():
    with pytest.raises(FileNotFoundError):
        app_setup.get_stylesheet_contents(":/stylesheets/not-a-real-stylesheet.qss")
