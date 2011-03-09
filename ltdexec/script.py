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
    def __init__(self, code, source, envrionment_factory):
        assert isinstance(source, Source)
        self.code = code
        self.source = source
        self.env_factory = envrionment_factory
        self.python_version = sys.version_info

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

