import __builtin__

from .meta import DialectMeta
from . import registry
from ..config.flags import leafflag_traits
from ..processor import validator, transform, processor
from .. import compiler, environment



#==============================================================================#
class _DialectBase(object):
    """ Dialect base class that defines the default settings for certain flags 
        and attributes. 
    """
    allowed_imports = {}
    forbidden_imports = {}
    objects = {}

# Set flag defaults in _DialectBase.
for traits in leafflag_traits.itervalues():
    setattr(_DialectBase, traits.name, traits.default)


#==============================================================================#
class Dialect(_DialectBase):
    """ The Dialect defines the limitations and abilities of scripts.  
        
        It defines the limitations by declaring what parts of the Python 
        language are and are not permissible.  It also defines what names, 
        attributes, and modules are and are not permissible.  It defines the 
        abilities by declaring what objects will be available to scripts. 
        
        To create a custom dialect, one should use this class as a base class.
        
        Dialects should not be modified once defined.  All configuration should 
        be placed within the class statement.  This invariant is assumed 
        throughout the LtdExec library, and to do otherwise may result in 
        unpredictable behavior.  By treating Dialects as though they were 
        immutable, it allows them to be singletons without incurring the 
        downsides singletons otherwise may have.  In fact, calling the class 
        (e.g. ``x = Dialect()``) will *always* return the same instance object.
    """
    __metaclass__ = DialectMeta

    Processor = None
    SourceValidator = None
    SourceTransform = None
    AstValidator = None
    AstTransform = None
    EnvironmentFactory = None
    Compiler = None

    def __init__(self):
        ##print 'creating Dialect.'
        self.Processor = self.Processor or processor.Processor
        self.SourceValidator = self.SourceValidator or validator.SourceValidator
        self.SourceTransform = self.SourceTransform or transform.SourceTransform
        self.AstValidator = self.AstValidator or validator.create_ast_validator_class(self)
        self.AstTransform = self.AstTransform or transform.AstTransform
        self.EnvironmentFactory = self.EnvironmentFactory or environment.EnvironmentFactory
        compiler_cls = self.Compiler or compiler.Compiler
        self.compiler = compiler_cls(self)
        self.objects = self.objects.copy()

    @classmethod
    def compile(cls, src, filename):
        dialect = registry.dialects[cls.name]
        return dialect.compiler(src, filename)
    
    
    @classmethod
    def getattr(cls, obj, name, *args):
        if name.startswith(LTDEXEC_PRIVATE_PREFIX):
            raise RuntimeError('TODO')
        elif name in cls.forbidden_attrs_set:
            raise RuntimeError('TODO')
        return __builtin__.getattr(obj, name, *args)
        
    @classmethod
    def hasattr(cls, obj, name):
        if name.startswith(LTDEXEC_PRIVATE_PREFIX):
            raise RuntimeError('TODO')
        elif name in cls.forbidden_attrs_set:
            raise RuntimeError('TODO')
        return __builtin__.hasattr(obj, name)
        
    @classmethod
    def setattr(cls, obj, name, val):
        if name.startswith(LTDEXEC_PRIVATE_PREFIX):
            raise RuntimeError('TODO')
        elif name in cls.forbidden_attrs_set:
            raise RuntimeError('TODO')
        elif name in cls.unassignable_attrs_set:
            raise RuntimeError('TODO')
        __builtin__.setattr(obj, name, val)
        
    @classmethod
    def delattr(cls, obj, name):
        if name.startswith(LTDEXEC_PRIVATE_PREFIX):
            raise RuntimeError('TODO')
        elif name in cls.forbidden_attrs_set:
            raise RuntimeError('TODO')
        elif name in cls.unassignable_attrs_set:
            raise RuntimeError('TODO')
        __builtin__.delattr(obj, name)




#==============================================================================#
