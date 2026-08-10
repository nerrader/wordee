import pytest
from wordle_gui.models.game_logic import WordeeGame


@pytest.fixture
def wordee_game() -> WordeeGame:
    return WordeeGame("ENTRY", set(["stray", "louie", "sheep", "entry"]))


@pytest.mark.parametrize(
    "input, expected",
    [
        ("STRAY", ["gray", "yellow", "yellow", "gray", "green"]),
        ("LOuiE", ["gray", "gray", "gray", "gray", "yellow"]),
        ("SheeP", ["gray", "gray", "yellow", "gray", "gray"]),
        ("entRY", ["green", "green", "green", "green", "green"]),
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


def test_submit_guess_state_remains_playing(wordee_game: WordeeGame) -> None:
    wordee_game.submit_guess("STRAY")
    assert wordee_game.game_state == "playing"

    wordee_game.submit_guess("sheep")
    assert wordee_game.game_state == "playing"


def test_submit_guess_sets_state_to_win(wordee_game: WordeeGame) -> None:
    wordee_game.submit_guess("entry")
    assert wordee_game.game_state == "win"


def test_submit_guess_sets_state_to_loss(wordee_game: WordeeGame) -> None:
    wordee_game.submit_guess("shEEP")
    wordee_game.submit_guess("shEEP")
    wordee_game.submit_guess("shEEP")
    wordee_game.submit_guess("shEEP")
    wordee_game.submit_guess("shEEP")
    wordee_game.submit_guess("shEEP")
    assert wordee_game.game_state == "loss"
