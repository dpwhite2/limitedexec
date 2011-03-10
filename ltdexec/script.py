import sys
from .source import Source


#==============================================================================#
class Result(object):
    def __init__(self):
        self.result = None
        self.exception = None
        self.globals = {}
        self.locals = {}


#==============================================================================#
class Script(object):
    def __init__(self, code, source, dialect):
        assert isinstance(source, Source)
        self.python_version = sys.version_info
        self.code = code
        self.source = source
        self.dialect = dialect
        EnvironmentFactory = self.dialect.environment_factory_class()
        self.env_factory = EnvironmentFactory(self.dialect)

    def run(self, globals=None, locals=None):
        globals = globals or {}
        locals = locals or {}

        with self.env_factory(globals, locals) as env:
            res = Result()
            try:
                res.result = eval(self.code, env.globals, env.locals)
            except Exception:
                # TODO: reraise the exception, or catch it?
                # TODO: set exception info in Result object
                pass
            res.globals = env.globals.copy()
            res.locals = env.locals.copy()

        return res


#==============================================================================#

