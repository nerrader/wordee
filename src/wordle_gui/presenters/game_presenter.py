from typing import TYPE_CHECKING
from loguru import logger

if TYPE_CHECKING:
    from PySide6.QtWidgets import QLabel
    from wordle_gui.views.main_window import MainWindow
    from wordle_gui.models.game_logic import WordeeGame
    from wordle_gui.views.letter_statuses import WordeeStatusKey


class GamePresenter:
    def __init__(self, view: MainWindow, model: WordeeGame) -> None:
        self.view = view
        self.model = model
        self.setup_connections()

    def setup_connections(self) -> None:
        self.view.alphabet_key_signal.connect(self.handle_alphabet_key)
        self.view.backspace_key_signal.connect(self.handle_backspace_key)
        self.view.enter_key_signal.connect(self.handle_enter_key)

    def handle_alphabet_key(self, key: str) -> None:
        """Changes the label in the grid to the letter

        Args:
            key (str): The alphabetical letter that the user inputted.
        """
        logger.debug(f"Presenter recieved alphabet key: {key}")

        if self.model.guesses_left == 6:
            self.view.left_game_area.status_label.setText(
                "Press ENTER to submit guess."
            )
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
        logger.debug("Presenter received enter key")

        grid_row_cell_labels: list[QLabel] = self.view.left_game_area.wordee_cells[
            -self.model.guesses_left
        ]
        user_guess: str = "".join([label.text() for label in grid_row_cell_labels])

        try:
            # no need to check for length as submit guess does the validation for us
            self.model.submit_guess(user_guess)
            color_feedback = self.model.get_color_feedback(user_guess)
            self.view.right_game_area.game_stats.guesses_left_label.setText(
                f"Guesses Left - {self.model.guesses_left}/6"
            )

            # to change from the color thing to the status property
            color_feedback_status_map: dict[str, str] = {
                "gray": "absent",
                "yellow": "misplaced",
                "green": "correct",
            }

            for label, color in zip(grid_row_cell_labels, color_feedback):
                label.setProperty("status", color_feedback_status_map[color])

                label.style().unpolish(label)
                label.style().polish(label)

            letter_status_buttons: list[WordeeStatusKey] = [
                self.view.right_game_area.letter_statuses.keyboard_map[letter.lower()]
                for letter in user_guess
            ]

            print(letter_status_buttons)

            for button, color in zip(letter_status_buttons, color_feedback):
                button.setProperty("status", color_feedback_status_map[color])

                button.style().unpolish(button)
                button.style().polish(button)

        except ValueError:
            self.view.left_game_area.status_label.setText("That is NOT a valid guess!")
            return

        if self.model.guesses_left == 1:
            self.view.left_game_area.status_label.setText("Last guess. Make it count!")
        else:
            self.view.left_game_area.status_label.setText(
                "Good guess. Try another word."
            )

        match self.model.game_state:
            case "win":
                self.view.left_game_area.status_label.setText(
                    f"Good job! The word was {self.model.target_word.upper()}"
                )
            case "loss":
                self.view.left_game_area.status_label.setText(
                    f"Out of guesses. The word was {self.model.target_word.upper()}"
                )

            case _:
                pass
