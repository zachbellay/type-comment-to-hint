import ast
import libcst as cst
import re
from libcst import RemovalSentinel


class TypeCommentToAnnotationTransformer(cst.CSTTransformer):
    def __init__(self):
        self.type_comment = None

    def visit_Comment(self, node: cst.Comment) -> None:
        type_comment_match = re.match(r"#\s*type:\s*\((.*)\)\s*->\s*(.*)", node.value)
        if type_comment_match:
            self.type_comment = type_comment_match.groups()   
   

    def leave_Comment(self, original_node: cst.Comment, updated_node: cst.Comment) -> cst.CSTNode:
        if re.match(r"#\s*type:", original_node.value):
            # Return REMOVE to remove the comment node
            return RemovalSentinel.REMOVE
        return updated_node

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        if not self.type_comment:
            return updated_node

        param_types, return_type = self.type_comment
        param_types = [cst.Annotation(cst.Name(t.strip())) for t in param_types.split(",")]

        new_params = [p.with_changes(annotation=a) for p, a in zip(updated_node.params.params, param_types)]
        new_params = cst.Parameters(params=new_params)

        new_returns = cst.Annotation(cst.Name(return_type.strip()))

        self.type_comment = None # Clear the comment for the next function

        return updated_node.with_changes(params=new_params, returns=new_returns)
