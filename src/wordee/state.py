import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from wordee.constants import GameStatus, WordeeCellColor


@dataclass
class DailyGameState:
    """This class should be used for persistent storage.
    If it is the user's first time, initialize this class
    using default values."""

    # im hoping these values will be provided later on by the presenter or smth
    date: str = date.today().isoformat()
    daily_board: list[list[tuple[str, WordeeCellColor | None]]] = field(
        default_factory=list
    )
    daily_letter_statuses: dict[str, WordeeCellColor | None] = field(
        default_factory=dict
    )
    daily_puzzle_number: int = 0
    daily_time_elapsed: int = 0
    daily_guesses_left: int = 6
    daily_game_status: GameStatus = "playing"


def save_daily_state(filepath: Path, daily_state: DailyGameState) -> None:
    daily_state_dict = {
        "date": daily_state.date,
        "board": daily_state.daily_board,
        "letter_statuses": daily_state.daily_letter_statuses,
        "time_elapsed": daily_state.daily_time_elapsed,
        "guesses_left": daily_state.daily_guesses_left,
        "game_status": daily_state.daily_game_status,
        "puzzle_number": daily_state.daily_puzzle_number,
    }
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(daily_state_dict, file, indent=4)


def load_daily_state(filepath: Path) -> DailyGameState:
    with open(filepath, encoding="utf-8") as file:
        daily_state_dict = json.load(file)

    return DailyGameState(
        date=daily_state_dict["date"],
        daily_board=daily_state_dict["board"],
        daily_letter_statuses=daily_state_dict["letter_statuses"],
        daily_time_elapsed=daily_state_dict["time_elapsed"],
        daily_guesses_left=daily_state_dict["guesses_left"],
        daily_game_status=daily_state_dict["game_status"],
        daily_puzzle_number=daily_state_dict["puzzle_number"],
    )


def load_or_create_daily_state(filepath: Path) -> DailyGameState:
    if not filepath.exists():
        logger.info("Daily state doesn't exist, returning default state.")
        return DailyGameState()

    daily_state = load_daily_state(filepath)
    if daily_state.date != date.today().isoformat():
        logger.info("Daily state is outdated, returning default state.")
        return DailyGameState()

    logger.info("Returning state from state.json")
    return daily_state
