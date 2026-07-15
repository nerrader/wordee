from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from wordle_gui.assets import resources_rc


class GameStats(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setup_components()
        self.setup_layouts()
        # setup_presenters()

    def setup_components(self) -> None:
        self.game_stats_label_header = QLabel("GAME STATS")
        self.game_stats_label_header.setObjectName("game_stats_label_header")

        self.time_elapsed_label = QLabel("Time Elapsed - xx:xx")
        self.time_elapsed_label.setObjectName("time_elapsed_label")

        self.guesses_left_label = QLabel("Guesses Left - 6/6")
        self.guesses_left_label.setObjectName("guesses-left-label")

        self.cat_image = QLabel()
        self.cat_image.setPixmap(QPixmap(":/images/cat-image.png"))

    def setup_layouts(self) -> None:
        game_stats_layout = QVBoxLayout()

        game_stats_layout.addWidget(self.game_stats_label_header)
        game_stats_layout.addWidget(self.time_elapsed_label)
        game_stats_layout.addWidget(self.guesses_left_label)
        game_stats_layout.addWidget(self.cat_image)

        self.setLayout(game_stats_layout)

    def setup_presenters(self):
        raise NotImplementedError(
            "setup_presenters() not implemented in views/game_stats.py"
        )
