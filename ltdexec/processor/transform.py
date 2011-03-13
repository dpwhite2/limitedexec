"""
ltdexec.processor.transform
===========================

Transform classes modify the raw source code or the abstract syntax tree before
it has been compiled.

"""

import ast

#==============================================================================#
class TransformBase(object):
    def __init__(self, dialect):
        self.dialect = dialect

    def precheck_transform(self, data):
        return data

    def postcheck_transform(self, data):
        return data

#==============================================================================#
class SourceTransform(TransformBase):
    pass

class AstTransform(TransformBase):
    # TODO: replace imports with custom import function
    def postcheck_transform(self, tree):
        return TransformImportsAst().visit(tree)

class MergedAstTransform(TransformBase):
    pass

#==============================================================================#
class TransformImportsAst(ast.NodeTransformer):
    def visit_Import(self, node):
        exprs = []
        for alias in node.names:
            modname = alias.name
            asname = alias.asname
            func = ast.Name(id='_LX_import_module', ctx=ast.Load())
            args = [ast.Str(s=modname)]
            if asname:
                keywords = [ast.keyword(arg='asname', value=ast.Str(s=asname))]
            else:
                keywords = []
            call = ast.Call(func=func, args=args, keywords=keywords, starargs=None, kwargs=None)
            expr = ast.Expr(value=call)
            expr = ast.copy_location(expr, node)
            ast.fix_missing_locations(expr)
            exprs.append(expr)
        return exprs
    
    def visit_ImportFrom(self, node):
        assert node.level == 0
        none = ast.Name(id='None', ctx=ast.Load())
        modname = node.module
        froms = []
        for alias in node.names:
            name = ast.Str(s=alias.name)
            asname = ast.Str(s=alias.asname) if alias.asname else none
            pair = ast.Tuple(elts=[name,asname], ctx=ast.Load())
            froms.append(pair)
        froms = ast.List(elts=froms, ctx=ast.Load())
        func = ast.Name(id='_LX_import_module', ctx=ast.Load())
        args = [ast.Str(s=modname)]
        keywords = [ast.keyword(arg='froms', value=froms)]
        call = ast.Call(func=func, args=args, keywords=keywords, starargs=None, kwargs=None)
        expr = ast.Expr(value=call)
        expr = ast.copy_location(expr, node)
        ast.fix_missing_locations(expr)
        return [expr]
        

















