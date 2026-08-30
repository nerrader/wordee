from typing import TYPE_CHECKING

from loguru import logger

from wordle_gui import constants as const
from wordle_gui.game_signals import game_signals
from wordle_gui.models.wordee_game_creation import WordeeGameFactory
from wordle_gui.views.block_switch_mode_dialog import BlockSwitchModeDialog
from wordle_gui.views.game_over_dialog import GameOverDialog

if TYPE_CHECKING:
    from PySide6.QtWidgets import QLabel

    from wordle_gui.state import WordeeState
    from wordle_gui.views.left_game_area import WordeeCell
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
        game_signals.give_up_signal.connect(self.handle_give_up)

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

        # if the user did their first successful guess
        if self.model.guesses_left == 5:
            self.view.right_game_area.enable_give_up_button()

        color_feedback = self.model.get_color_feedback(user_guess)
        self.view.right_game_area.game_stats.set_guesses_left(self.model.guesses_left)

        # 6 - guesses_left is to identify the row to update
        # example: we just submitted the guess, guesses_left = 2
        # should be the 4th row, 6-2 = 4
        self.view.left_game_area.update_wordee_cells(
            (6 - self.model.guesses_left), color_feedback
        )

        self.view.right_game_area.letter_statuses.update_letter_statuses(
            {letter: color for letter, color in zip(user_guess.lower(), color_feedback)}
        )

        if self.model.game_state in ("win", "loss"):
            if self.state.current_game_mode == "daily":
                self.state.daily_completed = True

            result_message = (
                f"Good job! The word was {self.model.target_word.upper()}"
                if self.model.game_state == "win"
                else f"Out of guesses. The word was {self.model.target_word.upper()}"
            )
            self.view.left_game_area.status_label.setText(result_message)
            self.view.right_game_area.game_stats.stop_time_elapsed_timer()

            self.view.right_game_area.disable_give_up_button()
            if self.state.current_game_mode == "unlimited":
                self.view.right_game_area.set_play_again_button()

            with self.view.dimmed():
                GameOverDialog(
                    "won" if self.model.game_state == "win" else "lost",
                    self.model.target_word.upper(),
                    self.state.current_game_mode,
                ).exec()
            return

        if self.model.guesses_left > 1:
            self.status_label.setText("Nice guess! Try another word.")
            return

        self.status_label.setText("Last guess. Make it count!")

    def handle_switch_modes(self) -> None:
        if not self.state.daily_completed or not self.model.can_switch_game_modes:
            with self.view.dimmed():
                BlockSwitchModeDialog(self.state.current_game_mode).exec()
            logger.info(
                "Cant switch games while playing. Give up your game or finish it to switch game_modes."
            )
            return

        self.view.right_game_area.game_stats.stop_time_elapsed_timer()
        current_game_mode = self.state.current_game_mode

        if current_game_mode == "daily":
            self.switch_to_unlimited()
            self.state.current_game_mode = "unlimited"
        else:
            self.switch_to_daily()
            self.state.current_game_mode = "daily"

    def switch_to_daily(self) -> None:
        self.view.right_game_area.set_numbered_puzzle_label(0)
        self.view.right_game_area.game_stats.set_game_mode("daily")
        self.view.left_game_area.set_game_mode_grid_color("daily")
        self.view.right_game_area.change_mode_button("unlimited")
        self.reset_game("daily")

    def switch_to_unlimited(self) -> None:
        self.view.right_game_area.set_unlimited_puzzle_label()
        self.view.right_game_area.game_stats.set_game_mode("unlimited")
        self.view.left_game_area.set_game_mode_grid_color("unlimited")
        self.view.right_game_area.change_mode_button("daily")
        self.reset_game("unlimited")

    def reset_game(self, game_mode: const.GameMode) -> None:
        self.view.reset_game_view()

        if game_mode == "unlimited":
            self.model = self.game_factory.create_unlimited_game()
        else:
            self.model = self.game_factory.create_daily_game()

        self.view.right_game_area.game_stats.set_guesses_left(self.model.guesses_left)
        self.state.current_game_mode = game_mode

    def handle_give_up(self) -> None:
        if not self.view.right_game_area.give_up_button_enabled:
            return

        self.model.give_up_game()

        if self.state.current_game_mode == "daily":
            self.state.daily_completed = True

        self.view.right_game_area.game_stats.stop_time_elapsed_timer()

        result_message = f"You gave up. The word was {self.model.target_word.upper()}."
        self.view.left_game_area.status_label.setText(result_message)
        self.view.right_game_area.game_stats.stop_time_elapsed_timer()

        if self.state.current_game_mode == "unlimited":
            self.view.right_game_area.set_play_again_button()

        with self.view.dimmed():
            GameOverDialog(
                game_result="gave_up",
                target_word=self.model.target_word,
                game_mode=self.state.current_game_mode,
            ).exec()
