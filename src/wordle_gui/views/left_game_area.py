from PySide6.QtCore import (
    QPoint,
    QPropertyAnimation,
    Qt,
)
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)

from wordle_gui.constants import GameMode


class WordeeCell(QLabel):
    def __init__(self) -> None:
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setContentsMargins(10, 10, 10, 10)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        new_size = min(self.width(), self.height())
        self.resize(new_size, new_size)

    def reset_cell(self) -> None:
        self.setText("")
        self.setProperty("status", None)


class LeftGameArea(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setup_components()
        self.setup_layouts()
        self.setup_animation()

    def setup_components(self) -> None:
        self.letter_grid_area_frame = QFrame()
        self.letter_grid_area_frame.setObjectName("letter_grid_area")

        # the default mode
        self.letter_grid_area_frame.setProperty("mode", "daily")

        self.letter_grid_label = QLabel("WORDEE LETTER GRID")
        self.letter_grid_label.setObjectName("letter_grid_header_label")
        self.letter_grid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.wordee_cells: list[list[WordeeCell]] = []

        self.status_label = QLabel("Start typing to play WORDEE!")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for _ in range(6):
            row_labels: list[WordeeCell] = []
            for _ in range(5):
                grid_label = WordeeCell()
                row_labels.append(grid_label)
            self.wordee_cells.append(row_labels)

    def setup_animation(self) -> None:
        self.shake_animation = QPropertyAnimation(self.status_label, b"pos")
        self.shake_animation.setDuration(300)

    # i do the rest here because the original_position will bug out if i dont
    def status_label_invalid_animation(self) -> None:
        # so the original position is locked
        if not hasattr(self, "_status_label_original_position"):
            self._status_label_original_position = self.status_label.pos()

        original_position = self._status_label_original_position

        self.shake_animation.stop()

        self.shake_animation.setKeyValueAt(0.0, original_position)
        self.shake_animation.setKeyValueAt(0.2, original_position + QPoint(-3, 0))
        self.shake_animation.setKeyValueAt(0.4, original_position + QPoint(3, 0))
        self.shake_animation.setKeyValueAt(0.6, original_position + QPoint(-2, 0))
        self.shake_animation.setKeyValueAt(0.8, original_position + QPoint(2, 0))
        self.shake_animation.setKeyValueAt(1.0, original_position)

        self.shake_animation.start()

    def setup_layouts(self) -> None:
        left_game_area_layout = QVBoxLayout()
        letter_grid_area_layout = QVBoxLayout()
        letter_grid_layout = QGridLayout()
        letter_grid_layout.setSpacing(7)

        for row_index, row in enumerate(self.wordee_cells):
            for column_index, column in enumerate(row):
                letter_grid_layout.addWidget(
                    column,
                    row_index,
                    column_index,
                )

        letter_grid_area_layout.addWidget(self.letter_grid_label)
        letter_grid_area_layout.addLayout(letter_grid_layout)
        letter_grid_area_layout.setStretch(0, 1)
        letter_grid_area_layout.setStretch(1, 9)
        letter_grid_area_layout.setSpacing(10)
        letter_grid_area_layout.setContentsMargins(20, 20, 20, 20)
        self.letter_grid_area_frame.setLayout(letter_grid_area_layout)

        # create a layout that centers the grid horizontally
        container_layout = QHBoxLayout()
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.letter_grid_area_frame)

        left_game_area_layout.addLayout(container_layout)
        left_game_area_layout.addWidget(self.status_label)
        left_game_area_layout.setSpacing(20)
        left_game_area_layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(left_game_area_layout)

    def set_game_mode_grid_color(self, game_mode: GameMode) -> None:
        self.letter_grid_area_frame.setProperty("mode", game_mode)
        self.letter_grid_area_frame.style().unpolish(self.letter_grid_area_frame)
        self.letter_grid_area_frame.style().polish(self.letter_grid_area_frame)

    def reset_wordee_cells(self) -> None:
        for row in self.wordee_cells:
            for cell in row:
                cell.reset_cell()
                cell.style().unpolish(cell)
                cell.style().polish(cell)

    def reset_status_label(self) -> None:
        self.status_label.setText("Start typing to play WORDEE!")
