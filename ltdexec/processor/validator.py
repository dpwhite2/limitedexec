import ast
import re

from .. import config

#==============================================================================#
class SourceValidator(object):
    def __init__(self, dialect):
        self.dialect = dialect
    def __call__(self, source):
        pass

#==============================================================================#
class AstValidator(ast.NodeVisitor):

    def __init__(self, dialect):
        super(AstValidator, self).__init__()
        self.dialect = dialect

    def __call__(self, tree):
        self.visit(tree)

    def check_import_from(self, module, name, asname, level):
        if level > 0:
            raise RuntimeError('TODO')
        if self.dialect.allowed_imports:
            if module not in self.dialect.allowed_imports:
                raise RuntimeError('TODO')
            allowed_froms = self.dialect.allowed_imports[module]
            if allowed_froms and (name not in allowed_froms):
                raise RuntimeError('TODO')
        elif module in self.dialect.forbidden_imports:
            raise RuntimeError('TODO')
        if asname and asname in self.dialect.forbidden_names_set:
            raise RuntimeError('TODO')

    def check_import(self, name, asname):
        if self.dialect.allowed_imports:
            if name not in self.dialect.allowed_imports:
                raise RuntimeError('TODO')
        elif name in self.dialect.forbidden_imports:
            raise RuntimeError('TODO')
        if asname and asname in self.dialect.forbidden_names_set:
            raise RuntimeError('TODO')

    def visit_Name(self, node):
        ctx = node.ctx
        name = node.id
        if name in self.dialect.forbidden_names_set:
            raise RuntimeError('TODO')
        elif (ctx == ast.Store or ctx == ast.AugStore or ctx == ast.Del) and \
              name in self.dialect.unassignable_names_set:
            raise RuntimeError('TODO')
        if self.dialect.no_double_underscore_names and len(name)>1:
            if name[:2]=='__' and name[-2:]=='__':
                raise RuntimeError('TODO')
        self.generic_visit(node)

    def visit_Attribute(self, node):
        ctx = node.ctx
        attr = node.attr
        if attr in self.forbidden_attrs_set:
            raise RuntimeError('TODO')
        elif (ctx == ast.Store or ctx == ast.AugStore or ctx == ast.Del) and \
              attr in self.dialect.unassignable_attrs_set:
            raise RuntimeError('TODO')
        if self.dialect.no_double_underscore_attrs and len(attr)>1:
            if attr[:2]=='__' and attr[-2:]=='__':
                raise RuntimeError('TODO')
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.check_import(node.name, node.asname)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.check_import_from(node.module, alias.name, alias.asname, node.level)
        self.generic_visit(node)


#------------------------------------------------------------------------------#
def make_forbidden_visitor(name, description):
    def func(self, node):
        msg = 'The following is not allowed in this script: {0}.'
        msg = msg.format(description)
        raise RuntimeError(msg)
    func.__name__ = 'visit_' + name
    return func

def create_ast_validator_class(dialect):
    attrs = {}
    for flag, flagtraits in config.flags.node_leafflag_traits.iteritems():
        if getattr(dialect, flag) == False:
            nodetraits = config.nodes.node_traits[flagtraits.node]
            visitor = make_forbidden_visitor(nodetraits.name, nodetraits.description)
            attrs['visit_' + nodetraits.name] = visitor


    return type('AutoAstValidator', (AstValidator,), attrs)

#==============================================================================#



