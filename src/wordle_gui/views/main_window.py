from PySide6.QtWidgets import QMainWindow, QFrame, QVBoxLayout
from PySide6.QtCore import Qt
from wordle_gui.views.topbar import Topbar


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        container = QFrame()
        container.setObjectName("main_container")
        self.setCentralWidget(container)

        topbar = Topbar()
        main_container_layout = QVBoxLayout()
        main_container_layout.setStretch(3, 17)
        main_container_layout.addWidget(topbar, alignment=Qt.AlignmentFlag.AlignTop)
        main_container_layout.setContentsMargins(0, 0, 0, 0)

        container.setLayout(main_container_layout)
