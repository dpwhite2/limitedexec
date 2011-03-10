"""
ltdexec.processor.validator
===========================

Validator classes verify that the raw source code or abstract syntax tree is
permissible before it is finally compiled to Python byte code.  They signal
errors through exceptions, which may be used to provide an error message.

"""

import ast
import re

from .. import config
from .. import exceptions

#==============================================================================#
def syntax_error(node, msg, reason=None):
    lineno = getattr(node, 'lineno', -1)
    offset = getattr(node, 'col_offset', -1)
    filename = '<unknown>'
    text = '<unknown>'
    raise exceptions.SyntaxError(msg, filename, lineno, offset, text, reason)

#==============================================================================#
class SourceValidator(object):
    """ A SourceValidator verifies the correctness of raw source code. """
    def __init__(self, dialect):
        self.dialect = dialect

    def __call__(self, source):
        """ Perform the validation.

            This default implementation does nothing; it simply returns the
            source unchanged.
        """
        pass

#==============================================================================#
class MinimalAstValidator(ast.NodeVisitor):
    """ The MinimalSourceValidator must be the base class of all abstract
        syntax tree validators. It verifies the few rules that all LimitedExec
        scripts must follow.
    """
    def __init__(self, dialect):
        super(MinimalAstValidator, self).__init__()
        self.dialect = dialect

    def check_name(self, node):
        """ Verifies that a name node does not use a name reserved for use by
            LimitedExec.  Such names begin with ``_LX_``.

            All abstract syntax tree validators **must** call this method,
            directly or indirectly.
        """
        if node.id.startswith(config.names.LTDEXEC_PRIVATE_PREFIX):
            m = 'Names may not begin with "{0}". '
            m += 'This is reserved for library-internal use.'
            m = m.format(config.names.LTDEXEC_PRIVATE_PREFIX)
            syntax_error(node, m, reason='private_prefix_name')

    def check_attribute(self, node):
        """ Verifies that a name node does not use a name reserved for use by
            LimitedExec.  Such names begin with ``_LX_``.

            All abstract syntax tree validators **must** call this method,
            directly or indirectly.
        """
        if node.attr.startswith(config.names.LTDEXEC_PRIVATE_PREFIX):
            m = 'Attributes may not begin with "{0}". '
            m += 'This is reserved for library-internal use.'
            m = m.format(config.names.LTDEXEC_PRIVATE_PREFIX)
            syntax_error(node, m, reason='private_prefix_attr')

    def visit_Name(self, node):
        self.check_name(node)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        self.check_attribute(node)
        self.generic_visit(node)

    def __call__(self, tree):
        """ Perform the validation. """
        self.visit(tree)

#==============================================================================#
class AstValidator(MinimalAstValidator):
    """ Base class of the default abstract syntax tree validator class created
        by a Dialect.

        This class checks that imports, if permitted, only import modules in
        the Dialect's approved list.  It also checks that the names and
        attributes used are permitted.  It also makes sure that names and
        attributes that are the target of an assignment operation are allowed
        to be the result of such an operation.
    """

    def __init__(self, dialect):
        super(AstValidator, self).__init__(dialect)

    def check_import_from(self, node, module, name, asname, level):
        if level > 0:
            syntax_error(node, 'Relative imports are not permitted.',
                         reason='relative_import')

        if self.dialect.allowed_imports:
            if module not in self.dialect.allowed_imports:
                m = 'Cannot import "{0}", it is not among the allowed imports.'
                m = m.format(module)
                syntax_error(node, m, reason='not_in_allowed_imports')
            allowed_froms = self.dialect.allowed_imports[module]
            if allowed_froms and (name not in allowed_froms):
                m = 'Importing "{0}" from "{1}" is not permitted.'
                m = m.format(name, module)
                syntax_error(node, m, reason='not_in_allowed_imports_froms')

        elif module in self.dialect.forbidden_imports:
            m = 'Importing of "{0}" is not permitted.'.format(module)
            syntax_error(node, m, reason='forbidden_import')

        if ((name in self.dialect.forbidden_names_set) or
           (asname and asname in self.dialect.forbidden_names_set)):
            m = 'Cannot import as "{0}", it is a forbidden name.'.format(asname)
            syntax_error(node, m, reason='import_forbidden_name')

    def check_import(self, node, name, asname):
        if self.dialect.allowed_imports:
            if name not in self.dialect.allowed_imports:
                m = 'Cannot import "{0}", it is not among the allowed imports.'
                m = m.format(name)
                syntax_error(node, m, reason='not_in_allowed_imports')

        elif name in self.dialect.forbidden_imports:
            m = 'Importing of "{0}" is not permitted.'.format(name)
            syntax_error(node, m, reason='forbidden_import')

        if ((name in self.dialect.forbidden_names_set) or
           (asname and asname in self.dialect.forbidden_names_set)):
            m = 'Cannot import as "{0}", it is a forbidden name.'.format(asname)
            syntax_error(node, m, reason='import_forbidden_name')

    def check_name(self, node):
        super(AstValidator, self).check_name(node)
        ctx = node.ctx
        name = node.id
        if name in self.dialect.forbidden_names_set:
            m = 'Use of the name "{0}" is forbidden.'.format(name)
            syntax_error(node, m, reason='forbidden_name')

        elif (ctx == ast.Store or ctx == ast.AugStore or ctx == ast.Del) and \
              name in self.dialect.unassignable_names_set:
            m = 'The name "{0}" may not be assigned to.'.format(name)
            syntax_error(node, m, reason='unassignable_name')

        if self.dialect.no_double_underscore_names and len(name)>1:
            if name[:2]=='__' and name[-2:]=='__':
                m = 'Use of the name "{0}" is forbidden--'
                m += 'it starts and ends with double underscores.'
                m = m.format(name)
                syntax_error(node, m, reason='double_underscore_name')


    def check_attribute(self, node):
        super(AstValidator, self).check_attribute(node)
        ctx = node.ctx
        attr = node.attr
        if attr in self.dialect.forbidden_attrs_set:
            m = 'Use of the attribute "{0}" is forbidden.'.format(attr)
            syntax_error(node, m, reason='forbidden_attr')

        elif (ctx == ast.Store or ctx == ast.AugStore or ctx == ast.Del) and \
              attr in self.dialect.unassignable_attrs_set:
            m = 'The attribute "{0}" may not be assigned to.'.format(attr)
            syntax_error(node, m, reason='unassignable_attr')

        if self.dialect.no_double_underscore_attrs and len(attr)>1:
            if attr[:2]=='__' and attr[-2:]=='__':
                m = 'Use of the attribute "{0}" is forbidden--'
                m += 'it starts and ends with double underscores.'
                m = m.format(attr)
                syntax_error(node, m, reason='double_underscore_attr')

        if isinstance(node.value, ast.Name) and \
           node.value.id in config.names.BUILTIN_NAMES_SET:
            m = 'Attributes of builtins may not be accessed.'
            syntax_error(node, m)


    def visit_Name(self, node):
        self.check_name(node)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        self.check_attribute(node)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.check_import(node, alias.name, alias.asname)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.check_import_from(node, node.module, alias.name, alias.asname,
                                   node.level)
        self.generic_visit(node)


#------------------------------------------------------------------------------#
def make_forbidden_visitor(name, description):
    def func(self, node):
        msg = 'The following is not allowed in this script: {0}.'
        msg = msg.format(description)
        syntax_error(node, msg, reason='node_'+name)
    func.__name__ = 'visit_' + name
    return func

def create_ast_validator_class(dialect):
    """ Create an abstract syntax tree validator class using the given
        dialect.

        By default, a Dialect uses this function to create an ast validator.
        The validator produced will have AstValdiator as a base class.
    """
    attrs = {}
    for flag, flagtraits in config.flags.node_leafflag_traits.iteritems():
        if getattr(dialect, flag) == False:
            nodetraits = config.nodes.node_traits[flagtraits.node]
            visitor = make_forbidden_visitor(nodetraits.name,
                                             nodetraits.description)
            attrs['visit_' + nodetraits.name] = visitor


    return type('AutoAstValidator', (AstValidator,), attrs)

#==============================================================================#
