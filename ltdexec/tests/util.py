

#==============================================================================#
class TestObj(object):
    initialized = False
    closed = False
    instances = {}
    def __init__(self, name=None):
        self.name = name
        self.initialized = True
        self.add_instance(name, self)

    def close(self):
        self.closed = True

    @classmethod
    def clear_instances(cls):
        cls.instances = {}
    @classmethod
    def add_instance(cls, name, obj):
        cls.instances[name] = obj

#------------------------------------------------------------------------------#
class ThrowingTestObj(TestObj):
    def __init__(self, name=None):
        self.add_instance(name, self)
        raise RuntimeError('ThrowingTestObj')

#------------------------------------------------------------------------------#
class ThrowsOnClose(TestObj):
    def close(self):
        raise RuntimeError('ThrowsOnClose')

#==============================================================================#
