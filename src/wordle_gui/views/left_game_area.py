from PySide6.QtWidgets import QGridLayout, QLabel, QFrame, QVBoxLayout


class LeftGameArea(QFrame):
    def __init__(self):
        super().__init__()

        self.setup_components()
        self.setup_layouts()
        # self.setup_presenters()

    def setup_components(self):
        self.letter_grid_area_frame = QFrame()
        self.letter_grid_area_frame.setObjectName("letter_grid_area_layout")
        self.letter_grid_label = QLabel("WORDEE LETTER GRID")
        self.letter_grid_label.setObjectName("letter_grid_header_label")
        self.grid_labels: list[list[QLabel]] = []
        self.status_label = QLabel("Start typing to play WORDEE!")

        for _ in range(6):
            row_labels: list[QLabel] = []
            for _ in range(6):
                row_labels.append(QLabel(" "))
            self.grid_labels.append(row_labels)

    def setup_layouts(self):
        left_game_area_layout = QVBoxLayout()
        letter_grid_area_layout = QVBoxLayout()
        letter_grid_layout = QGridLayout()

        for row in self.grid_labels:
            for column in row:
                letter_grid_layout.addWidget(
                    column, self.grid_labels.index(row), row.index(column)
                )

        letter_grid_area_layout.addWidget(self.letter_grid_label)
        letter_grid_area_layout.addLayout(letter_grid_layout)
        self.letter_grid_area_frame.setLayout(letter_grid_area_layout)

        left_game_area_layout.addWidget(self.letter_grid_area_frame)
        left_game_area_layout.addWidget(self.status_label)

        self.setLayout(left_game_area_layout)

    def setup_presenters(self):
        raise NotImplementedError(
            "setup_presenters() not implemented in views/wordee_grid.py"
        )
