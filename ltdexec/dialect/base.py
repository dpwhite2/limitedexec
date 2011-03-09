from .meta import DialectMeta
from . import registry
from ..config.flags import leafflag_traits
from ..processor import validator, transform, processor
from .. import compiler, environment


#==============================================================================#
class _DialectBase(object):
    allowed_imports = {}
    forbidden_imports = {}
    objects = {}

# Set flag defaults in _DialectBase.
for traits in leafflag_traits.itervalues():
    setattr(_DialectBase, traits.name, traits.default)


#==============================================================================#
class Dialect(_DialectBase):
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
    




#==============================================================================#

