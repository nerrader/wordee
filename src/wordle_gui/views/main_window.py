from collections.abc import Iterator
from contextlib import contextmanager
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from wordle_gui.game_signals import game_signals
from wordle_gui.views.left_game_area import LeftGameArea
from wordle_gui.views.right_game_area import RightGameArea
from wordle_gui.views.topbar import Topbar

if TYPE_CHECKING:
    from PySide6.QtGui import QKeyEvent


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("WORDEE")
        self.setWindowIcon(QIcon(":/icons/wordee-icon.svg"))
        self.setup_components()
        self.setup_layouts()

    def setup_components(self) -> None:
        self.main_container = QFrame()
        self.main_container.setObjectName("main_container")
        self.setCentralWidget(self.main_container)

        self.topbar = Topbar()
        self.left_game_area = LeftGameArea()
        self.right_game_area = RightGameArea()

    def setup_layouts(self) -> None:
        main_container_layout = QVBoxLayout()
        main_container_layout.setStretch(0, 1)
        main_container_layout.setStretch(1, 9)
        main_container_layout.addWidget(self.topbar)
        main_container_layout.setContentsMargins(0, 0, 0, 0)

        game_area_layout = QHBoxLayout()
        game_area_layout.addWidget(self.left_game_area)
        game_area_layout.addWidget(self.right_game_area)
        game_area_layout.setSpacing(20)

        main_container_layout.addLayout(game_area_layout)

        self.main_container.setLayout(main_container_layout)

    @contextmanager
    def dimmed(self) -> Iterator[None]:
        overlay = QWidget(self)
        overlay.setGeometry(self.rect())
        overlay.setStyleSheet("background-color: rgba(0, 0, 0, 80)")
        overlay.show()

        # i dont understand what this means but basically
        # the finally block is the __exit__ block
        try:
            yield
        finally:
            overlay.deleteLater()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        match event.key():
            case Qt.Key.Key_Backspace:
                game_signals.backspace_key_pressed.emit()
            case Qt.Key.Key_Return | Qt.Key.Key_Enter:
                game_signals.enter_key_pressed.emit()
            case _:
                if event.text().isalpha():
                    game_signals.alphabet_key_pressed.emit(event.text().lower())
                else:
                    return

    def reset_game_view(self) -> None:
        self.left_game_area.reset_status_label()
        self.left_game_area.reset_wordee_cells()

        self.right_game_area.game_stats.reset_time_elapsed()
        self.right_game_area.letter_statuses.reset_letter_statuses()
        self.right_game_area.set_give_up_button()
