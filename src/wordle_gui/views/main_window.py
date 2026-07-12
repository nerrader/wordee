from PySide6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from wordle_gui.views.topbar import Topbar
from wordle_gui.views.left_game_area import LeftGameArea


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setup_components()
        self.setup_layouts()
        # self.setup_presenters()

    def setup_components(self):
        self.main_container = QFrame()
        self.main_container.setObjectName("main_container")
        self.setCentralWidget(self.main_container)

        self.topbar = Topbar()
        self.left_game_area = LeftGameArea()

    def setup_layouts(self):
        main_container_layout = QVBoxLayout()
        main_container_layout.setStretch(3, 17)
        main_container_layout.addWidget(
            self.topbar, alignment=Qt.AlignmentFlag.AlignTop
        )
        main_container_layout.setContentsMargins(0, 0, 0, 0)

        game_area_layout = QHBoxLayout()
        game_area_layout.addWidget(self.left_game_area)
        # to simulate the right game area taking up space
        game_area_layout.addWidget(QFrame())
        main_container_layout.addLayout(game_area_layout)

        self.main_container.setLayout(main_container_layout)

    def setup_presenters(self):
        raise NotImplementedError(
            "setup_presenters() not implemented in views/wordee_grid.py"
        )
