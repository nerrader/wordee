from loguru import logger

from wordle_gui.constants import GameStatus, WordeeCellColor


class WordeeGame:
    def __init__(
        self,
        target_word: str,
        valid_guesses: set[str],
        guesses_left: int = 6,
        game_state: GameStatus = "playing",
    ) -> None:
        self._target_word: str = target_word.lower()
        self._valid_guesses: set[str] = valid_guesses
        self._guesses_left: int = guesses_left
        self._game_state: GameStatus = game_state

    @property
    def target_word(self) -> str:
        return self._target_word

    @property
    def guesses_left(self) -> int:
        return self._guesses_left

    @property
    def game_state(self) -> GameStatus:
        return self._game_state

    @property
    def can_switch_game_modes(self) -> bool:
        return self.guesses_left == 6 or self.game_state != "playing"

    def get_color_feedback(self, guess: str) -> list[WordeeCellColor]:
        """From the guess and the current target word, get a list that
        returns "gray"/"yellow"/"green" for every letter in the guess.

        "gray" = The guessed letter doesn't exist in the target word.
        "yellow" = The guessed letter is misplaced.
        "green" = The guessed letter is in the correct spot.
        """
        guess = guess.lower()

        color_feedback: list[WordeeCellColor] = ["gray"] * 5

        # do all greens first
        remaining_letters: list[str] = list(self.target_word)
        for index, letter in enumerate(guess):
            target_word_letter: str = self.target_word[index]

            if letter == target_word_letter:
                color_feedback[index] = "green"
                remaining_letters.remove(letter)

        for index, letter in enumerate(guess):
            if (
                letter in remaining_letters  # so theres no double yellows
                and color_feedback[index] == "gray"  # to prevent green to go yellow
            ):
                color_feedback[index] = "yellow"
                remaining_letters.remove(letter)

        return color_feedback

    def submit_guess(self, guess: str) -> None:
        """
        If conditions meet, change the game state, and decrease number of guesses left.
        If the guess is not valid, raise a ValueError.
        """
        guess = guess.lower()

        if guess not in self._valid_guesses:
            logger.warning(f"This guess is not valid: '{guess}'")
            raise ValueError(f"This guess is not valid: '{guess}'")
        self._guesses_left -= 1

        logger.info(f"User guessed: {guess}. Guesses remaining: {self._guesses_left}")

        if (guess != self.target_word) and self.guesses_left == 0:
            logger.info("The user lost the game.")
            self._game_state = "loss"
        elif guess == self.target_word:
            logger.info("The user won the game.")
            self._game_state = "win"

    def give_up_game(self) -> None:
        self._game_state = "loss"
