from wordle_gui import constants as const


class WordeeState:
    def __init__(self) -> None:
        self.current_game_mode: const.GameMode = "daily"
        self.daily_completed: bool = False
