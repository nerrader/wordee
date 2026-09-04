import pytest

from wordee.models.game_logic import WordeeGame


@pytest.fixture
def wordee_game() -> WordeeGame:
    return WordeeGame(
        "EERIE",
        {"sheep", "eerie", "eeeat", "peeel", "iiiis", "rears", "ieere", "stray"},
    )


@pytest.mark.parametrize(
    "input, expected",
    [
        ("EERIE", ["green", "green", "green", "green", "green"]),
        ("EEEAT", ["green", "green", "yellow", "gray", "gray"]),
        ("PEEEL", ["gray", "green", "yellow", "yellow", "gray"]),
        ("IIIIS", ["gray", "gray", "gray", "green", "gray"]),
        ("REARS", ["yellow", "green", "gray", "gray", "gray"]),
        ("IEERE", ["yellow", "green", "yellow", "yellow", "green"]),
    ],
)
def test_get_color_feedback(
    wordee_game: WordeeGame, input: str, expected: list[str]
) -> None:
    assert wordee_game.get_color_feedback(input) == expected


def test_submit_invalid_guess(wordee_game: WordeeGame) -> None:
    with pytest.raises(ValueError):
        wordee_game.submit_guess("ajdkjalf")


def test_submit_guess_is_case_insensitive(wordee_game: WordeeGame) -> None:
    wordee_game.submit_guess("sHeeP")
    assert wordee_game.guesses_left == 5


def test_submit_guess_state_remains_playing(wordee_game: WordeeGame) -> None:
    wordee_game.submit_guess("STRAY")
    assert wordee_game.game_state == "playing"
    assert wordee_game.guesses_left == 5

    wordee_game.submit_guess("sheep")
    assert wordee_game.game_state == "playing"
    assert wordee_game.guesses_left == 4


def test_submit_guess_sets_state_to_win(wordee_game: WordeeGame) -> None:
    wordee_game.submit_guess("eeRIE")
    assert wordee_game.game_state == "win"


def test_submit_guess_sets_state_to_loss(wordee_game: WordeeGame) -> None:
    wordee_game.submit_guess("shEEP")
    wordee_game.submit_guess("shEEP")
    wordee_game.submit_guess("shEEP")
    wordee_game.submit_guess("shEEP")
    wordee_game.submit_guess("shEEP")
    wordee_game.submit_guess("shEEP")
    assert wordee_game.game_state == "loss"
