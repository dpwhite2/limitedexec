from .meta import DialectMeta
from ..config.flags import leafflag_traits
from ..processor import validator, transform, processor


#==============================================================================#
class _DialectBase(object):
    pass

# Set flag defaults in _DialectBase.
for traits in leafflag_traits.itervalues():
    setattr(_DialectBase, traits.name, traits.default)


#==============================================================================#
class Dialect(_DialectBase):
    __metaclass__ = DialectMeta

    Processor = processor.Processor
    SourceValidator = validator.SourceValidator
    SourceTransform = transform.SourceTransform
    AstValidator = None
    AstTransform = transform.AstTransform

    @classmethod
    def source_transform_class(cls):
        if not cls.SourceTransform:
            cls.SourceTransform = cls.create_source_transform_class()
        return cls.SourceTransform

    @classmethod
    def create_source_transform_class(cls):
        raise NotImplementedError()

    @classmethod
    def ast_transform_class(cls):
        if not cls.AstTransform:
            cls.AstTransform = cls.create_ast_transform_class()
        return cls.AstTransform

    @classmethod
    def create_ast_transform_class(cls):
        raise NotImplementedError()

    @classmethod
    def source_validator_class(cls):
        if not cls.SourceValidator:
            cls.SourceValidator = cls.create_source_validator_class()
        return cls.SourceValidator

    @classmethod
    def create_source_validator_class(cls):
        raise NotImplementedError()

    @classmethod
    def ast_validator_class(cls):
        if not cls.AstValidator:
            cls.AstValidator = cls.create_ast_validator_class()
        return cls.AstValidator

    @classmethod
    def create_ast_validator_class(cls):
        return validator.create_ast_validator_class(cls)

    @classmethod
    def compiler_instance(cls):
        try:
            return cls._compiler_instance
        except AttributeError:
            cls._compiler_instance = cls.create_compiler()
            return cls._compiler_instance

    @classmethod
    def create_compiler(cls):
        pass


#==============================================================================#


