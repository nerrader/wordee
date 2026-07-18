from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import httpx
    from pathlib import Path


def validate_cache_type(cache_type: str) -> None:
    """Checks the filename base and raises an error if invalid.
    Only 'possible_solutions' and 'valid_guesses' are valid filename bases."""
    if cache_type not in ["possible_solutions", "valid_guesses"]:
        raise ValueError(f"Invalid filename base: {cache_type}")


def sync_cache(cache_type: str, cache_dir: Path, client: httpx.Client) -> None:
    """Fetches data from the github repository, and saves it to cache. Checks ETAG to prevent uneccessary saving.

    Args:
        - cache_type (str): Can only be "possible_solutions" or "valid_guesses",
        as those are the only two types of cache used in this application currently.
        - client (httpx.Client | None, optional): The HTTPX client to use for the request.
        If None, a new client will be created for this request. Defaults to None.
        - cache_dir (Path): The directory where the cache files are stored.
    """

    validate_cache_type(cache_type)
    try:
        request_headers: dict[str, str] = (
            {"If-None-Match": (cache_dir / f"{cache_type}.etag").read_text().strip()}
            if (cache_dir / f"{cache_type}.etag").exists()
            else {}
        )
        response = client.get(
            f"https://raw.githubusercontent.com/nerrader/wordle-gui/refs/heads/main/data/{cache_type}.txt",
            headers=request_headers,
        )
        if response.status_code == 304:
            print(f"Cache for {cache_type} is up to date.")
            return
        elif response.status_code != 200:
            raise httpx.HTTPStatusError(
                f"Failed to fetch {cache_type} cache. Status code: {response.status_code}",
                request=response.request,
                response=response,
            )

        (cache_dir / f"{cache_type}.txt").write_text(response.text)
        if response.headers.get("ETag"):
            (cache_dir / f"{cache_type}.etag").write_text(response.headers["ETag"])
        print(f"Cache for {cache_type} downloaded and saved.")

    except Exception as error:
        print(f"An error occurred while fetching {cache_type}: {error}")


def read_cache(cache_type: str, cache_dir: Path) -> set[str]:
    """Reads the cache file and returns a set of words.

    Args:
        cache_type (str): Can only be "possible_solutions" or "valid_guesses",
        as those are the only two types of cache used in this application currently.
        cache_dir (Path): The directory where the cache files are stored.

    Raises:
        ValueError: If the cache_type is invalid.
        FileNotFoundError: If the cache file does not exist.
    """
    validate_cache_type(cache_type)

    cache_file = cache_dir / f"{cache_type}.txt"
    if not cache_file.exists():
        raise FileNotFoundError(f"Cache file for {cache_type} not found.")

    return set(cache_file.read_text().splitlines())
