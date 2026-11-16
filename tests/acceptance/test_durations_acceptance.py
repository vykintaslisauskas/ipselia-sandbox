import hashlib
import importlib
import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _parse_duration():
    assert importlib.util.find_spec("durations") is not None, "module durations (src/durations.py) does not exist"
    module = importlib.import_module("durations")
    assert hasattr(module, "parse_duration"), "durations.parse_duration is missing"
    return module.parse_duration


def _assert_seconds(text, expected):
    result = _parse_duration()(text)
    assert type(result) is int
    assert result == expected


def _assert_rejected(text):
    parse_duration = _parse_duration()
    with pytest.raises(ValueError):
        parse_duration(text)


# Valid durations


def test_seconds_only():
    """parse_duration("45s") returns 45 seconds as an int."""
    _assert_seconds("45s", 45)


def test_minutes_only():
    """parse_duration("2m") returns 120 seconds."""
    _assert_seconds("2m", 120)


def test_hours_and_minutes():
    """parse_duration("1h30m") returns 5400 seconds."""
    _assert_seconds("1h30m", 5400)


def test_hours_minutes_and_seconds():
    """parse_duration("1h2m3s") returns 3723 seconds."""
    _assert_seconds("1h2m3s", 3723)


def test_zero_seconds():
    """parse_duration("0s") returns 0 seconds."""
    _assert_seconds("0s", 0)


def test_zero_minutes_unit_allowed():
    """parse_duration("1h0m") returns 3600 seconds."""
    _assert_seconds("1h0m", 3600)


def test_leading_zeros_allowed():
    """parse_duration("007s") returns 7 seconds (leading zeros are allowed)."""
    _assert_seconds("007s", 7)


# Invalid durations


def test_rejects_empty_string():
    """parse_duration("") raises ValueError."""
    _assert_rejected("")


def test_rejects_number_without_unit():
    """parse_duration("10") raises ValueError because the unit is missing."""
    _assert_rejected("10")


def test_rejects_unknown_unit():
    """parse_duration("5x") raises ValueError because x is not a known unit."""
    _assert_rejected("5x")


def test_rejects_wrong_unit_order():
    """parse_duration("1m1h") raises ValueError because units are out of order."""
    _assert_rejected("1m1h")


def test_rejects_repeated_unit():
    """parse_duration("1h1h") raises ValueError because a unit is repeated."""
    _assert_rejected("1h1h")


def test_rejects_leading_space():
    """parse_duration(" 1h") raises ValueError because of the leading space."""
    _assert_rejected(" 1h")


def test_rejects_trailing_space():
    """parse_duration("1h ") raises ValueError because of the trailing space."""
    _assert_rejected("1h ")


def test_rejects_inner_space():
    """parse_duration("1 h") raises ValueError because of the space before the unit."""
    _assert_rejected("1 h")


def test_rejects_minus_sign():
    """parse_duration("-5s") raises ValueError because signs are not allowed."""
    _assert_rejected("-5s")


def test_rejects_plus_sign():
    """parse_duration("+5s") raises ValueError because signs are not allowed."""
    _assert_rejected("+5s")


def test_rejects_decimal_number():
    """parse_duration("1.5h") raises ValueError because decimals are not allowed."""
    _assert_rejected("1.5h")


def test_rejects_unit_without_number():
    """parse_duration("h") raises ValueError because the unit has no number."""
    _assert_rejected("h")


def test_rejects_trailing_number_without_unit():
    """parse_duration("1h30") raises ValueError because the trailing 30 has no unit."""
    _assert_rejected("1h30")


def test_rejects_non_ascii_digit():
    """parse_duration("\u0663s") (Arabic-Indic digit three) raises ValueError."""
    _assert_rejected("\u0663s")


# Scope of the change


UNCHANGED_FILES = {
    "src/sandbox_calc.py": "8a45f82534763c87c8791573d469a6384b70b965ac7f136e5c65ba36ea39070d",
    "pyproject.toml": "6d9a80bfa723d04e9f1432b6f53332afd2d89c514b0a7ab56101747b5e6b20a5",
    "tests/test_sandbox_calc.py": "4627516b7607f4a4a2650cbf93b26576284a49e50eae6b49f520386170abe07e",
    ".github/workflows/tests.yml": "63f5663a41c4b665529cb04ac63306fcb72f27df5f6583954d3354de27293a2a",
}


def test_only_durations_module_added_and_existing_files_unchanged():
    """src/ gains only durations.py, and existing project files are left unchanged."""
    src_files = {
        p.relative_to(REPO_ROOT / "src").as_posix()
        for p in (REPO_ROOT / "src").rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }
    assert src_files == {"sandbox_calc.py", "durations.py"}
    for rel, expected in UNCHANGED_FILES.items():
        digest = hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest()
        assert digest == expected, f"{rel} was changed"
    assert not (REPO_ROOT / "conftest.py").exists()
    assert not (REPO_ROOT / "tests" / "conftest.py").exists()
