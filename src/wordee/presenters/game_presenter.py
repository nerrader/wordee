from typing import TYPE_CHECKING

from loguru import logger

from wordee.game_signals import game_signals
from wordee.models.wordee_game_creation import WordeeGameFactory
from wordee.views.dialogs import BlockSwitchModeDialog, GameOverDialog

if TYPE_CHECKING:
    from wordee.constants import GameMode
    from wordee.state import DailyGameState
    from wordee.views.main_window import MainWindow


class GamePresenter:
    """This class coordinates most of the events and their actions,
    including the switching of current gamemodes and saving of
    the persistent daily state.
    """

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
        self.current_game_mode: GameMode = "daily"
        self.setup_connections()
        self.restore_daily_view()

    @property
    def guess_row_number(self) -> int:
        return 7 - self.model.guesses_left

    def setup_connections(self) -> None:
        game_signals.alphabet_key_pressed.connect(self.handle_alphabet_key)
        game_signals.backspace_key_pressed.connect(self.handle_backspace_key)
        game_signals.enter_key_pressed.connect(self.handle_enter_key)
        game_signals.switch_mode_requested.connect(self.handle_switch_modes)
        game_signals.play_unlimited_again.connect(self.reset_unlimited_game)
        game_signals.give_up_signal.connect(self.handle_give_up)

    def sync_daily_state(self) -> None:
        """Syncs the daily state with the model and view states.

        Raises:
            RuntimeError: If the current gamemode is not daily.
        """
        if self.current_game_mode != "daily":
            raise RuntimeError("The current game_mode is not daily.")

        self.state.daily_board = self.view.wordee_grid.get_wordee_grid()
        self.state.daily_letter_statuses = (
            self.view.right_game_area.letter_statuses.get_letter_statuses()
        )
        self.state.daily_guesses_left = self.model.guesses_left
        self.state.daily_time_elapsed = (
            self.view.right_game_area.game_stats.seconds_elapsed
        )
        self.state.daily_game_status = self.model.game_state

    def restore_daily_view(self) -> None:
        """Restores the daily view by using the persistent daily state to update
        the daily_board, letter statuses, time_elapsed, and setting the state of the
        give up button"""
        # if the state is still default values aka first time opening up the thingy
        # fill it in with the actual default values
        if not self.state.daily_board:
            self.state.daily_board = self.view.wordee_grid.get_wordee_grid()
        if not self.state.daily_letter_statuses:
            self.state.daily_letter_statuses = (
                self.view.right_game_area.letter_statuses.get_letter_statuses()
            )

        # might as well update them for those who actually do have
        # values for the state
        self.view.wordee_grid.update_wordee_grid(self.state.daily_board)
        self.view.right_game_area.letter_statuses.update_letter_statuses(
            self.state.daily_letter_statuses
        )
        self.view.right_game_area.game_stats.set_time_elapsed(
            self.state.daily_time_elapsed
        )

        if self.model.guesses_left <= 5 and self.model.game_state == "playing":
            self.view.right_game_area.enable_give_up_button()

        # 0 is jsut a placeholder number, itll have the days_since_launch
        # from the nyt in the real game
        self.view.right_game_area.set_numbered_puzzle_label(
            self.state.daily_puzzle_number
        )
        self.view.right_game_area.game_stats.set_game_mode("daily")
        self.view.wordee_grid.set_game_mode_grid_color("daily")

        # this means, switch the mode button to say switch to unlimited
        self.view.right_game_area.change_mode_button("unlimited")

    def handle_alphabet_key(self, key: str) -> None:
        if self.model.game_state != "playing":
            return

        logger.debug(f"Presenter recieved alphabet key: {key}")
        self.view.wordee_grid.add_letter_to_grid(key, self.guess_row_number)

        # it checks if its started or not in the function, so just do this
        self.view.right_game_area.game_stats.start_time_elapsed_timer()

        if self.current_game_mode == "daily":
            self.sync_daily_state()

    def handle_backspace_key(self) -> None:
        if self.model.game_state != "playing":
            return

        logger.debug("Presenter received backspace key")
        self.view.wordee_grid.delete_last_grid_letter(self.guess_row_number)

        if self.current_game_mode == "daily":
            self.sync_daily_state()

    def handle_enter_key(self) -> None:
        if self.model.game_state != "playing":
            return

        logger.debug("Presenter received enter key")

        user_guess = self.view.wordee_grid.get_wordee_row_text(self.guess_row_number)
        # im saving it now cuz itll change when we submit guess
        user_guess_row = self.guess_row_number

        try:
            # no need to check for length as submit guess does the validation for us
            self.model.submit_guess(user_guess)
        except ValueError:
            self.view.wordee_grid.invalid_row_animation(user_guess_row)
            return

        color_feedback = self.model.get_color_feedback(user_guess)
        self.view.right_game_area.game_stats.set_guesses_left(self.model.guesses_left)

        self.view.wordee_grid.update_wordee_row_cell_colors(
            user_guess_row, color_feedback
        )

        self.view.right_game_area.letter_statuses.update_letter_statuses(
            {letter: color for letter, color in zip(user_guess.lower(), color_feedback)}
        )

        # no need for an if check cuz view already does that now
        self.view.right_game_area.enable_give_up_button()

        # update all state when the view finishes updating stuff
        if self.current_game_mode == "daily":
            self.sync_daily_state()

        if self.model.game_state in ("win", "loss"):
            self.view.right_game_area.game_stats.stop_time_elapsed_timer()
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

    def handle_switch_modes(self) -> None:
        """Handles the switching of current gamemode, daily to unlimited and vice versa
        This will execute the retrospective switch_to_{mode} functions.

        You cannot switch modes while playing in a game."""
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

        self.view.right_game_area.game_stats.reset_time_elapsed()
        current_game_mode = self.current_game_mode

        if current_game_mode == "daily":
            self.switch_to_unlimited()
            self.current_game_mode = "unlimited"
        else:
            self.restore_daily_view()
            self.current_game_mode = "daily"

    def switch_to_unlimited(self) -> None:
        self.view.right_game_area.set_unlimited_puzzle_label()
        self.view.right_game_area.game_stats.set_game_mode("unlimited")
        self.view.wordee_grid.set_game_mode_grid_color("unlimited")
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
            self.sync_daily_state()

        self.view.right_game_area.game_stats.stop_time_elapsed_timer()

        if self.current_game_mode == "unlimited":
            self.view.right_game_area.set_play_again_button()

        with self.view.dimmed():
            GameOverDialog(
                game_result="gave_up",
                target_word=self.model.target_word,
                game_mode=self.current_game_mode,
            ).exec()
