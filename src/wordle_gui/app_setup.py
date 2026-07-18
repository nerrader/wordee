from loguru import logger

from PySide6.QtCore import QFile, QIODevice, QTextStream
from PySide6.QtGui import QFontDatabase


def load_application_font(font_path: str) -> None:
    """Loads a font for the application from font_path.

    Args:
        font_path (str): The virtual path to the font, found in assets/resources.qrc

    Raises:
        FileNotFoundError: Raised if the font was not loaded.
    """
    font_id = QFontDatabase.addApplicationFont(font_path)

    if font_id == -1:
        logger.error(f"Failed to load [{font_path}], font ID: {font_id}")
        raise FileNotFoundError(f"{font_path} failed to load with a font ID of -1.")

    logger.debug(f"Loaded [{font_path}] with an ID of {font_id}")


def get_stylesheet_contents(stylesheet_path: str) -> str:
    """Returns the full stylesheet contents in the stylesheet path.

    Args:
        stylesheet_path (str): The virtual path to the stylesheet made in assets/resources.qrc

    Raises:
        FileNotFoundError: Raised if the file was not found in the virtual path.
    """
    # for some reason qfile doesnt support the with statement in python so
    file = QFile(stylesheet_path)
    if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        stream = QTextStream(file)
        stylesheet: str = stream.readAll()
        file.close()
        logger.debug(f"Successfully loaded stylesheet: {stylesheet_path}")
        return stylesheet
    else:
        logger.error(f"Stylesheet path: [{stylesheet_path}] could not be loaded.")
        raise FileNotFoundError(
            "ERROR: Could not read file for :/style.qss. Closing the application..."
        )
