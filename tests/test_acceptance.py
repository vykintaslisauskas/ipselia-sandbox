"""OWNER acceptance tests for the Wordcount CLI goal (written by the OWNER, never by the coding agent).

The import is inside the test on purpose: until src/wordcount.py exists only these tests fail,
and the rest of the suite still runs.
"""
import os
import subprocess
import sys
from pathlib import Path

SRC = str(Path(__file__).resolve().parents[1] / "src")


def run(args, stdin=None):
    env = {**os.environ, "PYTHONPATH": SRC}
    return subprocess.run([sys.executable, "-m", "wordcount", *args],
                          input=stdin, capture_output=True, text=True, env=env)


def test_count_function():
    from wordcount import count

    assert count("a b\nc") == (1, 3, 5)


def test_empty_file(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("")
    r = run([str(f)])
    assert r.returncode == 0 and r.stdout.strip() == "0 0 0"


def test_multiline_file(tmp_path):
    f = tmp_path / "multi.txt"
    f.write_text("hello world\nfoo bar baz\n")
    r = run([str(f)])
    assert r.returncode == 0 and r.stdout.strip() == "2 5 24"


def test_stdin():
    r = run([], stdin="one two\n")
    assert r.returncode == 0 and r.stdout.strip() == "1 2 8"


def test_missing_file(tmp_path):
    r = run([str(tmp_path / "nope.txt")])
    assert r.returncode == 2 and r.stderr.strip() != ""
