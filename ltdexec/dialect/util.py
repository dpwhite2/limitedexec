from .base import Dialect
from .registry import dialects

def get_dialect_object(dialect):
    """ If given a dialect class, or dialect name, returns the associated
        dialect object.  If given a dialect object it simply returns it.
    """
    if isinstance(dialect, type):
        assert issubclass(dialect, Dialect)
        dialect = dialects[dialect.name]
    elif isinstance(dialect, basestring):
        dialect = dialects[dialect]
    assert isinstance(dialect, Dialect)
    return dialect