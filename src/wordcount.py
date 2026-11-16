"""Count lines, words and characters of a file or stdin, like wc."""

import sys


def count(text):
    """Return (lines, words, chars): newline count, whitespace-separated tokens, total characters."""
    return text.count("\n"), len(text.split()), len(text)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) > 1:
        print("usage: python -m wordcount [FILE]", file=sys.stderr)
        return 2
    if args:
        try:
            with open(args[0], encoding="utf-8", newline="") as f:
                text = f.read()
        except OSError as exc:
            print(f"wordcount: {args[0]}: {exc.strerror}", file=sys.stderr)
            return 2
    else:
        text = sys.stdin.read()
    lines, words, chars = count(text)
    print(f"{lines} {words} {chars}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
