from PySide6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QHBoxLayout
from wordle_gui.views.topbar import Topbar
from wordle_gui.views.left_game_area import LeftGameArea
from wordle_gui.views.right_game_area import RightGameArea


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setup_components()
        self.setup_layouts()
        # self.setup_presenters()

    def setup_components(self) -> None:
        self.main_container = QFrame()
        self.main_container.setObjectName("main_container")
        self.setCentralWidget(self.main_container)

        self.topbar = Topbar()
        self.left_game_area = LeftGameArea()
        self.right_game_area = RightGameArea()

    def setup_layouts(self) -> None:
        main_container_layout = QVBoxLayout()
        main_container_layout.setStretch(0, 1)
        main_container_layout.setStretch(1, 9)
        main_container_layout.addWidget(self.topbar)
        main_container_layout.setContentsMargins(0, 0, 0, 0)

        game_area_layout = QHBoxLayout()
        game_area_layout.addWidget(self.left_game_area)
        game_area_layout.addWidget(self.right_game_area)
        game_area_layout.setSpacing(20)

        main_container_layout.addLayout(game_area_layout)

        self.main_container.setLayout(main_container_layout)

    def setup_presenters(self) -> None:
        raise NotImplementedError(
            "setup_presenters() not implemented in views/main_window.py"
        )
