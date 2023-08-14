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
