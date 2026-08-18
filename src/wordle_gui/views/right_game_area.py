from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QCursor
from PySide6.QtWidgets import (
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
from wordle_gui.views.game_stats import GameStats
from wordle_gui.views.letter_statuses import LetterStatuses


class RightGameArea(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setMaximumWidth(900)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setup_components()
        self.setup_shadows()
        self.setup_layouts()

    def setup_components(self) -> None:
        self.puzzle_number_label = QLabel("Puzzle #NULL")
        self.puzzle_number_label.setObjectName("puzzle_number_label")
        self.puzzle_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.game_stats = GameStats()

        self.letter_statuses = LetterStatuses()

        self.give_up_button = QPushButton("Give Up")
        self.give_up_button.setObjectName("give_up_button")
        self.give_up_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.switch_modes_button = QPushButton("Switch to Unlimited")
        self.switch_modes_button.setObjectName("switch_modes_button")
        self.switch_modes_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.switch_modes_button.clicked.connect(
            game_signals.switch_mode_requested.emit
        )

        # the default mode
        self.switch_modes_button.setProperty("mode", "unlimited")

    def setup_layouts(self) -> None:
        misc_buttons_layout = QHBoxLayout()
        misc_buttons_layout.addWidget(self.give_up_button)
        misc_buttons_layout.addWidget(self.switch_modes_button)

        right_game_area_layout = QVBoxLayout()

        right_game_area_layout.addWidget(self.puzzle_number_label)
        right_game_area_layout.addWidget(
            self.game_stats, alignment=Qt.AlignmentFlag.AlignCenter
        )
        right_game_area_layout.addWidget(self.letter_statuses)
        right_game_area_layout.addLayout(misc_buttons_layout)

        right_game_area_layout.setStretch(0, 1)
        right_game_area_layout.setStretch(1, 3)
        right_game_area_layout.setStretch(2, 4)
        right_game_area_layout.setStretch(3, 1)

        right_game_area_layout.setSpacing(20)
        right_game_area_layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(right_game_area_layout)

    def setup_shadows(self) -> None:
        give_up_button_shadow = QGraphicsDropShadowEffect(self.give_up_button)
        give_up_button_shadow.setColor(QColor("#3A525F40"))
        give_up_button_shadow.setBlurRadius(8)
        give_up_button_shadow.setXOffset(0)
        give_up_button_shadow.setYOffset(4)
        self.give_up_button.setGraphicsEffect(give_up_button_shadow)

        unlimited_button_shadow = QGraphicsDropShadowEffect(self.switch_modes_button)
        unlimited_button_shadow.setColor(QColor("#3A525F40"))
        unlimited_button_shadow.setBlurRadius(8)
        unlimited_button_shadow.setXOffset(0)
        unlimited_button_shadow.setYOffset(4)
        self.switch_modes_button.setGraphicsEffect(unlimited_button_shadow)

    def change_mode_button(self, game_mode: GameMode) -> None:
        if game_mode == "daily":
            self.switch_modes_button.setText("Switch to Daily")
            self.switch_modes_button.setProperty("mode", "daily")
        if game_mode == "unlimited":
            self.switch_modes_button.setText("Switch to Unlimited")
            self.switch_modes_button.setProperty("mode", "unlimited")

        self.switch_modes_button.style().unpolish(self.switch_modes_button)
        self.switch_modes_button.style().polish(self.switch_modes_button)
