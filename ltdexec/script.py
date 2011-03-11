import sys
import __builtin__

from .source import Source


#==============================================================================#
class Result(object):
    def __init__(self):
        self.result = None
        self.exception = False
        self.exc_info = (None,None,None)
        self.globals = {}
        self.locals = {}


#==============================================================================#
class Script(object):
    def __init__(self, code, source, dialect):
        from .dialect import util as dialect_util
        assert isinstance(source, Source)
        self.python_version = sys.version_info
        self.code = code
        self.source = source
        self.dialect = dialect_util.get_dialect_object(dialect)
        self.env_factory = self.dialect.EnvironmentFactory(self.dialect)

    def run(self, globals=None, locals=None):
        globals = globals or {}
        locals = locals or {}

        # Exceptions due to initializing the Environment will propogate.  This 
        # is expected because such exceptions are *not* due to the script 
        # itself.  The source is instead the result of the `objects` attribute 
        # of the Dialect.
        with self.env_factory(globals, locals) as env:
            res = Result()
            try:
                # In CPython, if __builtins__ is not in globals, the current
                # globals are copied into the globals dict before executing the
                # expression.  This is not what we want, so we provide
                # __builtins__ ourselves.
                env.globals['__builtins__'] = __builtin__
                res.result = eval(self.code, env.globals, env.locals)
            except:
                # TODO: reraise the exception, or catch it?
                res.exc_info = sys.exc_info()
                res.exception = True

            res.globals = env.globals.copy()
            res.locals = env.locals.copy()

        return res


#==============================================================================#
