import sys
import __builtin__

from .source import Source


#==============================================================================#
class Result(object):
    """ The result of executing a Script. """
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

    @property
    def filename(self):
        return self.source.filename

    def run(self, globals=None):
        """ Run the script.  If *globals* is provided, they will
            be merged into the environment's namespace overwriting any object
            with the same name.  The return value is a Result object containing
            information about the script's run.

            Before execution, an Environment will be created using the dialect
            given in the constructor.  It is seperate from any other
            Environment created by a previous or future run.

            If an execption occurs while creating the Environment, it will
            propogate normally from this method.  However, if an exception
            occurs during script execution, it will be caught and saved in the
            Result object.
        """
        globals = globals or {}

        # Exceptions due to initializing the Environment will propogate.  This
        # is expected because such exceptions are *not* due to the script
        # itself.  The source is instead the result of the `objects` attribute
        # of the Dialect.
        with self.env_factory(globals) as env:
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