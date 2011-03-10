import unittest

from ltdexec.dialect.base import Dialect
from ltdexec.processor.validator import AstValidator

from .base import LtdExec_TestCaseBase


#==============================================================================#
class Struct(object):
    pass

#==============================================================================#
class Dialect_TestCase(LtdExec_TestCaseBase):

    def test_basic(self):
        dialect = Dialect()
        # same object must be returned
        self.assertEquals(dialect, Dialect())

        self.assertEquals(None, Dialect.Processor)
        self.assertEquals(None, Dialect.SourceValidator)
        self.assertEquals(None, Dialect.SourceTransform)
        self.assertEquals(None, Dialect.AstValidator)
        self.assertEquals(None, Dialect.AstTransform)
        self.assertEquals(None, Dialect.EnvironmentFactory)
        self.assertEquals(None, Dialect.Compiler)

    def test_flags(self):
        self.assertEquals(False, Dialect.allow_statement_import)
        self.assertEquals(True, Dialect.allow_statement_def)
        self.assertEquals(True, Dialect.allow_statement_try_finally)
        self.assertEquals(True, Dialect.allow_statement_try_except)
        self.assertEquals(True, Dialect.allow_statement_raise)
        self.assertFalse(hasattr(Dialect, 'allow_statements_non_expressions'))
        self.assertEquals(False, Dialect().allow_statement_import)
        self.assertEquals(True, Dialect().allow_statement_def)
        self.assertEquals(True, Dialect().allow_statement_try_finally)
        self.assertEquals(True, Dialect().allow_statement_try_except)
        self.assertEquals(True, Dialect().allow_statement_raise)
        self.assertFalse(hasattr(Dialect(), 'allow_statements_non_expressions'))

    def test_names(self):
        self.assertEquals(set(('type open eval execfile exec compile reload '
                               '__import__ globals locals delattr setattr '
                               'getattr hasattr vars raw_input input dir file '
                               'help').split()),
                          Dialect.forbidden_names_set)
        self.assertEquals(set('__class__ __dict__ __bases__ __mro__ __module__ __file__'.split()),
                          Dialect.forbidden_attrs_set)
        self.assertEquals(set(), Dialect.unassignable_names_set)
        self.assertEquals(set(), Dialect.unassignable_attrs_set)

    def test_create_ast_validator(self):
        AutoAstValidator = Dialect().AstValidator
        # Later calls must return the same class object:
        self.assertEquals(AutoAstValidator, Dialect().AstValidator)
        self.assertTrue(isinstance(AutoAstValidator, type))
        self.assertTrue(issubclass(AutoAstValidator, AstValidator))
        self.assertTrue(hasattr(AutoAstValidator, 'visit_Import'))
        self.assertTrue(hasattr(AutoAstValidator, 'visit_ImportFrom'))
        self.assertTrue(hasattr(AutoAstValidator, 'visit_Exec'))
        self.assertTrue(hasattr(AutoAstValidator, 'visit_Delete'))

    def test_create_classes(self):
        SourceTransform = Dialect().SourceTransform
        self.assertTrue(isinstance(SourceTransform, type))
        self.assertEquals(SourceTransform, Dialect().SourceTransform)

        SourceValicator = Dialect().SourceValidator
        self.assertTrue(isinstance(SourceValicator, type))
        self.assertEquals(SourceValicator, Dialect().SourceValidator)

        AstTransform = Dialect().AstTransform
        self.assertTrue(isinstance(AstTransform, type))
        self.assertEquals(AstTransform, Dialect().AstTransform)

        Processor = Dialect().Processor
        self.assertTrue(isinstance(Processor, type))

    def test_dialect_name(self):
        self.assertEquals('ltdexec.dialect.base.Dialect', Dialect.name)
        
    def test_getattr(self):
        obj = Struct()
        obj.abc = 123
        obj._LX_forbidden = 456
        
        self.assertEquals(123, Dialect.getattr(obj, 'abc'))
        self.assertEquals(None, Dialect.getattr(obj, 'efg', None))
        with self.assertRaises(AttributeError) as cm:
            Dialect.getattr(obj, 'efg')
        with self.assertRaises(RuntimeError) as cm:
            Dialect.getattr(obj, '_LX_forbidden')
        with self.assertRaises(RuntimeError) as cm:
            Dialect.getattr(obj, '__class__')
        
    def test_hasattr(self):
        obj = Struct()
        obj.abc = 123
        obj._LX_forbidden = 456
        
        self.assertTrue(Dialect.hasattr(obj, 'abc'))
        self.assertFalse(Dialect.hasattr(obj, 'efg'))
        with self.assertRaises(RuntimeError) as cm:
            Dialect.hasattr(obj, '_LX_forbidden')
        with self.assertRaises(RuntimeError) as cm:
            Dialect.hasattr(obj, '__class__')
        
    def test_setattr(self):
        obj = Struct()
        obj.abc = 123
        obj._LX_forbidden = 456
        
        Dialect.setattr(obj, 'abc', 321)
        self.assertTrue(321, obj.abc)
        Dialect.setattr(obj, 'efg', 'xyz')
        self.assertTrue('xyz', obj.efg)
        
        with self.assertRaises(RuntimeError) as cm:
            Dialect.setattr(obj, '_LX_forbidden', 101)
        with self.assertRaises(RuntimeError) as cm:
            Dialect.setattr(obj, '__class__', 'what a class!')
        
    def test_delattr(self):
        obj = Struct()
        obj.abc = 123
        obj._LX_forbidden = 456
        
        Dialect.delattr(obj, 'abc')
        self.assertFalse(hasattr(obj, 'abc'))
        with self.assertRaises(AttributeError) as cm:
            Dialect.delattr(obj, 'efg')
        with self.assertRaises(RuntimeError) as cm:
            Dialect.delattr(obj, '_LX_forbidden')
        with self.assertRaises(RuntimeError) as cm:
            Dialect.delattr(obj, '__class__')
        
        

#==============================================================================#
class EmptyCustomDialect_TestCase(LtdExec_TestCaseBase):
    # An empty dialect should behave just like Dialect.

    def setUp(self):
        super(EmptyCustomDialect_TestCase, self).setUp()
        class MyDialect(Dialect):
            pass
        self.MyDialect = MyDialect

    def test_flags(self):
        self.assertEquals(False, self.MyDialect.allow_statement_import)
        self.assertEquals(True, self.MyDialect.allow_statement_def)
        self.assertEquals(True, self.MyDialect.allow_statement_try_finally)
        self.assertEquals(True, self.MyDialect.allow_statement_try_except)
        self.assertEquals(True, self.MyDialect.allow_statement_raise)
        self.assertFalse(hasattr(self.MyDialect, 'allow_statements_non_expressions'))

    def test_names(self):
        self.assertEquals(set(('type open eval execfile exec compile reload '
                               '__import__ globals locals delattr setattr '
                               'getattr hasattr vars raw_input input dir file '
                               'help').split()),
                          self.MyDialect.forbidden_names_set)
        self.assertEquals(set('__class__ __dict__ __bases__ __mro__ __module__ __file__'.split()),
                          self.MyDialect.forbidden_attrs_set)
        self.assertEquals(set(), self.MyDialect.unassignable_names_set)
        self.assertEquals(set(), self.MyDialect.unassignable_attrs_set)

    def test_dialect_name(self):
        self.assertEquals('ltdexec.tests.test_dialect.MyDialect', self.MyDialect.name)

#==============================================================================#
class CustomDialect_TestCase(LtdExec_TestCaseBase):
    def test_parent_flag(self):
        class MyDialect(Dialect):
            allow_statements_exceptions = False

        self.assertEquals(False, MyDialect.allow_statement_try_finally)
        self.assertEquals(False, MyDialect.allow_statement_try_except)
        self.assertEquals(False, MyDialect.allow_statement_raise)

    def test_nested_flag_behavior(self):
        # TODO
        # nested flags override parent flags
        pass

    def test_non_expressions_flag(self):
        class MyDialect(Dialect):
            allow_statements_non_expressions = False

        self.assertEquals(False, MyDialect.allow_statement_def)
        self.assertEquals(False, MyDialect.allow_statement_class)
        self.assertEquals(False, MyDialect.allow_statement_import)
        self.assertEquals(False, MyDialect.allow_statement_import_from)
        self.assertEquals(False, MyDialect.allow_statement_assignment)
        self.assertEquals(False, MyDialect.allow_statement_augmented_assignment)
        self.assertEquals(False, MyDialect.allow_statement_for)
        self.assertEquals(False, MyDialect.allow_statement_while)
        self.assertEquals(False, MyDialect.allow_statement_try_finally)
        self.assertEquals(False, MyDialect.allow_statement_try_except)
        self.assertEquals(False, MyDialect.allow_statement_raise)
        self.assertEquals(False, MyDialect.allow_statement_exec)
        self.assertEquals(False, MyDialect.allow_statement_assert)
        self.assertEquals(False, MyDialect.allow_statement_global)
        self.assertEquals(False, MyDialect.allow_statement_nonlocal)
        self.assertEquals(False, MyDialect.allow_statement_del)
        self.assertEquals(False, MyDialect.allow_statement_if)
        self.assertEquals(False, MyDialect.allow_statement_with)
        self.assertEquals(False, MyDialect.allow_statement_print)
        self.assertEquals(False, MyDialect.allow_statement_pass)
        self.assertEquals(False, MyDialect.allow_statement_break)
        self.assertEquals(False, MyDialect.allow_statement_continue)
        self.assertEquals(False, MyDialect.allow_statement_return)
        self.assertEquals(True, MyDialect.allow_expression_yield)
        self.assertEquals(True, MyDialect.allow_expression_lambda)

#==============================================================================#
