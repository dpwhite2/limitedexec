import __builtin__

def _liststr(*args):
    return (' '.join(args)).split()


DEFAULT_FORBIDDEN_BUILTIN_FUNCTIONS = _liststr(
            '__import__ compile delattr dir eval exec execfile file getattr',
            'globals hasattr help input locals open raw_input reload setattr',
            'type vars')

DEFAULT_FORBIDDEN_NAMES = DEFAULT_FORBIDDEN_BUILTIN_FUNCTIONS
DEFAULT_FORBIDDEN_ATTRS = []
DEFAULT_UNASSIGNABLE_NAMES = []
DEFAULT_UNASSIGNABLE_ATTRS = []

ALWAYS_FORBIDDEN_NAMES = []
ALWAYS_FORBIDDEN_ATTRS = []
ALWAYS_UNASSIGNABLE_NAMES = []
ALWAYS_UNASSIGNABLE_ATTRS = []

ALWAYS_ALLOWED_NAMES = _liststr('True False None')

LTDEXEC_PRIVATE_PREFIX = '_LX_'

BUILTIN_NAMES_SET = frozenset(x for x in __builtin__.__dict__.iterkeys())

