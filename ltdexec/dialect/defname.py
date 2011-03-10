
#==============================================================================#
# The following are used when defining what objects appear in a Dialect's 
# namespace.

class defname(object):
    def __init__(self, callable, args=None, kwargs=None, method_on_close=None):
        self.callable = callable
        self.args = args or []
        self.kwargs = kwargs or {}
        self.method_on_close = method_on_close
        
    def construct(self):
        return self.callable(*self.args, **self.kwargs)
    

def wrap_function(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return _wrapper
    

class deffunc(defname):
    def __init__(self, function):
        super(deffunc, self).__init__(wrap_function, args=[function])

#==============================================================================#

