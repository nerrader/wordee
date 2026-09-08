import subprocess
from pathlib import Path


def test_commit_message_accepts_valid_commit_message(tmp_path: Path) -> None:
    message_path = tmp_path / "message"
    message_path.write_text("feat: add new feature")

    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "scripts/hooks/check_commit_message.py",
            message_path,
        ],
        check=False,
    )

    assert result.returncode == 0


def test_commit_message_only_checks_commit_header(
    tmp_path: Path,
) -> None:
    message_path = tmp_path / "message"
    message_path.write_text("feat: add feature\n\nthis is the body")

    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "scripts/hooks/check_commit_message.py",
            message_path,
        ],
        check=False,
    )

    assert result.returncode == 0


def test_commit_message_rejects_not_using_conventional_commits_message(
    tmp_path: Path,
) -> None:
    message_path = tmp_path / "message"
    message_path.write_text("fix something")

    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "scripts/hooks/check_commit_message.py",
            message_path,
        ],
        check=False,
    )

    assert result.returncode == 1


def test_commit_message_rejects_invalid_commit_category(tmp_path: Path) -> None:
    message_path = tmp_path / "message"
    message_path.write_text("ci(CI): something something")

    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "scripts/hooks/check_commit_message.py",
            message_path,
        ],
        check=False,
    )

    assert result.returncode == 1


def test_commit_message_rejects_invalid_commit_scope(tmp_path: Path) -> None:
    message_path = tmp_path / "message"
    message_path.write_text("chore(): something something")

    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "scripts/hooks/check_commit_message.py",
            message_path,
        ],
        check=False,
    )

    assert result.returncode == 1


def test_commit_message_rejects_invalid_commit_description(tmp_path: Path) -> None:
    message_path = tmp_path / "message"
    message_path.write_text("chore(): something something")

    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "scripts/hooks/check_commit_message.py",
            message_path,
        ],
        check=False,
    )

    assert result.returncode == 1
