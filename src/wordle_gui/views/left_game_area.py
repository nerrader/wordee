from PySide6.QtCore import Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)


class WordeeCell(QLabel):
    def __init__(self) -> None:
        super().__init__()

        self.setProperty("class", "grid_label")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    def resizeEvent(self, event: QResizeEvent) -> None:
        new_size = min(self.width(), self.height())
        self.resize(new_size, new_size)

        super().resizeEvent(event)


class LeftGameArea(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setup_components()
        self.setup_layouts()

    def setup_components(self) -> None:
        self.letter_grid_area_frame = QFrame()
        self.letter_grid_area_frame.setObjectName("letter_grid_area_layout")

        self.letter_grid_label = QLabel("WORDEE LETTER GRID")
        self.letter_grid_label.setObjectName("letter_grid_header_label")
        self.letter_grid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.wordee_cells: list[list[QLabel]] = []

        self.status_label = QLabel("Start typing to play WORDEE!")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for _ in range(6):
            row_labels: list[QLabel] = []
            for _ in range(5):
                grid_label = WordeeCell()
                row_labels.append(grid_label)
            self.wordee_cells.append(row_labels)

    def setup_layouts(self) -> None:
        left_game_area_layout = QVBoxLayout()
        letter_grid_area_layout = QVBoxLayout()
        letter_grid_layout = QGridLayout()
        letter_grid_layout.setSpacing(10)

        for row_index, row in enumerate(self.wordee_cells):
            for column_index, column in enumerate(row):
                letter_grid_layout.addWidget(column, row_index, column_index)

        letter_grid_area_layout.addWidget(self.letter_grid_label)
        letter_grid_area_layout.addLayout(letter_grid_layout)
        letter_grid_area_layout.setStretch(0, 1)
        letter_grid_area_layout.setStretch(1, 9)
        letter_grid_area_layout.setSpacing(10)
        letter_grid_area_layout.setContentsMargins(20, 20, 20, 20)
        letter_grid_area_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.letter_grid_area_frame.setLayout(letter_grid_area_layout)

        # create a layout that centers the grid horizontally
        container_layout = QHBoxLayout()
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.letter_grid_area_frame)

        # left_game_area_layout.addWidget(self.letter_grid_area_frame)
        left_game_area_layout.addLayout(container_layout)
        left_game_area_layout.addWidget(self.status_label)
        left_game_area_layout.setStretch(0, 9)
        left_game_area_layout.setStretch(1, 1)
        left_game_area_layout.setSpacing(20)
        left_game_area_layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(left_game_area_layout)
