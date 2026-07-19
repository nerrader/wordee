from typing import Literal
from loguru import logger


class WordeeGame:
    def __init__(self, target_word: str, valid_guesses: set[str]) -> None:
        self._target_word: str = target_word.lower()
        self._valid_guesses: set[str] = valid_guesses
        self._guesses_left: int = 6
        self._game_state: Literal["win", "loss", "playing"] = "playing"

    @property
    def target_word(self) -> str:
        return self._target_word

    @property
    def guesses_left(self) -> int:
        return self._guesses_left

    @property
    def game_state(self) -> str:
        return self._game_state

    def get_color_feedback(
        self, guess: str
    ) -> list[Literal["gray", "green", "yellow"]]:
        """From the guess and the current target word, get a list that
        returns "gray"/"yellow"/"green" for every letter in the guess.

        "gray" = The guessed letter doesn't exist in the target word.
        "yellow" = The guessed letter is misplaced.
        "green" = The guessed letter is in the correct spot.
        """
        guess = guess.lower()
        words_in_target_word = set(self.target_word)

        color_feedback: list[Literal["gray", "green", "yellow"]] = []
        for index, letter in enumerate(guess):
            target_word_letter: str = self.target_word[index]

            if letter == target_word_letter:
                color_feedback.append("green")
            elif letter in words_in_target_word:
                color_feedback.append("yellow")
                words_in_target_word.remove(letter)
            else:
                color_feedback.append("gray")

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
