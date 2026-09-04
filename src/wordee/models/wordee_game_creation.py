from random import choice

from wordee.constants import GameStatus
from wordee.models.game_logic import WordeeGame


class WordeeGameFactory:
    def __init__(
        self, possible_solutions: set[str], valid_guesses: set[str], daily_word: str
    ) -> None:
        self.valid_guesses = valid_guesses
        self.possible_solutions = tuple(possible_solutions)
        self.daily_word = daily_word

    def create_daily_game(
        self,
        guesses_left: int = 6,
        game_state: GameStatus = "playing",
    ) -> WordeeGame:
        return WordeeGame(
            self.daily_word,
            self.valid_guesses,
            guesses_left=guesses_left,
            game_state=game_state,
        )

    def create_unlimited_game(self) -> WordeeGame:
        # had to turn it into a tuple for choice to work to make it truly random
        return WordeeGame(choice(self.possible_solutions), self.valid_guesses)
