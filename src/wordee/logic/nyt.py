# nyt stands for new york times in this case
from datetime import date
from typing import Any

import httpx
from loguru import logger


def fetch_wordle_solution(user_agent: str) -> tuple[str, int]:
    """Fetches the wordle solution for today from the New York Times API."""
    logger.debug("Starting fetch of wordle solution")
    current_date = date.today()
    # no httpx client here because it only works when you talk to same domain anyway
    try:
        response = httpx.get(
            f"https://www.nytimes.com/svc/wordle/v2/{current_date}.json",
            headers={"User-Agent": user_agent},
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()

        logger.debug("Successfully fetched wordle solution.")

        wordle_solution: str = data["solution"]
        puzzle_number: int = data["days_since_launch"]
        return (wordle_solution, puzzle_number)

    except httpx.ConnectError as error:
        logger.error(f"Fetch wordle solution ({current_date}) failed: {error}")
        raise httpx.ConnectError("HTTP Error when fetching for wordle solution.")
