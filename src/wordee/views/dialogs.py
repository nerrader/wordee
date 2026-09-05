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

from wordee.constants import GameMode
from wordee.game_signals import game_signals


class GameOverDialog(QDialog):
    """Contains the dialog when you win/lose the game."""

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
        close_button.setProperty("class", "close_button")
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
    """This dialog shows up to block the switching of modes when you
    are currently playing a game."""

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


class HelpMenu(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setContentsMargins(0, 0, 0, 0)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setup_topbar()
        self.setup_help_contents()

        main_layout.addWidget(self.topbar)
        main_layout.addLayout(self.help_contents_layout)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 9)

        self.setLayout(main_layout)

    def setup_topbar(self) -> None:
        topbar_layout = QHBoxLayout()

        self.topbar = QFrame()
        self.topbar.setContentsMargins(10, 10, 10, 10)
        self.topbar.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.topbar.setObjectName("help_menu_topbar")
        self.topbar.setLayout(topbar_layout)

        header_label = QLabel("HOW TO PLAY")
        header_label.setProperty("class", "help_menu_header")

        close_button = QPushButton("x")
        close_button.setProperty("class", "close_button")
        close_button.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        close_button.clicked.connect(self.accept)

        topbar_layout.addWidget(header_label)
        topbar_layout.addStretch()
        topbar_layout.addWidget(close_button)

    def setup_help_contents(self) -> None:
        self.help_contents_layout = QVBoxLayout()
        self.help_contents_layout.setContentsMargins(10, 10, 10, 10)
        introduction_label = QLabel(
            "Wordee is a GUI application for a game called Wordle.\n\n"
            "Wordle is a game where you have six tries to guess a five-letter word.\n\n"
            "Each guess must be a valid word, and each color of the tile will change "
            "depending on how close your guess was to the word."
        )
        introduction_label.setWordWrap(True)
        introduction_label.setProperty("class", "help_menu_context")

        self.setup_legend_container()

        header_example_label = QLabel("EXAMPLE")
        header_example_label.setProperty("class", "help_menu_header")

        example_row_layout = QHBoxLayout()
        example_row_layout.addSpacing(7)

        example_row_data = {
            "F": "gray",
            "R": "gray",
            "A": "green",
            "M": "yellow",
            "E": "green",
        }

        for letter, color in example_row_data.items():
            example_cell = QLabel(letter)
            example_cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
            example_cell.setContentsMargins(10, 10, 10, 10)

            example_cell.setProperty("color", color)
            example_cell.setObjectName("help_menu_example_cell")

            example_row_layout.addWidget(example_cell)

        example_context = QLabel(
            "For context, the word is AMAZE.\n\n"
            "- A and E are in the correct spots, so they are green.\n"
            "- M is misplaced, so it is yellow.\n"
            "- F and R are not in the word, so they are gray."
        )
        example_context.setProperty("class", "help_menu_context")

        self.help_contents_layout.addWidget(introduction_label)
        self.help_contents_layout.addWidget(self.legend_container)

        self.help_contents_layout.addWidget(header_example_label)
        self.help_contents_layout.addLayout(example_row_layout)
        self.help_contents_layout.addWidget(example_context)

    def setup_legend_container(self) -> None:
        legend_layout = QVBoxLayout()
        self.legend_container = QFrame()
        self.legend_container.setContentsMargins(10, 10, 10, 10)
        self.legend_container.setObjectName("help_menu_legend_container")
        self.legend_container.setLayout(legend_layout)

        legend_header = QLabel("LEGEND")
        legend_header.setProperty("class", "help_menu_header")
        legend_layout.addWidget(legend_header)

        legend_data = {
            "green": "This letter is in the correct position.",
            "yellow": "This letter is in the wrong spot.",
            "gray": "This letter is not in the word.",
        }

        for color, context in legend_data.items():
            legend_row = QHBoxLayout()

            color_frame = QFrame()
            color_frame.setObjectName(f"help_menu_legend_{color}_frame")
            color_frame.setMaximumSize(30, 30)

            color_context = QLabel(context)
            color_context.setProperty("class", "help_menu_context")

            legend_row.addWidget(color_frame)
            legend_row.addWidget(color_context)

            legend_layout.addLayout(legend_row)
