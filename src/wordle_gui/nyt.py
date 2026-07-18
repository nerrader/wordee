# nyt stands for new york times in this case
from datetime import date
from typing import Any

import httpx


def fetch_wordle_solution(user_agent: str) -> str:
    """Fetches the wordle solution for today from the New York Times API."""
    # no httpx client here because it only works when you talk to same domain anyway
    current_date = date.today()
    headers = {"User-Agent": user_agent}
    response = httpx.get(
        f"https://www.nytimes.com/svc/wordle/v2/{current_date}.json", headers=headers
    )
    data: dict[str, Any] = response.json()

    return data["solution"]
