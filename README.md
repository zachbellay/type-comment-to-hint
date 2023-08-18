# Use com2ann instead!
https://github.com/ilevkivskyi/com2ann

I started working on this before discovering com2ann, that is much more mature so just use that.

## `type-comment-to-annotation`

🚧 Under active development 🚧

Convert your type comments:

```py
def sum_two_number(a, b):
    # type: (int, int) -> int
    return a + b
```

to type annotations (AKA type hints):
```py
def sum_two_number(a: int, b: int) -> int:
    return a + b
```
