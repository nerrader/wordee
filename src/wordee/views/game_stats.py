from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout

# this import is required for the .qrc :/ virtual filepaths to work
from wordee.assets import resources_rc  # noqa: F401
from wordee.constants import GameMode


class GameStats(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.setContentsMargins(20, 10, 20, 10)

        self.setup_components()
        self.setup_layouts()

    def setup_components(self) -> None:
        self.game_stats_label_header = QLabel("GAME STATS")
        self.game_stats_label_header.setProperty("class", "header")

        self.mode_label = QLabel("Mode - Daily")
        self.mode_label.setProperty("class", "game_stats_label")

        self.difficulty_label = QLabel("Difficulty - Normal")
        self.difficulty_label.setProperty("class", "game_stats_label")

        self.seconds_elapsed = 0
        self.time_elapsed_label = QLabel("Time Elapsed - 00:00")
        self.time_elapsed_label.setProperty("class", "game_stats_label")

        self.guesses_left_label = QLabel("Guesses Left - 6/6")
        self.guesses_left_label.setProperty("class", "game_stats_label")

        # this is to initialize it so the check in start_time_elapsed_timer() works
        self.time_elapsed_timer = QTimer()
        self.time_elapsed_timer.timeout.connect(self.update_time_elapsed_timer)

    def setup_layouts(self) -> None:
        game_stats_layout = QVBoxLayout()

        game_stats_layout.addWidget(self.game_stats_label_header)
        game_stats_layout.addWidget(self.mode_label)
        game_stats_layout.addWidget(self.difficulty_label)
        game_stats_layout.addWidget(self.time_elapsed_label)
        game_stats_layout.addWidget(self.guesses_left_label)

        self.setLayout(game_stats_layout)

    def set_guesses_left(self, guesses_left: int) -> None:
        self.guesses_left_label.setText(f"Guesses left -  {guesses_left}/6")

    def set_game_mode(self, game_mode: GameMode) -> None:
        self.mode_label.setText(f"Mode - {game_mode.capitalize()}")

    def start_time_elapsed_timer(self) -> None:
        if self.time_elapsed_timer.isActive():
            return

        self.time_elapsed_timer.start(1000)

    def update_time_elapsed_timer(self, increment: int = 1) -> None:
        self.seconds_elapsed += increment

        minutes = self.seconds_elapsed // 60
        seconds = self.seconds_elapsed % 60

        self.time_elapsed_label.setText(f"Time Elapsed - {minutes:02d}:{seconds:02d}")

    def set_time_elapsed(self, seconds: int) -> None:
        self.seconds_elapsed = seconds

        minutes = self.seconds_elapsed // 60
        seconds = self.seconds_elapsed % 60

        self.time_elapsed_label.setText(f"Time Elapsed - {minutes:02d}:{seconds:02d}")

    def stop_time_elapsed_timer(self) -> None:
        if self.time_elapsed_timer is not None and self.time_elapsed_timer.isActive():
            self.time_elapsed_timer.stop()

    def reset_time_elapsed(self) -> None:
        self.time_elapsed_label.setText("Time Elapsed - 00:00")
        self.seconds_elapsed = 0
