from loguru import logger
from PySide6.QtCore import QParallelAnimationGroup, QPoint, QPropertyAnimation, Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from wordee.constants import GameMode, WordeeCellColor


class WordeeCell(QLabel):
    def __init__(self) -> None:
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(10, 10, 10, 10)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        new_size = min(self.width(), self.height())
        self.resize(new_size, new_size)

    def reset_cell(self) -> None:
        self.setText("")
        self.setProperty("color", None)


class WordeeGrid(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setup_components()
        self.setup_layouts()

    def setup_components(self) -> None:
        self.letter_grid_area_frame = QFrame()
        self.letter_grid_area_frame.setObjectName("letter_grid_area")

        # the default mode
        self.letter_grid_area_frame.setProperty("mode", "daily")

        self.header_label = QLabel("WORDEE LETTER GRID")
        self.header_label.setObjectName("letter_grid_header_label")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.wordee_cells: list[list[WordeeCell]] = []

        for _ in range(6):
            row_labels: list[WordeeCell] = []
            for _ in range(5):
                grid_label = WordeeCell()
                row_labels.append(grid_label)
            self.wordee_cells.append(row_labels)

    # i do the rest here because the original_position will bug out if i dont
    def invalid_row_animation(self, row: int) -> None:
        """This displays the shaking animation on the invalid guess row.

        Args:
            row: The row number from 1-6.
        """
        # so the original positions are locked
        if not hasattr(self, "_wordee_cells_original_positions"):
            self._wordee_cells_original_positions = []
            for wordee_row in self.wordee_cells:
                row_cells = []
                for cell in wordee_row:
                    row_cells.append(cell.pos())
                self._wordee_cells_original_positions.append(row_cells)

        grid_row: list[WordeeCell] = self.wordee_cells[row - 1]
        original_position_row = self._wordee_cells_original_positions[row - 1]

        self.animation_group = QParallelAnimationGroup(self)
        self.animation_group.stop()

        for cell, original_position in zip(grid_row, original_position_row):
            shake_animation = QPropertyAnimation(cell, b"pos")
            shake_animation.setDuration(300)

            shake_animation.setKeyValueAt(0.0, original_position)
            shake_animation.setKeyValueAt(0.2, original_position + QPoint(-3, 0))
            shake_animation.setKeyValueAt(0.4, original_position + QPoint(3, 0))
            shake_animation.setKeyValueAt(0.6, original_position + QPoint(-2, 0))
            shake_animation.setKeyValueAt(0.8, original_position + QPoint(2, 0))
            shake_animation.setKeyValueAt(1.0, original_position)

            self.animation_group.addAnimation(shake_animation)

        self.animation_group.start()

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

        letter_grid_area_layout.addWidget(self.header_label)
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

    def update_wordee_row_cell_colors(
        self, row: int, color_feedback: list[WordeeCellColor]
    ) -> None:
        """Updates the wordee cells in the wordee grid.

        Args:
            row: The row number from 1-6
            color_feedback: The color to give to the cells in that row.
        """
        # for the wordee grid color changing
        grid_row: list[WordeeCell] = self.wordee_cells[row - 1]
        for label, color in zip(grid_row, color_feedback):
            label.setProperty("color", color)

            label.style().unpolish(label)
            label.style().polish(label)

    def get_wordee_grid(self) -> list[list[tuple[str, WordeeCellColor | None]]]:
        return [
            [(cell.text(), cell.property("color")) for cell in row]
            for row in self.wordee_cells
        ]

    def update_wordee_grid(
        self, board: list[list[tuple[str, WordeeCellColor | None]]]
    ) -> None:
        for target_row, saved_row in zip(self.wordee_cells, board):
            for target_cell, saved_cell in zip(target_row, saved_row):
                # cell is the tuple[str, str] in this case
                saved_letter, saved_color = saved_cell
                target_cell.setText(saved_letter.upper())
                target_cell.setProperty("color", saved_color)

                target_cell.style().unpolish(target_cell)
                target_cell.style().polish(target_cell)

    def add_letter_to_grid(self, letter: str, row: int) -> None:
        cell = next(
            (cell for cell in self.wordee_cells[row - 1] if not cell.text()), None
        )

        if cell is not None:
            cell.setText(letter.upper())
            return

        logger.info("No cells to update.")

    def delete_last_grid_letter(self, row: int) -> None:
        cell = next(
            (cell for cell in reversed(self.wordee_cells[row - 1]) if cell.text()), None
        )

        if cell is not None:
            cell.setText("")
            return
        logger.info("No cell text to delete.")

    def get_wordee_row_text(self, row: int) -> str:
        return "".join(cell.text() for cell in self.wordee_cells[row - 1])
