from importlib.resources import files
from importlib.resources.abc import Traversable
from typing import Literal

from loguru import logger

WORD_FILES = files("wordee.word_lists")


def read_word_file(
    word_file_type: Literal["possible_solutions", "valid_guesses"],
    word_files_dir: Traversable = WORD_FILES,
) -> set[str]:
    """Reads the cache file and returns a set of words.

    Args:
        word_file_type (Literal): The valid word file types.

    Raises:
        FileNotFoundError: If the word file does not exist.
    """
    word_file = word_files_dir / f"{word_file_type}.txt"
    if not word_file.is_file():
        logger.error(f"Word file for {word_file_type} not found.")
        raise FileNotFoundError(f"Word file for {word_file_type} not found.")

    logger.debug(f"Successfully read {word_file_type}.txt")
    return set(word_file.read_text().splitlines())
