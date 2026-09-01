from typing import TYPE_CHECKING

from loguru import logger

from wordle_gui import constants as const
from wordle_gui.game_signals import game_signals
from wordle_gui.models.wordee_game_creation import WordeeGameFactory
from wordle_gui.views.dialogs import BlockSwitchModeDialog, GameOverDialog

if TYPE_CHECKING:
    from PySide6.QtWidgets import QLabel

    from wordle_gui.state import DailyGameState
    from wordle_gui.views.left_game_area import WordeeCell
    from wordle_gui.views.main_window import MainWindow


class GamePresenter:
    def __init__(
        self,
        view: MainWindow,
        game_factory: WordeeGameFactory,
        daily_game_state: DailyGameState,
    ) -> None:
        self.view = view
        self.game_factory = game_factory
        self.state = daily_game_state
        self.model = game_factory.create_daily_game(
            self.state.daily_guesses_left, self.state.daily_game_status
        )
        self.current_game_mode: const.GameMode = "daily"
        self.setup_connections()

        # I WANT TO LET YALL KNOW THIS EXTRA LOGIC IS CAUSE OF
        # THE PERSISTENT DAILY GAME STATE ALRIGHT

        # if the state is still default values aka first time opening up the thingy
        # fill it in with the actual default values
        if not self.state.daily_board:
            print("It got in the daily board ====")
            self.state.daily_board = self.view.left_game_area.get_wordee_grid()
        if not self.state.daily_letter_statuses:
            print("It got in the daily_letter_statuses")
            self.state.daily_letter_statuses = (
                self.view.right_game_area.letter_statuses.get_letter_statuses()
            )

        # might as well update them for those who actually do have
        # values for the state
        self.view.left_game_area.update_wordee_grid(self.state.daily_board)
        self.view.right_game_area.letter_statuses.update_letter_statuses(
            self.state.daily_letter_statuses
        )
        self.view.right_game_area.game_stats.set_time_elapsed(
            self.state.daily_time_elapsed
        )

        # the user has done atleast one guess this means
        if self.model.guesses_left <= 5 and self.model.game_state == "playing":
            self.view.right_game_area.enable_give_up_button()

    # basically just shortcuts cuz i was too lazy to type the full thing
    @property
    def status_label(self) -> QLabel:
        return self.view.left_game_area.status_label

    def setup_connections(self) -> None:
        game_signals.alphabet_key_pressed.connect(self.handle_alphabet_key)
        game_signals.backspace_key_pressed.connect(self.handle_backspace_key)
        game_signals.enter_key_pressed.connect(self.handle_enter_key)
        game_signals.switch_mode_requested.connect(self.handle_switch_modes)
        game_signals.play_unlimited_again.connect(self.reset_unlimited_game)
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
            self.status_label.setText("Press ENTER to submit guess.")

        grid_row_cell_labels: list[WordeeCell] = self.view.left_game_area.wordee_cells[
            -self.model.guesses_left
        ]
        target_label: QLabel | None = next(
            (label for label in grid_row_cell_labels if label.text() == ""), None
        )

        if target_label is None:
            return

        # it checks if its started or not in the function, so just do this
        self.view.right_game_area.game_stats.start_time_elapsed_timer()

        target_label.setText(key.upper())

        if self.current_game_mode == "daily":
            self.state.daily_board = self.view.left_game_area.get_wordee_grid()

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

        if self.current_game_mode == "daily":
            self.state.daily_board = self.view.left_game_area.get_wordee_grid()

    def handle_enter_key(self) -> None:
        """
        - Submits guess to the model, to change the gamestate variables.
        - Updates color of wordee grid and letter status cells.
        - Occassionally updates status label if something interesting happens.
        """
        if self.model.game_state != "playing":
            return

        logger.debug("Presenter received enter key")
        print(self.view.right_game_area.game_stats.seconds_elapsed)

        grid_row_cell_labels: list[WordeeCell] = self.view.left_game_area.wordee_cells[
            -self.model.guesses_left
        ]
        user_guess: str = "".join(label.text() for label in grid_row_cell_labels)

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

        # 6 - guesses_left is to identify the row to update
        # example: we just submitted the guess, guesses_left = 2
        # should be the 4th row, 6-2 = 4
        self.view.left_game_area.update_wordee_row_cell_colors(
            (6 - self.model.guesses_left), color_feedback
        )

        self.view.right_game_area.letter_statuses.update_letter_statuses(
            {letter: color for letter, color in zip(user_guess.lower(), color_feedback)}
        )

        # no need for an if check cuz view already does that now
        self.view.right_game_area.enable_give_up_button()

        # update all state when the view finishes updating stuff
        if self.current_game_mode == "daily":
            self.state.daily_guesses_left -= 1
            self.state.daily_board = self.view.left_game_area.get_wordee_grid()
            self.state.daily_letter_statuses = (
                self.view.right_game_area.letter_statuses.get_letter_statuses()
            )

        if self.model.game_state in ("win", "loss"):
            result_message = (
                f"Good job! The word was {self.model.target_word.upper()}"
                if self.model.game_state == "win"
                else f"Out of guesses. The word was {self.model.target_word.upper()}"
            )
            self.view.left_game_area.status_label.setText(result_message)
            self.view.right_game_area.game_stats.stop_time_elapsed_timer()

            if self.current_game_mode == "daily":
                self.state.daily_game_status = self.model.game_state
                self.state.daily_time_elapsed = (
                    self.view.right_game_area.game_stats.seconds_elapsed
                )

            self.view.right_game_area.disable_give_up_button()
            if self.current_game_mode == "unlimited":
                self.view.right_game_area.set_play_again_button()

            with self.view.dimmed():
                GameOverDialog(
                    "won" if self.model.game_state == "win" else "lost",
                    self.model.target_word.upper(),
                    self.current_game_mode,
                ).exec()
            return

        if self.model.guesses_left > 1:
            self.status_label.setText("Nice guess! Try another word.")
            return

        self.status_label.setText("Last guess. Make it count!")

    def handle_switch_modes(self) -> None:
        if (
            self.state.daily_game_status not in ("win", "loss")
            or not self.model.can_switch_game_modes
        ):
            with self.view.dimmed():
                BlockSwitchModeDialog(self.current_game_mode).exec()
            logger.info(
                "Cant switch games while playing. Give up your game or finish it to switch game_modes."
            )
            return

        self.view.right_game_area.game_stats.stop_time_elapsed_timer()
        current_game_mode = self.current_game_mode

        if current_game_mode == "daily":
            self.switch_to_unlimited()
            self.current_game_mode = "unlimited"
        else:
            self.switch_to_daily()
            self.current_game_mode = "daily"

    def switch_to_daily(self) -> None:
        # if it gets through this function, that means that the
        # user already finished daily mode
        # so that means he just wants to admire it or smth
        self.view.right_game_area.set_numbered_puzzle_label(0)
        self.view.right_game_area.game_stats.set_game_mode("daily")
        self.view.left_game_area.set_game_mode_grid_color("daily")
        self.view.right_game_area.change_mode_button("unlimited")
        self.view.right_game_area.letter_statuses.update_letter_statuses(
            self.state.daily_letter_statuses
        )
        self.view.left_game_area.update_wordee_grid(self.state.daily_board)
        self.view.right_game_area.game_stats.set_time_elapsed(
            self.state.daily_time_elapsed
        )

    def switch_to_unlimited(self) -> None:
        self.view.right_game_area.set_unlimited_puzzle_label()
        self.view.right_game_area.game_stats.set_game_mode("unlimited")
        self.view.left_game_area.set_game_mode_grid_color("unlimited")
        self.view.right_game_area.change_mode_button("daily")
        self.reset_unlimited_game()

    def reset_unlimited_game(self) -> None:
        self.view.reset_game_view()

        self.model = self.game_factory.create_unlimited_game()
        self.view.right_game_area.game_stats.set_guesses_left(self.model.guesses_left)

    def handle_give_up(self) -> None:
        if not self.view.right_game_area.give_up_button_enabled:
            return

        self.model.give_up_game()

        if self.current_game_mode == "daily":
            self.state.daily_game_status = "loss"
            self.state.daily_time_elapsed = (
                self.view.right_game_area.game_stats.seconds_elapsed
            )

        self.view.right_game_area.game_stats.stop_time_elapsed_timer()

        result_message = f"You gave up. The word was {self.model.target_word.upper()}."
        self.view.left_game_area.status_label.setText(result_message)

        if self.current_game_mode == "unlimited":
            self.view.right_game_area.set_play_again_button()

        with self.view.dimmed():
            GameOverDialog(
                game_result="gave_up",
                target_word=self.model.target_word,
                game_mode=self.current_game_mode,
            ).exec()
