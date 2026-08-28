from typing import TYPE_CHECKING

from loguru import logger

from wordle_gui import constants as const
from wordle_gui.game_signals import game_signals
from wordle_gui.models.wordee_game_creation import WordeeGameFactory
from wordle_gui.views.game_over_dialog import GameOverDialog

if TYPE_CHECKING:
    from PySide6.QtWidgets import QLabel

    from wordle_gui.state import WordeeState
    from wordle_gui.views.left_game_area import WordeeCell
    from wordle_gui.views.letter_statuses import WordeeStatusKey
    from wordle_gui.views.main_window import MainWindow


class GamePresenter:
    def __init__(
        self, view: MainWindow, game_factory: WordeeGameFactory, state: WordeeState
    ) -> None:
        self.view = view
        self.game_factory = game_factory
        self.model = game_factory.create_daily_game()
        self.state = state
        self.setup_connections()

    # basically just shortcuts cuz i was too lazy to type the full thing
    @property
    def status_label(self) -> QLabel:
        return self.view.left_game_area.status_label

    def setup_connections(self) -> None:
        game_signals.alphabet_key_pressed.connect(self.handle_alphabet_key)
        game_signals.backspace_key_pressed.connect(self.handle_backspace_key)
        game_signals.enter_key_pressed.connect(self.handle_enter_key)
        game_signals.switch_mode_requested.connect(self.handle_switch_modes)
        game_signals.play_unlimited_again.connect(lambda: self.reset_game("unlimited"))

    def handle_alphabet_key(self, key: str) -> None:
        """Changes the label in the wordee grid to the letter.

        Args:
            key (str): The alphabetical letter that the user inputted.
        """
        if self.model.game_state != "playing":
            return
        logger.debug(f"Presenter recieved alphabet key: {key}")

        # when the user first starts the game and types, to give them more indication on what to do
        # after theyve entered a guess
        if self.model.guesses_left == 6:
            self.view.right_game_area.game_stats.start_time_elapsed_timer()
            self.status_label.setText("Press ENTER to submit guess.")

        grid_row_cell_labels: list[WordeeCell] = self.view.left_game_area.wordee_cells[
            -self.model.guesses_left
        ]
        target_label: QLabel | None = next(
            (label for label in grid_row_cell_labels if label.text() == ""), None
        )

        if target_label is None:
            return

        target_label.setText(key.upper())

    def handle_backspace_key(self) -> None:
        if self.model.game_state != "playing":
            return
        logger.debug("Presenter received backspace key")

        grid_row_cell_labels: list[WordeeCell] = self.view.left_game_area.wordee_cells[
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
        if self.model.game_state != "playing":
            return
        logger.debug("Presenter received enter key")

        grid_row_cell_labels: list[WordeeCell] = self.view.left_game_area.wordee_cells[
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

        # for the wordee grid color changing
        for label, color in zip(grid_row_cell_labels, color_feedback):
            label.setProperty("status", STATUS_FROM_COLOR_MAP[color])

            label.style().unpolish(label)
            label.style().polish(label)

        letter_status_buttons: list[WordeeStatusKey] = [
            self.view.right_game_area.letter_statuses.keyboard_map[letter.lower()]
            for letter in user_guess
        ]

        # for the letter statuses color changing
        for button, color in zip(letter_status_buttons, color_feedback):
            # prevent already green buttons from turning yellow
            if button.property("status") == "correct":
                continue

            button.setProperty("status", STATUS_FROM_COLOR_MAP[color])

            button.style().unpolish(button)
            button.style().polish(button)

        if self.model.game_state in ("win", "loss"):
            self.state.daily_completed = True
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
                    self.state.current_game_mode,
                ).exec()
            return

        if self.model.guesses_left > 1:
            self.status_label.setText("Nice guess! Try another word.")
            return

        self.status_label.setText("Last guess. Make it count!")

    def handle_switch_modes(self) -> None:
        if not self.model.can_switch_gamemodes:
            # TODO: change it into a ui element later
            logger.info(
                "Cant switch games while playing. Give up your game or finish it to switch gamemodes."
            )
            return
        self.view.right_game_area.game_stats.stop_time_elapsed_timer()
        current_game_mode = self.state.current_game_mode

        if current_game_mode == "daily":
            self.state.current_game_mode = "unlimited"
            self.switch_to_unlimited()
        else:
            self.state.current_game_mode = "daily"
            self.switch_to_daily()

    def switch_to_daily(self) -> None:
        self.view.right_game_area.set_numbered_puzzle_label(0)
        self.view.right_game_area.game_stats.set_game_mode("daily")
        self.view.left_game_area.set_game_mode_grid_color("daily")
        self.view.right_game_area.change_mode_button("unlimited")
        self.reset_game("daily")

    def switch_to_unlimited(self) -> None:
        if not self.state.daily_completed:
            logger.info("You must beat daily mode before switching to unlimited.")
            return
        self.view.right_game_area.set_unlimited_puzzle_label()
        self.view.right_game_area.game_stats.set_game_mode("unlimited")
        self.view.left_game_area.set_game_mode_grid_color("unlimited")
        self.view.right_game_area.change_mode_button("daily")
        self.reset_game("unlimited")

    def reset_game(self, gamemode: const.GameMode) -> None:
        self.view.reset_game_view()
        if gamemode == "unlimited":
            self.model = self.game_factory.create_unlimited_game()
        else:
            self.model = self.game_factory.create_daily_game()
        self.view.right_game_area.game_stats.set_guesses_left(self.model.guesses_left)
        self.state.current_game_mode = gamemode
