from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

# this import is required for the .qrc :/ virtual filepaths to work
from wordle_gui.assets import resources_rc  # noqa: F401


class GameStats(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setup_components()
        self.setup_layouts()

    def setup_components(self) -> None:
        self.game_stats_label_header = QLabel("GAME STATS")
        self.game_stats_label_header.setObjectName("game_stats_label_header")

        self.mode_label_header = QLabel("Mode - Daily")
        self.mode_label_header.setProperty("class", "game_stats_label")

        self.difficulty_label_header = QLabel("Difficulty - Normal")
        self.difficulty_label_header.setProperty("class", "game_stats_label")

        self.time_elapsed_label = QLabel("Time Elapsed - 00:00")
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

    def set_guesses_left(self, guesses_left: int) -> None:
        self.guesses_left_label.setText(f"Guesses left -  {guesses_left}/6")

    def start_time_elapsed_timer(self) -> None:
        self.seconds_elapsed = 0
        self.time_elapsed_timer = QTimer()
        self.time_elapsed_timer.timeout.connect(self._update_time_elapsed_timer)
        self.time_elapsed_timer.start(1000)

    def _update_time_elapsed_timer(self) -> None:
        self.seconds_elapsed += 1

        minutes = self.seconds_elapsed // 60
        seconds = self.seconds_elapsed % 60

        self.time_elapsed_label.setText(f"Time Elapsed - {minutes:02d}:{seconds:02d}")

    def stop_time_elapsed_timer(self) -> None:
        self.time_elapsed_timer.stop()
