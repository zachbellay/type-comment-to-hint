import ast
from type_comment_to_hint.transformers import TypeCommentToAnnotationTransformer
import pytest
from type_comment_to_hint.utils import compare_ast_nodes
import libcst as cst

def test_conversion_1():
    type_comment="""
def sum_two_number(a, b):
    # type: (int, int) -> int
    return a + b
"""

    type_annotation="""
def sum_two_number(a: int, b: int) -> int:
    return a + b
"""

    source_tree = cst.parse_module(type_comment)
    transformer = TypeCommentToAnnotationTransformer()
    modified_tree = source_tree.visit(transformer)

    assert compare_ast_nodes(ast.parse(modified_tree.code), ast.parse(type_annotation))

def test_conversion_2():
    type_comment="""
def sum_two_number(a, b):
    # type: (int, List[int]) -> int
    return a + b
"""

    type_annotation="""
def sum_two_number(a: int, b: List[int]) -> int:
    return a + b
"""

    source_tree = cst.parse_module(type_comment)
    transformer = TypeCommentToAnnotationTransformer()
    modified_tree = source_tree.visit(transformer)

    assert compare_ast_nodes(ast.parse(modified_tree.code), ast.parse(type_annotation))
