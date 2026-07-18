from datetime import date
from httpx import Response
import respx

from wordle_gui import nyt
from wordle_gui import constants as const


@respx.mock
def test_fetch_wordle_solution() -> None:

    current_date = date.today()
    respx.get(f"https://www.nytimes.com/svc/wordle/v2/{current_date}.json").mock(
        return_value=Response(200, json={"solution": "pizza"})
    )

    solution = nyt.fetch_wordle_solution(const.USER_AGENT)
    assert solution == "pizza"
