from typing import TYPE_CHECKING, Literal

import httpx
from loguru import logger

if TYPE_CHECKING:
    from pathlib import Path


def sync_cache(
    cache_type: Literal["possible_solutions", "valid_guesses"],
    cache_dir: Path,
    client: httpx.Client,
) -> None:
    """Fetches data from the github repository, and saves it to cache. Checks ETAG to prevent uneccessary saving.

    Args:
        - cache_type (Literal): The cache type to sync.
        - client (httpx.Client): The HTTPX client to use for the request.
        - cache_dir (Path): The directory where the cache files are stored.
    """

    try:
        request_headers: dict[str, str] = (
            {"If-None-Match": (cache_dir / f"{cache_type}.etag").read_text().strip()}
            if (cache_dir / f"{cache_type}.etag").exists()
            else {}
        )
        response = client.get(
            f"https://raw.githubusercontent.com/nerrader/wordee/refs/heads/main/data/{cache_type}.txt",
            headers=request_headers,
        )
        if response.status_code == 304:
            logger.info(f"Cache type {cache_type} is up to date.")
            return
        elif response.status_code != 200:
            logger.error(
                f"Failed to fetch {cache_type} cache, status code: {response.status_code}"
            )
            raise httpx.HTTPStatusError(
                f"Failed to fetch {cache_type} cache. Status code: {response.status_code}",
                request=response.request,
                response=response,
            )

        (cache_dir / f"{cache_type}.txt").write_text(response.text)
        if response.headers.get("ETag"):
            (cache_dir / f"{cache_type}.etag").write_text(response.headers["ETag"])
        logger.success(f"Cache for {cache_type} downloaded and saved.")

    except httpx.HTTPStatusError as error:
        logger.error(f"Failed to sync cache while fetching {cache_type}: {error}")
        print(f"An error occurred while fetching {cache_type}: {error}")


def read_cache(
    cache_type: Literal["possible_solutions", "valid_guesses"], cache_dir: Path
) -> set[str]:
    """Reads the cache file and returns a set of words.

    Args:
        cache_type (Literal): The cache type to read from.
        cache_dir (Path): The directory where the cache files are stored.

    Raises:
        ValueError: If the cache_type is invalid.
        FileNotFoundError: If the cache file does not exist.
    """
    cache_file = cache_dir / f"{cache_type}.txt"
    if not cache_file.exists():
        logger.error(f"Cache file for {cache_type} not found.")
        raise FileNotFoundError(f"Cache file for {cache_type} not found.")

    logger.debug(f"Successfully read the cache for {cache_type}")
    return set(cache_file.read_text().splitlines())
