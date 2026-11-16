# ipselia-sandbox

## Usage

### wordcount

Count lines, words and characters of a file or stdin, like `wc`:

```sh
PYTHONPATH=src python -m wordcount FILE      # count a file
echo "a b" | PYTHONPATH=src python -m wordcount   # count stdin
```

It prints `lines words chars`, where lines is the number of newline characters,
words is the number of whitespace-separated tokens and chars is the total number
of characters. A missing file prints an error on stderr and exits with code 2.

From Python:

```python
from wordcount import count

count("a b\nc\n")  # (2, 3, 6)
```
