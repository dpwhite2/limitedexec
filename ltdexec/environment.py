import uuid
import sys

from . import wrapper

#==============================================================================#
class Environment(object):
    """ A script is executed in an Environment.  This contains the globals and 
        locals dicts that are available to the script when it begins execution. 
    """
    def __init__(self, objects, globals, locals):
        self.key = wrapper.create_envkey()
        self.metadata = {}
        try:
            _globals = {}
            for name, objdef in objects.iteritems():
                _globals[name] = objdef.construct()
                self.metadata[name] = {
                    'method_on_close': objdef.method_on_close,
                    }
            _globals.update(globals)

            self.globals = _globals
            self.locals = locals
            self.modules = {}
        except:
            wrapper.pop_envkey(self.key)
            raise
        # TODO: put custom import function into globals
        
    def _close_object(self, name, obj):
        try:
            obj._LX_unlock(key)
        except AttributeError:
            pass
        finally:
            if name in self.metadata:
                getattr(obj, self.metadata[name]['method_on_close'], lambda: None)()

    def close(self):
        """ Called when a script has completed execution.  Any cleanup required 
            by the environment members should be performed during this call. 
        """
        key = self.key
        exc = None
        for name, obj in self.globals:
            try:
                self._close_object(name, obj)
            except:
                excinfo = sys.exc_info()
        if excinfo:
            raise exc[0], exc[1], exc[2]


    def __enter__(self):
        pass
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
        try:
            self.objects = dialect.objects
        except AttributeError:
            self.objects = {}
        self.objects.update(dialect.builtins)

    def __call__(self, globals, locals):
        """ Create an Environment object. """
        return self.Environment(self.objects, globals, locals)


#==============================================================================#




