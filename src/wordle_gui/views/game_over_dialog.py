from random import choice

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QCursor
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from wordle_gui.game_signals import game_signals


class GameOverDialog(QDialog):
    def __init__(self, won: bool, target_word: str):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        layout = QVBoxLayout()

        close_button = QPushButton("x")
        close_button.setObjectName("post_game_close_button")
        close_button.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close_button.clicked.connect(self.reject)

        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(close_button)

        result_label = QLabel(f"YOU {'WON!' if won else 'lost.'}")
        result_label.setObjectName("post_game_result_label")

        extra_win_labels = (
            "congratulations!",
            "you got good vocab",
            "you didn't google it up right",
            "we get it, you're good",
            "actual tryhard",
        )

        extra_loss_lables = (
            "better luck next time",
            "you should get better at english",
            "your english teacher would be disappointed",
            "theres only 26 letters in the alphabet",
            "that was tough",
            "try again next time",
            "well, that wasn't exactly your day",
        )

        extra_label = QLabel(
            choice(extra_win_labels) if won else choice(extra_loss_lables)
        )
        extra_label.setObjectName("post_game_extra_label")

        result_container = QFrame()
        result_container.setObjectName("post_game_result_container")
        result_container.setProperty("win", won)
        result_container.setContentsMargins(10, 10, 10, 10)

        result_container_layout = QVBoxLayout()
        result_container_layout.addWidget(
            result_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        result_container_layout.addWidget(
            extra_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        result_container.setLayout(result_container_layout)

        answer_label = QLabel(f"The word was <b>{target_word.upper()}</b>!")
        answer_label.setObjectName("post_game_answer_label")
        answer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.play_unlimited_button = QPushButton("Play Unlimited Mode")
        self.play_unlimited_button.setObjectName("post_game_play_unlimited_button")
        self.play_unlimited_button.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.play_unlimited_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.play_unlimited_button.clicked.connect(self._play_unlimited)

        play_again_shadow = QGraphicsDropShadowEffect(self.play_unlimited_button)
        play_again_shadow.setBlurRadius(15)
        play_again_shadow.setYOffset(5)
        play_again_shadow.setColor(QColor(58, 82, 95, 25))

        self.play_unlimited_button.setGraphicsEffect(play_again_shadow)

        layout.setSpacing(20)
        layout.addLayout(header_layout)
        layout.addWidget(result_container)
        layout.addWidget(answer_label)
        layout.addWidget(self.play_unlimited_button)

        self.setLayout(layout)

    def _play_unlimited(self) -> None:
        game_signals.switch_mode_requested.emit()
        self.accept()
