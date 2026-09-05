from datetime import date

import respx
from httpx import Response

from wordee.logic import nyt


@respx.mock
def test_fetch_wordle_solution() -> None:

    current_date = date.today()
    respx.get(f"https://www.nytimes.com/svc/wordle/v2/{current_date}.json").mock(
        return_value=Response(
            200, json={"solution": "pizza", "days_since_launch": 2000}
        )
    )

    solution, puzzle_number = nyt.fetch_wordle_solution("Testing")
    assert solution == "pizza"
    assert puzzle_number == 2000
