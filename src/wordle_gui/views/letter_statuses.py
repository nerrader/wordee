from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame


class LetterStatuses(QFrame):
    def __init__(self) -> None:

        super().__init__()

        self.setup_components()
        self.setup_layouts()
        # self.setup_presenters()

    def setup_components(self) -> None:

        self.letter_status_label_header = QLabel("LETTER STATUSES")
        self.letter_status_label_header.setObjectName("letter-statuses-header-label")

        def label_format(letter):
            label_widget = QPushButton(letter)
            label_widget.setProperty("class", "letter-status-label")
            return label_widget

        self.first_letter_row = [
            label_format(letter)
            for letter in ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
        ]
        self.second_letter_row = [
            label_format(letter)
            for letter in ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
        ]
        self.third_letter_row = [
            label_format(letter) for letter in ["Z", "X", "C", "V", "B", "N", "M"]
        ]

    def setup_layouts(self) -> None:
        letter_statuses_layout = QVBoxLayout()

        first_row_layout = QHBoxLayout()
        for label in self.first_letter_row:
            first_row_layout.addWidget(label)

        second_row_layout = QHBoxLayout()
        for label in self.second_letter_row:
            second_row_layout.addWidget(label)

        third_row_layout = QHBoxLayout()
        for label in self.third_letter_row:
            third_row_layout.addWidget(label)

        letter_statuses_layout.addWidget(self.letter_status_label_header)
        letter_statuses_layout.addLayout(first_row_layout)
        letter_statuses_layout.addLayout(second_row_layout)
        letter_statuses_layout.addLayout(third_row_layout)

        self.setLayout(letter_statuses_layout)

    def setup_presenters(self) -> None:
        raise NotImplementedError(
            "setup_presenters() not implemented in letter_statuses.py"
        )
