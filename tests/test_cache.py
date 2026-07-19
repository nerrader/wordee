from pathlib import Path

import httpx

from wordle_gui import cache


def test_sync_cache(tmp_path: Path) -> None:
    with httpx.Client(timeout=10.0, headers={"User-Agent": "test-agent"}) as client:
        cache.sync_cache("possible_solutions", tmp_path, client)
        cache.sync_cache("valid_guesses", tmp_path, client)

    assert (tmp_path / "possible_solutions.txt").exists()
    assert (tmp_path / "possible_solutions.etag").exists()
    assert (tmp_path / "valid_guesses.txt").exists()
    assert (tmp_path / "valid_guesses.etag").exists()


def test_read_cache(tmp_path: Path) -> None:
    temp_text_filepath = tmp_path / "possible_solutions.txt"
    temp_text_filepath.write_text("test1\ntest2\ntest3\n")
    assert cache.read_cache("possible_solutions", tmp_path) == {
        "test1",
        "test2",
        "test3",
    }
