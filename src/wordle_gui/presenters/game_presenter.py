from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QLabel
    from wordle_gui.views.main_window import MainWindow
    from wordle_gui.models.game_logic import WordeeGame


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
        print(f"Presenter received alphabet key: {key}")
        grid_row_cell_labels: list[QLabel] = self.view.left_game_area.wordee_cells[
            -self.model.guesses_left
        ]
        target_label: QLabel | None = next(
            (label for label in grid_row_cell_labels if label.text() == ""), None
        )

        if target_label is None:
            print("the wordee row is full so it no longer supports any more characters")
            return

        target_label.setText(key.upper())

    def handle_backspace_key(self) -> None:
        print("Presenter received backspace key")
        grid_row_cell_labels: list[QLabel] = self.view.left_game_area.wordee_cells[
            -self.model.guesses_left
        ]

        filled_labels: list[QLabel] = [
            label for label in grid_row_cell_labels if label.text().strip()
        ]

        if not filled_labels:
            print("there are no characters to delete in this row")
            return

        filled_labels[-1].setText("")

    def handle_enter_key(self) -> None:
        print("Presenter received enter key")

        try:
            grid_row_cell_labels: list[QLabel] = self.view.left_game_area.wordee_cells[
                -self.model.guesses_left
            ]
            user_guess: str = "".join([label.text() for label in grid_row_cell_labels])
            print(user_guess)

            # no need to check for length as submit guess does the validation for us
            self.model.submit_guess(user_guess)
            color_feedback = self.model.get_color_feedback(user_guess)

            # to change from the color thing to the status property
            color_feedback_status_map: dict[str, str] = {
                "gray": "absent",
                "yellow": "misplaced",
                "green": "correct",
            }

            for label, color in zip(grid_row_cell_labels, color_feedback):
                label.setProperty("status", color_feedback_status_map[color])
                print((color_feedback_status_map[color]))

                label.style().unpolish(label)
                label.style().polish(label)

        except ValueError:
            print("that is not a valid guess")
            self.view.left_game_area.status_label.setText("That is NOT a valid guess!")
