from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

# this import is used for the .qrc :/ virtual filepaths to work
from wordle_gui.assets import resources_rc  # type: ignore # noqa: F401


class GameStats(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setup_components()
        self.setup_layouts()
        # setup_presenters()

    def setup_components(self) -> None:
        self.game_stats_label_header = QLabel("GAME STATS")
        self.game_stats_label_header.setObjectName("game_stats_label_header")

        self.mode_label_header = QLabel("Mode - NULL")
        self.mode_label_header.setProperty("class", "game_stats_label")

        self.difficulty_label_header = QLabel("Difficulty - NULL")
        self.difficulty_label_header.setProperty("class", "game_stats_label")

        self.time_elapsed_label = QLabel("Time Elapsed - xx:xx")
        self.time_elapsed_label.setProperty("class", "game_stats_label")

        self.guesses_left_label = QLabel("Guesses Left - 6/6")
        self.guesses_left_label.setProperty("class", "game_stats_label")

    def setup_layouts(self) -> None:
        game_stats_layout = QVBoxLayout()

        game_stats_layout.addWidget(self.game_stats_label_header)
        game_stats_layout.addWidget(self.mode_label_header)
        game_stats_layout.addWidget(self.difficulty_label_header)
        game_stats_layout.addWidget(self.time_elapsed_label)
        game_stats_layout.addWidget(self.guesses_left_label)

        self.setLayout(game_stats_layout)

    def setup_presenters(self) -> None:
        raise NotImplementedError(
            "setup_presenters() not implemented in views/game_stats.py"
        )
