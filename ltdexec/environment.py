import uuid

from . import wrapper

#==============================================================================#
class Environment(object):
    """ A script is executed in an Environment.  This contains the globals and 
        locals dicts that are available to the script when it begins execution. 
    """
    def __init__(self, objects, globals, locals):
        self.key = wrapper.create_envkey()
        try:
            _globals = {}
            for name, objdef in objects.iteritems():
                _globals[name] = objdef.construct()
            _globals.update(globals)

            self.globals = _globals
            self.locals = locals
            self.modules = {}
        except:
            wrapper.pop_envkey(self.key)
            raise
        # TODO: put custom import function into globals

    def close(self):
        key = self.key
        try:
            for name, obj in self.globals:
                try:
                    obj._LX_unlock(key)
                except AttributeError:
                    pass
        finally:
            wrapper.pop_envkey(key)


    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def import_(self):
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
        return self.Environment(self.objects, globals, locals)


#==============================================================================#




