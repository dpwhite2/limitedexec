


#==============================================================================#
class DialectRegistry(object):
    def __init__(self):
        self.dialects = {}
        self.dialect_classes = {}

    def register(self, dialect_cls):
        assert isinstance(dialect_cls, type)
        name = dialect_cls.name
        if name not in self.dialect_classes and name not in self.dialects:
            self.dialect_classes[name] = dialect_cls

    def unregister(self, name):
        self.dialects.pop(name, None)
        self.dialect_classes.pop(name)

    def __getitem__(self, name):
        try:
            return self.dialects[name]
        except KeyError:
            self.dialects[name] = self.dialect_classes[name]._construct()
            return self.dialects[name]
            
    def get_class(self, name):
        return self.dialect_classes[name]

    def names(self):
        return self.dialect_classes.keys()

    def __contains__(self, name):
        return name in self.dialect_classes

#==============================================================================#
dialects = DialectRegistry()

#==============================================================================#