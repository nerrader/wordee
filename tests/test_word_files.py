from pathlib import Path

from wordee.logic import word_files


def test_read_word_files(tmp_path: Path) -> None:
    temp_text_filepath = tmp_path / "possible_solutions.txt"
    temp_text_filepath.write_text("test1\ntest2\ntest3\n")
    assert word_files.read_word_file("possible_solutions", tmp_path) == {
        "test1",
        "test2",
        "test3",
    }
