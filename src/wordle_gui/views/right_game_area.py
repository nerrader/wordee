from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QFrame
from wordle_gui.views.game_stats import GameStats
from wordle_gui.views.letter_statuses import LetterStatuses


class RightGameArea(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setup_components()
        self.setup_layouts()
        # self.setup_presenters()

    def setup_components(self) -> None:
        self.puzzle_number_label = QLabel("Puzzle #NULL")
        self.puzzle_number_label.setObjectName("puzzle_number_label")

        self.game_stats = GameStats()

        self.letter_statuses = LetterStatuses()

        self.give_up_button = QPushButton("Give Up")
        self.give_up_button.setObjectName("give_up_button")

        self.switch_to_unlimited_mode_button = QPushButton("Switch to Unlimited")
        self.switch_to_unlimited_mode_button.setObjectName(
            "switch_to_unlimited_mode_button"
        )

    def setup_layouts(self) -> None:
        right_game_area_layout = QVBoxLayout()

        right_game_area_layout.addWidget(self.puzzle_number_label)
        right_game_area_layout.addWidget(self.game_stats)
        right_game_area_layout.addWidget(self.letter_statuses)
        right_game_area_layout.addWidget(self.give_up_button)
        right_game_area_layout.addWidget(self.switch_to_unlimited_mode_button)

        self.setLayout(right_game_area_layout)

    def setup_presenters(self) -> None:
        raise NotImplementedError(
            "setup_presenters() not implemented in right_game_area.py"
        )
