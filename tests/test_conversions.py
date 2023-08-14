import ast

import libcst as cst
import pytest

from type_comment_to_hint.transformers import transform
from type_comment_to_hint.utils import compare_ast_nodes


def test_conversion_1():
    type_comment = """
def sum_two_number(a, b):
    # type: (int, int) -> int
    return a + b
"""

    type_annotation = """
def sum_two_number(a: int, b: int) -> int:
    return a + b
"""

    transformed = transform(type_comment)

    print(transformed)
    print("=" * 20)
    print(type_annotation)

    assert compare_ast_nodes(ast.parse(transformed), ast.parse(type_annotation))


def test_conversion_2():
    type_comment = """
def sum_num_and_list(a, b):
    # type: (int, List[int]) -> int
    sum = 0
    for i in b:
        sum += i
    return a + sum
"""

    type_annotation = """
def sum_num_and_list(a: int, b: List[int]) -> int:
    sum = 0
    for i in b:
        sum += i
    return a + sum
"""

    transformed = transform(type_comment)

    print(transformed)
    print("=" * 20)
    print(type_annotation)

    assert compare_ast_nodes(ast.parse(transformed), ast.parse(type_annotation))


def test_conversion_3():
    type_comment = """
def sum_num_and_list(a, b): # type: (int, List[int]) -> int
    sum = 0
    for i in b:
        sum += i
    return a + sum

def test(a,b):
    pass
"""
    type_annotation = """
def sum_num_and_list(a: int, b: List[int]) -> int:
    sum = 0
    for i in b:
        sum += i
    return a + sum

def test(a,b):
    pass
"""

    transformed = transform(type_comment)

    print(transformed)
    print("=" * 20)
    print(type_annotation)

    assert compare_ast_nodes(ast.parse(transformed), ast.parse(type_annotation))


def test_conversion_4():
    type_comment = """
my_variable = 42 # type: int
"""

    type_annotation = """
my_variable: int = 42
"""

    transformed = transform(type_comment)

    print(transformed)
    print("=" * 20)
    print(type_annotation)

    assert compare_ast_nodes(ast.parse(transformed), ast.parse(type_annotation))


def test_conversion_5():
    type_comment = """
def sum_two_number(
    a, # type: int
    b, # type: int
):
    # type: (...) -> int
    return a + b
"""

    type_annotation = """
def sum_two_number(a: int, b: int) -> int:
    return a + b
"""

    transformed = transform(type_comment)

    print(transformed)
    print("=" * 20)
    print(type_annotation)

    assert compare_ast_nodes(ast.parse(transformed), ast.parse(type_annotation))
