from PySide6.QtWidgets import QGridLayout, QLabel, QFrame, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt


class LeftGameArea(QFrame):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        self.setup_components()
        self.setup_layouts()
        # self.setup_presenters()

    def setup_components(self):
        self.letter_grid_area_frame = QFrame()
        self.letter_grid_area_frame.setObjectName("letter_grid_area_layout")
        self.letter_grid_area_frame.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )

        self.letter_grid_label = QLabel("WORDEE LETTER GRID")
        self.letter_grid_label.setObjectName("letter_grid_header_label")
        self.letter_grid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_labels: list[list[QLabel]] = []

        self.status_label = QLabel("Start typing to play WORDEE!")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )

        for _ in range(6):
            row_labels: list[QLabel] = []
            for _ in range(6):
                grid_label = QLabel("A")
                grid_label.setProperty("class", "grid_label")
                grid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                row_labels.append(grid_label)
            self.grid_labels.append(row_labels)

    def setup_layouts(self):
        left_game_area_layout = QVBoxLayout()
        letter_grid_area_layout = QVBoxLayout()
        letter_grid_layout = QGridLayout()

        for row_index, row in enumerate(self.grid_labels):
            for column_index, column in enumerate(row):
                letter_grid_layout.addWidget(column, row_index, column_index)

        letter_grid_area_layout.addWidget(self.letter_grid_label)
        letter_grid_area_layout.addLayout(letter_grid_layout)
        letter_grid_area_layout.setStretch(0, 1)
        letter_grid_area_layout.setStretch(1, 9)
        self.letter_grid_area_frame.setLayout(letter_grid_area_layout)

        left_game_area_layout.addWidget(self.letter_grid_area_frame)
        left_game_area_layout.addWidget(self.status_label)
        left_game_area_layout.setStretch(0, 9)
        left_game_area_layout.setStretch(1, 1)
        left_game_area_layout.setSpacing(10)
        left_game_area_layout.setContentsMargins(20, 10, 20, 10)

        self.setLayout(left_game_area_layout)
        self.setStyleSheet("border: 1px solid red;")

    def setup_presenters(self):
        raise NotImplementedError(
            "setup_presenters() not implemented in views/left_game_area.py"
        )
