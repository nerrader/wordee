from typing import TYPE_CHECKING

from loguru import logger

from wordle_gui.game_signals import game_signals
from wordle_gui.views.game_over_dialog import GameOverDialog

if TYPE_CHECKING:
    from PySide6.QtWidgets import QLabel

    from wordle_gui.constants import GameMode
    from wordle_gui.models.game_logic import WordeeGame
    from wordle_gui.views.letter_statuses import WordeeStatusKey
    from wordle_gui.views.main_window import MainWindow


class GamePresenter:
    def __init__(self, view: MainWindow, model: WordeeGame) -> None:
        self.view = view
        self.model = model
        self.game_mode: GameMode = "daily"
        self.setup_connections()

    @property
    def status_label(self) -> QLabel:
        return self.view.left_game_area.status_label

    @property
    def is_playing(self) -> bool:
        return self.model.game_state == "playing"

    def setup_connections(self) -> None:
        game_signals.alphabet_key_pressed.connect(self.handle_alphabet_key)
        game_signals.backspace_key_pressed.connect(self.handle_backspace_key)
        game_signals.enter_key_pressed.connect(self.handle_enter_key)
        game_signals.switch_mode_requested.connect(self.handle_switch_modes)

    def handle_alphabet_key(self, key: str) -> None:
        """Changes the label in the wordee grid to the letter.

        Args:
            key (str): The alphabetical letter that the user inputted.
        """
        if not self.is_playing:
            return
        logger.debug(f"Presenter recieved alphabet key: {key}")

        # when the user first starts the game and types, to give them more indication on what to do
        # after theyve entered a guess
        if self.model.guesses_left == 6:
            self.view.right_game_area.game_stats.start_time_elapsed_timer()
            self.status_label.setText("Press ENTER to submit guess.")

        grid_row_cell_labels: list[QLabel] = self.view.left_game_area.wordee_cells[
            -self.model.guesses_left
        ]
        target_label: QLabel | None = next(
            (label for label in grid_row_cell_labels if label.text() == ""), None
        )

        if target_label is None:
            return

        target_label.setText(key.upper())

    def handle_backspace_key(self) -> None:
        if not self.is_playing:
            return
        logger.debug("Presenter received backspace key")

        grid_row_cell_labels: list[QLabel] = self.view.left_game_area.wordee_cells[
            -self.model.guesses_left
        ]

        filled_labels: list[QLabel] = [
            label for label in grid_row_cell_labels if label.text().strip()
        ]

        if not filled_labels:
            return

        filled_labels[-1].setText("")

    def handle_enter_key(self) -> None:
        """
        - Submits guess to the model, to change the gamestate variables.
        - Updates color of wordee grid and letter status cells.
        - Occassionally updates status label if something interesting happens.
        """
        if not self.is_playing:
            return
        logger.debug("Presenter received enter key")

        grid_row_cell_labels: list[QLabel] = self.view.left_game_area.wordee_cells[
            -self.model.guesses_left
        ]
        user_guess: str = "".join([label.text() for label in grid_row_cell_labels])

        try:
            # no need to check for length as submit guess does the validation for us
            self.model.submit_guess(user_guess)
        except ValueError:
            self.view.left_game_area.status_label_invalid_animation()
            if len(user_guess) == 0:
                self.status_label.setText("You submitted an empty guess.")
                return
            self.status_label.setText("That is NOT a valid guess!")
            return

        color_feedback = self.model.get_color_feedback(user_guess)
        self.view.right_game_area.game_stats.set_guesses_left(self.model.guesses_left)

        STATUS_FROM_COLOR_MAP: dict[str, str] = {
            "gray": "absent",
            "yellow": "misplaced",
            "green": "correct",
        }

        for label, color in zip(grid_row_cell_labels, color_feedback):
            label.setProperty("status", STATUS_FROM_COLOR_MAP[color])

            label.style().unpolish(label)
            label.style().polish(label)

        letter_status_buttons: list[WordeeStatusKey] = [
            self.view.right_game_area.letter_statuses.keyboard_map[letter.lower()]
            for letter in user_guess
        ]

        for button, color in zip(letter_status_buttons, color_feedback):
            # prevent already green buttons from turning yellow
            if button.property("status") == "correct":
                continue

            button.setProperty("status", STATUS_FROM_COLOR_MAP[color])

            button.style().unpolish(button)
            button.style().polish(button)

        if self.model.game_state in ("win", "loss"):
            result_message = (
                f"Good job! The word was {self.model.target_word.upper()}"
                if self.model.game_state == "win"
                else f"Out of guesses. The word was {self.model.target_word.upper()}"
            )
            self.view.left_game_area.status_label.setText(result_message)
            self.view.right_game_area.game_stats.stop_time_elapsed_timer()

            with self.view.dimmed():
                GameOverDialog(
                    self.model.game_state == "win",
                    self.model.target_word.upper(),
                ).exec()
            return

        if self.model.guesses_left > 1:
            self.status_label.setText("Nice guess! Try another word.")
            return

        self.status_label.setText("Last guess. Make it count!")

    def handle_switch_modes(self) -> None:
        current_game_mode = self.game_mode

        if current_game_mode == "daily":
            self.game_mode = "unlimited"
            self.switch_to_unlimited()
        else:
            self.game_mode = "daily"
            self.switch_to_daily()

    def switch_to_daily(self) -> None:
        self.view.right_game_area.game_stats.set_game_mode("daily")
        self.view.left_game_area.set_game_mode_grid_color("daily")
        self.view.right_game_area.change_mode_button("unlimited")

    def switch_to_unlimited(self) -> None:
        # check here if the daily wordee is completed
        # if so continue
        self.view.right_game_area.game_stats.set_game_mode("unlimited")
        self.view.left_game_area.set_game_mode_grid_color("unlimited")
        self.view.right_game_area.change_mode_button("daily")
