import re
import sys
from pathlib import Path

VALID_COMMIT_TYPES: tuple[str, ...] = (
    "feat",
    "fix",
    "refactor",
    "docs",
    "test",
    "chore",
    "style",
    "revert",
    "perf",
    "ci",
    "build",
)

commit_regex: str = rf"^({'|'.join(VALID_COMMIT_TYPES)})(\([^()]+\))?(!)?: .+$"


def is_valid_commit_message(commit_message: str) -> bool:
    return bool(re.fullmatch(commit_regex, commit_message))


def main() -> None:
    commit_message_path: Path = Path(sys.argv[1])

    # only check the commit message header, ignore all comments and stuff
    commit_message: str = commit_message_path.read_text().strip().splitlines()[0]

    if not is_valid_commit_message(commit_message):
        print("Invalid commit message!")
        print("Expected commit message to follow Conventional Commits format.")
        print(f"Valid Commit Types: {VALID_COMMIT_TYPES}")
        sys.exit(1)


if __name__ == "__main__":
    main()
