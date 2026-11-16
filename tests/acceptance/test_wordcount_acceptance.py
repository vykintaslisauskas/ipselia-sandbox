import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"


def _run_wordcount(args, cwd, stdin_text=None):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_DIR)
    return subprocess.run(
        [sys.executable, "-m", "wordcount", *args],
        input=stdin_text,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
        timeout=30,
    )


def test_count_empty_text_is_all_zero():
    """count("") returns (0, 0, 0)."""
    try:
        from wordcount import count
    except ImportError as exc:
        pytest.fail(f"wordcount.count is not importable: {exc}")
    assert count("") == (0, 0, 0)


def test_count_lines_words_chars():
    """count("a b\\nc\\n") returns (2, 3, 6): 2 newlines, 3 words, 6 characters."""
    try:
        from wordcount import count
    except ImportError as exc:
        pytest.fail(f"wordcount.count is not importable: {exc}")
    assert count("a b\nc\n") == (2, 3, 6)


def test_cli_file_argument_prints_counts(tmp_path):
    """`python -m wordcount FILE` prints "lines words chars" for that file."""
    target = tmp_path / "sample.txt"
    target.write_bytes(b"hello world\nfoo bar baz\n")
    result = _run_wordcount([str(target)], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "2 5 24"


def test_cli_stdin_prints_counts(tmp_path):
    """`python -m wordcount` with no FILE reads stdin and prints "lines words chars"."""
    result = _run_wordcount([], cwd=tmp_path, stdin_text="one two three\nfour\n")
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "2 4 19"


def test_cli_missing_file_exits_2_with_stderr_message(tmp_path):
    """A missing FILE makes `python -m wordcount` exit with code 2 and print an error on stderr."""
    missing = tmp_path / "does_not_exist.txt"
    result = _run_wordcount([str(missing)], cwd=tmp_path)
    assert result.returncode == 2, (result.returncode, result.stderr)
    assert result.stderr.strip() != ""


def test_readme_has_usage_section():
    """README.md has a "Usage" heading and documents wordcount."""
    readme = REPO_ROOT / "README.md"
    assert readme.is_file(), "README.md does not exist"
    text = readme.read_text(encoding="utf-8")
    assert re.search(r"^#+\s*usage\b", text, re.IGNORECASE | re.MULTILINE), "no Usage heading"
    assert "wordcount" in text
