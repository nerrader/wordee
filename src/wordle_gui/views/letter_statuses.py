from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from wordle_gui.game_signals import game_signals


class WordeeStatusKey(QPushButton):
    def __init__(self, letter: str):
        super().__init__(letter)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setContentsMargins(10, 10, 10, 10)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # this signal will be passed into main_window.py, to be converted into the main alphabet_key_signal
        self.clicked.connect(lambda: game_signals.alphabet_key_pressed.emit(letter))


class LetterStatuses(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setup_components()
        self.setup_layouts()

    def setup_components(self) -> None:
        self.letter_status_label_header = QLabel("LETTER STATUSES")
        self.letter_status_label_header.setObjectName("letter_statuses_header_label")

        self.backspace_key = QPushButton("Backspace")
        self.backspace_key.setObjectName("backspace_key")
        self.backspace_key.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.backspace_key.clicked.connect(game_signals.backspace_key_pressed.emit)
        self.backspace_key.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.enter_key = QPushButton("Enter")
        self.enter_key.setObjectName("enter_key")
        self.enter_key.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.enter_key.clicked.connect(game_signals.enter_key_pressed.emit)
        self.enter_key.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.first_letter_row = [
            WordeeStatusKey(letter)
            for letter in ("Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P")
        ]
        self.second_letter_row = [
            WordeeStatusKey(letter)
            for letter in ("A", "S", "D", "F", "G", "H", "J", "K", "L")
        ]
        self.third_letter_row = [
            WordeeStatusKey(letter) for letter in ("Z", "X", "C", "V", "B", "N", "M")
        ]

        self.keyboard_map: dict[str, WordeeStatusKey] = {}

        for button in (
            self.first_letter_row + self.second_letter_row + self.third_letter_row
        ):
            button_letter = button.text().lower()
            self.keyboard_map[button_letter] = button

    def setup_layouts(self) -> None:
        label_header_layout = QHBoxLayout()

        label_header_layout.addWidget(self.letter_status_label_header)
        label_header_layout.addWidget(self.backspace_key)
        label_header_layout.addWidget(self.enter_key)

        label_header_layout.setSpacing(10)

        letter_statuses_layout = QVBoxLayout()

        first_row_layout = QHBoxLayout()
        for label in self.first_letter_row:
            first_row_layout.addWidget(label)
        first_row_layout.setSpacing(7)

        second_row_layout = QHBoxLayout()
        for label in self.second_letter_row:
            second_row_layout.addWidget(label)
        second_row_layout.setSpacing(7)

        third_row_layout = QHBoxLayout()
        for label in self.third_letter_row:
            third_row_layout.addWidget(label)
        third_row_layout.setSpacing(7)

        letter_statuses_layout.addLayout(label_header_layout)
        letter_statuses_layout.addLayout(first_row_layout)
        letter_statuses_layout.addLayout(second_row_layout)
        letter_statuses_layout.addLayout(third_row_layout)

        letter_statuses_layout.setSpacing(7)

        letter_statuses_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(letter_statuses_layout)
