


#==============================================================================#
class DialectRegistry(object):
    def __init__(self):
        self.dialects = {}
        
    def register(self, dialect_cls):
        assert isinstance(dialect_cls, type)
        if dialect_cls.name not in self.dialects:
            self.dialects[dialect_cls.name] = dialect_cls()
            
    def unregister(self, name):
        self.dialects.pop(name)
        
    def __getitem__(self, name):
        return self.dialects[name]
        
    def names(self):
        return self.dialects.keys()
        
    def __contains__(self, name):
        return name in self.dialects

#==============================================================================#
dialects = DialectRegistry()

#==============================================================================#
