import ast
import re
from typing import Optional

#         return updated_node.with_changes(params=new_params, returns=new_returns)
import libcst as cst
from libcst import RemovalSentinel
from libcst._nodes.whitespace import Comment

# class FunctionTypeCommentTransformer(cst.CSTTransformer):
#     def __init__(self):
#         self.type_comment = None

#     def visit_Comment(self, node: cst.Comment) -> None:
#         type_comment_match = re.match(r"#\s*type:\s*\((.*)\)\s*->\s*(.*)", node.value)
#         if type_comment_match:
#             self.type_comment = type_comment_match.groups()   
   

#     def leave_FunctionDef(
#         self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
#     ) -> cst.FunctionDef:
#         if not self.type_comment:
#             return updated_node

#         param_types, return_type = self.type_comment
#         param_types = [cst.parse_expression(t.strip()) for t in param_types.split(",")]
#         param_annotations = [cst.Annotation(annotation=t) for t in param_types]

#         new_params = [p.with_changes(annotation=a) for p, a in zip(updated_node.params.params, param_annotations)]
#         new_params = cst.Parameters(params=new_params)

#         new_returns = cst.Annotation(cst.Name(return_type.strip()))

#         self.type_comment = None # Clear the comment for the next function


class FunctionTypeCommentTransformer(cst.CSTTransformer):
    def __init__(self):
        self.type_comment = None

    def visit_Comment(self, node: cst.Comment) -> None:
        type_comment_match = re.match(r"#\s*type:\s*\((.*)\)\s*->\s*(.*)", node.value)
        if type_comment_match:
            self.type_comment = type_comment_match.groups()   
   
    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        if not self.type_comment:
            return updated_node

        param_types, return_type = self.type_comment

        # Handle type comment such as 
        # # type: (...) -> int
        # but ignore the params
        if param_types.split(',')[0].strip() == '...':
            new_returns = cst.Annotation(annotation=cst.parse_expression(return_type.strip()))
            return updated_node.with_changes(returns=new_returns)

        param_types = [cst.parse_expression(t.strip()) for t in param_types.split(",")]
        param_annotations = [cst.Annotation(annotation=t) for t in param_types]

        new_params = []
        for param, annotation in zip(updated_node.params.params, param_annotations):
            param = param.with_changes(annotation=annotation)
            new_params.append(param)

        new_params = cst.Parameters(params=new_params)

        new_returns = cst.Annotation(annotation=cst.parse_expression(return_type.strip()))

        self.type_comment = None # Clear the comment for the next function

        return updated_node.with_changes(params=new_params, returns=new_returns)

class FunctionParamTypeCommentTransformer(cst.CSTTransformer):
    def __init__(self):
        self.type_comments = []

    def visit_Comment(self, node: cst.Comment) -> None:
        type_comment_match = re.match(r"#\s*type:\s*([^\(]*?)\s*$", node.value)

        # TODO: generalize this to something like 
        # def t(a # type: List[Dict[str, int]])
        if type_comment_match:
            self.type_comments.append(cst.parse_expression(type_comment_match.group(1).strip()))
   
    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        if not self.type_comments:
            return updated_node

        param_annotations = [cst.Annotation(annotation=t) for t in self.type_comments]                

        new_params = []
        for param, annotation in zip(updated_node.params.params, param_annotations):
            param = param.with_changes(annotation=annotation)
            new_params.append(param)

        new_params = cst.Parameters(params=new_params)

        self.type_comments = [] # Clear the comment for the next function
        return updated_node.with_changes(params=new_params)



class AssignTypeCommentTransformer(cst.CSTTransformer):
    def __init__(self):
        self.pending_assignment: Optional[cst.Assign] = None

    def leave_Assign(self, original_node: cst.Assign, updated_node: cst.Assign) -> cst.Assign:
        self.pending_assignment = original_node
        return updated_node

    def visit_Comment(self, node: cst.Comment) -> None:
        # Check if the comment is a type comment
        type_comment_match = re.match(r"#\s*type:\s*(.*?)\s*$", node.value)
        if type_comment_match and self.pending_assignment:
            # Parse the type comment into an annotation
            annotation = cst.Annotation(annotation=cst.parse_expression(type_comment_match.group(1).strip()))
            target = self.pending_assignment.targets[0].target
            value = self.pending_assignment.value

            # Create the new annotated assignment
            new_assign = cst.AnnAssign(target=target, annotation=annotation, value=value)

            # Replace the original assignment and comment with the annotated assignment
            self.pending_assignment = new_assign

    def leave_SimpleStatementLine(self, original_node: cst.SimpleStatementLine, updated_node: cst.SimpleStatementLine) -> cst.CSTNode:
        if self.pending_assignment:
            new_body = [self.pending_assignment if isinstance(item, cst.Assign) else item for item in updated_node.body]
            self.pending_assignment = None
            return updated_node.with_changes(body=new_body)

        return updated_node


class RemoveTypeCommentTransformer(cst.CSTTransformer):

    def leave_Comment(self, original_node: Comment, updated_node: Comment) -> Comment:
        if re.match(r"#\s*type:\s*(.*?)\s*$", updated_node.value):
            return RemovalSentinel.REMOVE

        return updated_node

def transform(type_comment: str) -> str:
    source_tree = cst.parse_module(type_comment)
    transformers =[
        FunctionTypeCommentTransformer(),
        FunctionParamTypeCommentTransformer(),
        AssignTypeCommentTransformer(),
        RemoveTypeCommentTransformer(),
    ]

    for transformer in transformers:
        source_tree = source_tree.visit(transformer)
    return source_tree.code

