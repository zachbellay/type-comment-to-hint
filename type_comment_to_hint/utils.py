import ast

import libcst as cst


def compare_ast_nodes(node1, node2):
    if type(node1) != type(node2):
        return False
    
    if isinstance(node1, ast.AST):
        for field, value1 in ast.iter_fields(node1):
            value2 = getattr(node2, field, None)
            if value1 is None and value2 is None:
                continue
            if not compare_ast_nodes(value1, value2):
                return False
        return True
    elif isinstance(node1, list):
        if len(node1) != len(node2):
            return False
        for item1, item2 in zip(node1, node2):
            if not compare_ast_nodes(item1, item2):
                return False
        return True
    else:
        return node1 == node2


# def compare_ast_nodes(src1, src2):
#     # if not modified_tree.deep_equals(source_tree):
#     # cst.parse_module(type_comment)

#     src1_tree = cst.parse_module(src1)
#     src2_tree = cst.parse_module(src2)

#     return src1_tree.deep_equals(src2_tree)
