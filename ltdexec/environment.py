


class Environment(object):
    def __init__(self, dialect):
        self.globals = {}
        self.locals = {}
        self.modules = {}

    def import_(self):
        pass


class EnvironmentFactory(object):
    Environment = Environment

    def __init__(self, dialect):
        pass

    def create_environment(self, globals, locals):
        self.Environment()
