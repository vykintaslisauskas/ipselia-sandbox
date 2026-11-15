"""Acceptance tests for src/slugify.py: slugify(text: str) -> str."""

import importlib.util
from pathlib import Path

SLUGIFY_PATH = Path(__file__).resolve().parents[2] / "src" / "slugify.py"


def _load_slugify():
    # Load src/slugify.py by path so an unrelated installed "slugify" package is never used.
    assert SLUGIFY_PATH.is_file(), f"{SLUGIFY_PATH} does not exist yet"
    spec = importlib.util.spec_from_file_location("ipselia_src_slugify", SLUGIFY_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "slugify"), "src/slugify.py does not define slugify()"
    return module.slugify


def test_module_exposes_callable_slugify_returning_str():
    """src/slugify.py exists and its slugify() returns a string."""
    slugify = _load_slugify()
    assert callable(slugify)
    assert isinstance(slugify("abc"), str)


def test_accented_e_becomes_plain_e():
    """An accented 'é' is converted to a plain 'e'."""
    slugify = _load_slugify()
    assert slugify("café") == "cafe"


def test_umlaut_u_becomes_plain_u():
    """An umlaut 'ü' is converted to a plain 'u'."""
    slugify = _load_slugify()
    assert slugify("über") == "uber"


def test_ogonek_a_becomes_plain_a():
    """A Lithuanian 'ą' is converted to a plain 'a'."""
    slugify = _load_slugify()
    assert slugify("ąžuolas") == "azuolas"


def test_uppercase_letters_are_lowercased():
    """Uppercase letters are turned into lowercase."""
    slugify = _load_slugify()
    assert slugify("ABCxyz") == "abcxyz"


def test_digits_are_kept():
    """Digits 0-9 are kept as they are."""
    slugify = _load_slugify()
    assert slugify("route66") == "route66"


def test_single_non_alphanumeric_character_becomes_hyphen():
    """A single character that is not a-z or 0-9 between words becomes one hyphen."""
    slugify = _load_slugify()
    assert slugify("a b") == "a-b"


def test_run_of_mixed_non_alphanumeric_characters_becomes_one_hyphen():
    """A run of several different non a-z/0-9 characters collapses into a single hyphen."""
    slugify = _load_slugify()
    assert slugify("a .,;!?@#$%^&*() b") == "a-b"


def test_leading_and_trailing_hyphens_are_removed():
    """Hyphens at the start and the end of the result are removed."""
    slugify = _load_slugify()
    assert slugify("--abc--") == "abc"


def test_leading_and_trailing_symbols_leave_no_hyphens():
    """Symbols and spaces at the edges of the input do not leave hyphens at the edges."""
    slugify = _load_slugify()
    assert slugify("  ***abc def!!!  ") == "abc-def"


def test_empty_input_returns_empty_string():
    """An empty input returns an empty string."""
    slugify = _load_slugify()
    assert slugify("") == ""


def test_whitespace_and_symbols_only_input_returns_empty_string():
    """An input made only of spaces and symbols returns an empty string."""
    slugify = _load_slugify()
    assert slugify("  -_- @#$ ") == ""


def test_example_hello_world():
    """Example: 'Hello, World!' becomes 'hello-world'."""
    slugify = _load_slugify()
    assert slugify("Hello, World!") == "hello-world"


def test_example_azuolas_didysis():
    """Example: '  Ąžuolas  Didysis ' becomes 'azuolas-didysis'."""
    slugify = _load_slugify()
    assert slugify("  Ąžuolas  Didysis ") == "azuolas-didysis"


def test_example_repeated_hyphens_and_underscores():
    """Example: 'a--b__c' becomes 'a-b-c'."""
    slugify = _load_slugify()
    assert slugify("a--b__c") == "a-b-c"


def test_example_exclamation_marks_only():
    """Example: '!!!' becomes an empty string."""
    slugify = _load_slugify()
    assert slugify("!!!") == ""
