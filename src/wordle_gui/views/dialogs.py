from random import choice
from typing import Literal

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

from wordle_gui.constants import GameMode
from wordle_gui.game_signals import game_signals


class GameOverDialog(QDialog):
    def __init__(
        self,
        game_result: Literal["won", "lost", "gave_up"],
        target_word: str,
        game_mode: GameMode,
    ):
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

        extra_win_labels: tuple[str, ...] = (
            "congratulations!",
            "you got good vocab",
            "you didn't google it up right",
            "we get it, you're good",
            "actual tryhard",
        )

        extra_loss_lables: tuple[str, ...] = (
            "better luck next time",
            "you should get better at english",
            "your english teacher would be disappointed",
            "theres only 26 letters in the alphabet",
            "that was tough",
            "try again next time",
            "well, that wasn't exactly your day",
        )

        extra_gave_up_labels: tuple[str, ...] = (
            "you didn't even try man",
            "what the fuck man",
            "really man",
            "come on i thought you were better than this",
            "ok bro",
            "i mean you could've atleast tried, just sayin",
            "godo job.",
        )

        match game_result:
            case "won":
                result_label = QLabel("You WON!")
                extra_label = QLabel(choice(extra_win_labels))
            case "lost":
                result_label = QLabel("You lost.")
                extra_label = QLabel(choice(extra_loss_lables))
            case "gave_up":
                result_label = QLabel("you gave up.")
                extra_label = QLabel(choice(extra_gave_up_labels))

        result_label.setObjectName("post_game_result_label")
        extra_label.setObjectName("post_game_extra_label")

        result_container = QFrame()
        result_container.setObjectName("post_game_result_container")
        result_container.setProperty("game_result", game_result)
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

        self.play_again_button = QPushButton(
            "Play Unlimited Mode" if game_mode == "daily" else "Play Again"
        )
        self.play_again_button.setObjectName("post_game_play_again_button")
        self.play_again_button.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.play_again_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.play_again_button.clicked.connect(
            self._play_unlimited if game_mode == "daily" else self._play_unlimited_again
        )

        play_again_shadow = QGraphicsDropShadowEffect(self.play_again_button)
        play_again_shadow.setBlurRadius(15)
        play_again_shadow.setYOffset(5)
        play_again_shadow.setColor(QColor(58, 82, 95, 25))

        self.play_again_button.setGraphicsEffect(play_again_shadow)

        layout.setSpacing(20)
        layout.addLayout(header_layout)
        layout.addWidget(result_container)
        layout.addWidget(answer_label)
        layout.addWidget(self.play_again_button)

        self.setLayout(layout)

    def _play_unlimited(self) -> None:
        game_signals.switch_mode_requested.emit()
        self.accept()

    def _play_unlimited_again(self) -> None:
        game_signals.play_unlimited_again.emit()
        self.accept()


class BlockSwitchModeDialog(QDialog):
    def __init__(self, game_mode: GameMode):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)

        layout = QVBoxLayout(self)

        result_container = QFrame()
        result_container.setObjectName("block_switch_mode_container")
        result_container.setContentsMargins(10, 10, 10, 10)

        stop_header_label = QLabel("STOP!!")
        stop_header_label.setObjectName("block_switch_mode_stop_header_label")
        stop_header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        daily_content_message = (
            "no switching game modes till you're done with today's daily."
        )
        unlimited_content_message = (
            "no switching modes till you're done with your unlimited game."
        )

        content_label = QLabel(
            daily_content_message if game_mode == "daily" else unlimited_content_message
        )
        content_label.setObjectName("block_switch_mode_contents_label")
        content_label.setWordWrap(True)

        ok_button = QPushButton("ok we get it")
        ok_button.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        ok_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        ok_button.setObjectName("block_switch_mode_ok_button")
        ok_button.clicked.connect(self.accept)

        ok_button_shadow = QGraphicsDropShadowEffect(ok_button)
        ok_button_shadow.setBlurRadius(15)
        ok_button_shadow.setYOffset(5)
        ok_button_shadow.setColor(QColor(58, 82, 95, 25))

        ok_button.setGraphicsEffect(ok_button_shadow)

        layout.setSpacing(20)
        layout.addWidget(stop_header_label)
        layout.addWidget(content_label)
        layout.addWidget(ok_button)

        self.setLayout(layout)
