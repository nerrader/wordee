from typing import TYPE_CHECKING
from PySide6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from wordle_gui.views.topbar import Topbar
from wordle_gui.views.left_game_area import LeftGameArea
from wordle_gui.views.right_game_area import RightGameArea

if TYPE_CHECKING:
    from PySide6.QtGui import QKeyEvent


class MainWindow(QMainWindow):
    alphabet_key_signal = Signal(str)
    backspace_key_signal = Signal()
    enter_key_signal = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setup_components()
        self.setup_layouts()

    def setup_components(self) -> None:
        self.main_container = QFrame()
        self.main_container.setObjectName("main_container")
        self.setCentralWidget(self.main_container)

        self.topbar = Topbar()
        self.left_game_area = LeftGameArea()
        self.right_game_area = RightGameArea()

        # make the buttons click signal connect with this main alphabet key signal
        # so theres no two signals that do the exact same thing
        letter_statuses = self.right_game_area.letter_statuses
        for button in letter_statuses.keyboard_map.values():
            button.key_pressed.connect(
                lambda letter: self.alphabet_key_signal.emit(letter)
            )
        letter_statuses.backspace_signal.connect(self.backspace_key_signal)
        letter_statuses.enter_signal.connect(self.enter_key_signal)

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

    def keyPressEvent(self, event: QKeyEvent) -> None:
        match event.key():
            case Qt.Key.Key_Backspace:
                self.backspace_key_signal.emit()
            case Qt.Key.Key_Return | Qt.Key.Key_Enter:
                self.enter_key_signal.emit()
            case _:
                if event.text().isalpha():
                    self.alphabet_key_signal.emit(event.text().lower())
                else:
                    return
