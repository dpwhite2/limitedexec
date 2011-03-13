from collections import namedtuple
import itertools

#==============================================================================#
_flag_hierarchy = {
    'allow_statements': {
        'allow_statements_non_expressions': {
            'allow_statements_definitions': {
                'allow_statement_def': None,
                'allow_statement_class': None,
            },
            'allow_statements_imports': {
                'allow_statement_import': None,
                'allow_statement_import_from': None,
            },
            'allow_statements_assignments': {
                'allow_statement_assignment': None,
                'allow_statement_augmented_assignment': None,
            },
            'allow_statements_loops': {
                'allow_statement_for': None,
                'allow_statement_while': None,
            },
            'allow_statements_exceptions': {
                'allow_statements_try_statements': {
                    'allow_statement_try_finally': None,
                    'allow_statement_try_except': None,
                },
                'allow_statement_raise': None,
            },
            'allow_statement_exec': None,
            'allow_statement_assert': None,
            'allow_statement_global': None,
            'allow_statement_nonlocal': None,
            'allow_statement_del': None,

            'allow_statement_if': None,
            'allow_statement_with': None,
            'allow_statement_print': None,
            'allow_statement_pass': None,
            'allow_statement_break': None,
            'allow_statement_continue': None,
            'allow_statement_return': None,
        },
    },
    'allow_expression_yield': None,
    'allow_expression_lambda': None,
}

non_leaf_flags = set()

def _compute_flag_parents_dict():
    global non_leaf_flags
    parents = {}
    def _inner(dct, flagpath):
        for flag, children in dct.iteritems():
            if children is not None:
                non_leaf_flags.add(flag)
                _inner(children, flagpath+(flag,))
            else:
                parents[flag] = flagpath

    _inner(_flag_hierarchy, () )
    return parents

flag_parents = _compute_flag_parents_dict()

#==============================================================================#
NodeTraits = namedtuple('NodeTraits','name default node category')

class StmtTraits(NodeTraits):
    def __new__(cls, name, default, node):
        category = 'statement'
        return super(StmtTraits, cls).__new__(cls, name, default, node,
                                              category)
class ExprTraits(NodeTraits):
    def __new__(cls, name, default, node):
        category = 'expression'
        return super(ExprTraits, cls).__new__(cls, name, default, node,
                                              category)
BuiltinTraits = namedtuple('BuiltinTraits','name default builtin_name category')
class BuiltinTraits(BuiltinTraits):
    def __new__(cls, name, default, builtin_name):
        return super(BuiltinTraits, cls).__new__(cls, name, default,
                                                 builtin_name, 'builtin')

ModuleTraits = namedtuple('ModuleTraits','name default module_name category')
class ModuleTraits(ModuleTraits):
    def __new__(cls, name, default, module_name):
        return super(ModuleTraits, cls).__new__(cls, name, default,
                                                module_name, 'module')

AttributeTraits = namedtuple('AttributeTraits',
                             'name default attr_name category')
class AttributeTraits(AttributeTraits):
    def __new__(cls, name, default, attr_name):
        return super(AttributeTraits, cls).__new__(cls, name, default,
                                                   attr_name, 'attribute')

MiscTraits = namedtuple('MiscTraits','name default')

T = StmtTraits
statement_leafflag_traits = [
    T('allow_statement_def', True, 'FunctionDef'),
    T('allow_statement_class', True, 'ClassDef'),
    T('allow_statement_import', False, 'Import'),
    T('allow_statement_import_from', False, 'ImportFrom'),
    T('allow_statement_assignment', True, 'Assign'),
    T('allow_statement_augmented_assignment', True, 'AugAssign'),
    T('allow_statement_for', True, 'For'),
    T('allow_statement_while', True, 'While'),
    T('allow_statement_try_finally', True, 'TryFinally'),
    T('allow_statement_try_except', True, 'TryExcept'),
    T('allow_statement_raise', True, 'Raise'),
    T('allow_statement_exec', False, 'Exec'),
    T('allow_statement_assert', True, 'Assert'),
    T('allow_statement_global', True, 'Global'),
    T('allow_statement_nonlocal', True, 'Nonlocal'),
    T('allow_statement_del', False, 'Delete'),

    T('allow_statement_if', True, 'If'),
    T('allow_statement_with', True, 'With'),
    T('allow_statement_print', True, 'Print'),
    T('allow_statement_pass', True, 'Pass'),
    T('allow_statement_break', True, 'Break'),
    T('allow_statement_continue', True, 'Continue'),
    T('allow_statement_return', True, 'Return'),
]
statement_leafflag_traits = dict((t.name, t) for t in statement_leafflag_traits)

T = ExprTraits
expression_leafflag_traits = [
    T('allow_expression_yield', True, 'Yield'),
    T('allow_expression_lambda', True, 'Lambda'),
]
expression_leafflag_traits = dict((t.name, t)
                                  for t in expression_leafflag_traits)
node_leafflag_traits = statement_leafflag_traits.copy()
node_leafflag_traits.update(expression_leafflag_traits)

T = BuiltinTraits
builtin_leafflag_traits = [
    T('allow_builtin_type', False, 'type'),
    T('allow_builtin_open', False, 'open'),
    T('allow_builtin_file', False, 'file'),
    T('allow_builtin_eval', False, 'eval'),
    T('allow_builtin_execfile', False, 'execfile'),
    T('allow_builtin_exec', False, 'exec'),
    T('allow_builtin_compile', False, 'compile'),
    T('allow_builtin_reload', False, 'reload'),
    T('allow_builtin_import', False, '__import__'),
    T('allow_builtin_globals', False, 'globals'),
    T('allow_builtin_locals', False, 'locals'),
]
builtin_leafflag_traits = dict((t.name, t) for t in builtin_leafflag_traits)

T = ModuleTraits
module_leafflag_traits = [
    T('allow_module_os', False, 'os'),
    T('allow_module_sys', False, 'sys'),
    T('allow_module_builtin', False, '__builtin__'),
]
module_leafflag_traits = dict((t.name, t) for t in module_leafflag_traits)

T = AttributeTraits
attribute_leafflag_traits = [
    T('allow_attribute_class', False, '__class__'),
    T('allow_attribute_name', True, '__name__'),
    T('allow_attribute_dict', False, '__dict__'),
    T('allow_attribute_bases', False, '__bases__'),
    T('allow_attribute_mro', False, '__mro__'),
    T('allow_attribute_module', False, '__module__'),
    T('allow_attribute_file', False, '__file__'),
    # The following are actually methods.
    T('allow_attribute_new', True, '__new__'),
    T('allow_attribute_init', True, '__init__'),
    T('allow_attribute_del', False, '__del__'),
    T('allow_attribute_getattr', False, '__getattr__'),
    T('allow_attribute_setattr', False, '__setattr__'),
    T('allow_attribute_delattr', False, '__delattr__'),
    T('allow_attribute_getattribute', False, '__getattribute__'),
    T('allow_attribute_get', False, '__get__'),
    T('allow_attribute_set', False, '__set__'),
    T('allow_attribute_delete', False, '__delete__'),
    T('allow_attribute_getitem', True, '__getitem__'),
    T('allow_attribute_setitem', True, '__setitem__'),
    T('allow_attribute_delitem', False, '__delitem__'),
    T('allow_attribute_getslice', True, '__getslice__'),
    T('allow_attribute_setslice', True, '__setslice__'),
    T('allow_attribute_delslice', False, '__delslice__'),
]
attribute_leafflag_traits = dict((t.name, t) for t in attribute_leafflag_traits)

T = MiscTraits
misc_leafflag_traits = [
    T('no_double_underscore_names', False),
    T('no_double_underscore_attrs', False),
]
misc_leafflag_traits = dict((t.name, t) for t in misc_leafflag_traits)

#==============================================================================#
class Traits(namedtuple('Traits','name parents default category')):
    def __new__(cls, other):
        name = other.name
        assert name not in non_leaf_flags  # only leaf flags have traits
        parents = flag_parents.get(name, ())
        default = other.default
        category = getattr(other, 'category', None)
        return super(Traits, cls).__new__(cls, name, parents, default, category)

allothers = [statement_leafflag_traits.values(),
             expression_leafflag_traits.values(),
             builtin_leafflag_traits.values(),
             module_leafflag_traits.values(),
             attribute_leafflag_traits.values(),
             misc_leafflag_traits.values() ]

leafflag_traits = [Traits(traits) for traits in itertools.chain(*allothers)]
leafflag_traits = dict((t.name, t) for t in leafflag_traits)

del allothers
del T

#==============================================================================#