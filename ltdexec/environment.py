import uuid
import sys

from . import wrapper
from .dialect import util as dialect_util

#==============================================================================#
class Environment(object):
    """ A script is executed in an Environment.  This contains the globals and
        locals dicts that are available to the script when it begins execution.
    """
    def __init__(self, objects, globals):
        assert isinstance(objects, dict)
        assert isinstance(globals, dict)

        self.metadata = {}
        self.key = wrapper.create_envkey()
        _globals = {}
        try:
            for name, objdef in objects.iteritems():
                _globals[name] = objdef.construct()
                self.metadata[name] = {
                    'id': id(_globals[name]),
                    'method_on_close': objdef.method_on_close,
                    }
        except:
            exc = sys.exc_info()
            for name, obj in _globals.iteritems():
                try:
                    self._close_object(name, obj)
                except:
                    pass
            wrapper.pop_envkey(self.key)
            raise exc[0], exc[1], exc[2]

        _globals.update(globals)

        # locals and globals must refer to the same dict.  Otherwise, 
        # module-scope names are only placed in the locals dict.  In that case, 
        # module-scope names could not be used from within local scopes.
        self.globals = _globals
        self.locals = self.globals
        self.modules = {}
        # TODO: put custom import function into globals

    def _close_object(self, name, obj):
        try:
            obj._LX_unlock(key)
        except AttributeError:
            pass
        finally:
            if name in self.metadata and self.metadata[name]['id']==id(obj):
                getattr(obj, self.metadata[name]['method_on_close'], lambda: None)()
                self.metadata.pop(name)  # pop the metadata so we don't close the same object twice

    def close(self):
        """ Called when a script has completed execution.  Any cleanup required
            by the environment members should be performed during this call.
        """
        key = self.key
        exc = None
        for name, obj in self.globals.iteritems():
            try:
                self._close_object(name, obj)
            except:
                exc = sys.exc_info()
        for name, obj in self.locals.iteritems():
            try:
                self._close_object(name, obj)
            except:
                exc = sys.exc_info()
        wrapper.pop_envkey(key)
        if exc:
            raise exc[0], exc[1], exc[2]


    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def import_(self):
        # TODO: custom import function
        pass


#==============================================================================#
class EnvironmentFactory(object):
    """ A Script contains an EnvironmentFactory, which it uses to construct the
        Environment each time it runs.
    """
    Environment = Environment

    def __init__(self, dialect):
        dialect = dialect_util.get_dialect_object(dialect)
        try:
            self.objects = dialect.objects
        except AttributeError:
            self.objects = {}
        self.objects.update(dialect.builtin_objects)

    def __call__(self, globals=None):
        """ Create an Environment object. """
        globals = globals or {}
        return self.Environment(self.objects, globals)


#==============================================================================#



