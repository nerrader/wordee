from pathlib import Path

from PySide6.QtCore import QFile, QIODevice, QTextStream

STYLESHEET = Path("src/wordee/assets/style.qss")


def test_resources_stylesheet_is_up_to_date(tmp_path: Path) -> None:
    current_stylesheet = STYLESHEET.read_text()

    file = QFile(":/style.qss")
    assert file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)

    stream = QTextStream(file)
    resources_stylesheet: str = stream.readAll()
    file.close()

    assert current_stylesheet == resources_stylesheet
