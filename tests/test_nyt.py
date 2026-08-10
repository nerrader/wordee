from datetime import date

import respx
from httpx import Client as httpxClient
from httpx import Response

from wordle_gui import nyt


@respx.mock
def test_fetch_wordle_solution() -> None:

    current_date = date.today()  # noqa: DTZ011
    respx.get(f"https://www.nytimes.com/svc/wordle/v2/{current_date}.json").mock(
        return_value=Response(200, json={"solution": "pizza"})
    )

    with httpxClient() as client:
        solution = nyt.fetch_wordle_solution(client)
    assert solution == "pizza"
