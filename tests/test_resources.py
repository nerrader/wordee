import subprocess
from pathlib import Path

QRC = Path("src/wordee/assets/resources.qrc")
RESOURCES = Path("src/wordee/assets/resources_rc.py")


def test_resources_rc_is_up_to_date(tmp_path: Path) -> None:
    original_rc_file = RESOURCES.read_text()

    result = subprocess.run(
        ["uv", "run", "pyside6-rcc", QRC, "-o", tmp_path / "resources_rc.py"],
        check=False,
    )

    assert result.returncode == 0
    assert original_rc_file == (tmp_path / "resources_rc.py").read_text()
