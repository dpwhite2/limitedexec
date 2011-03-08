import unittest

import ltdexec.dialect.meta
from ltdexec.dialect.base import Dialect
from ltdexec.processor.validator import AstValidator

class Dialect_TestCase(unittest.TestCase):
    def test_flags(self):
        self.assertEquals(False, Dialect.allow_statement_import)
        self.assertEquals(True, Dialect.allow_statement_def)
        self.assertEquals(True, Dialect.allow_statement_try_finally)
        self.assertEquals(True, Dialect.allow_statement_try_except)
        self.assertEquals(True, Dialect.allow_statement_raise)
        self.assertFalse(hasattr(Dialect, 'allow_statements_non_expressions'))
    
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
        AutoAstValidator = Dialect.ast_validator_class()
        # Later calls must return the same class object:
        self.assertEquals(AutoAstValidator, Dialect.ast_validator_class())
        self.assertTrue(isinstance(AutoAstValidator, type))
        self.assertTrue(issubclass(AutoAstValidator, AstValidator))
        self.assertTrue(hasattr(AutoAstValidator, 'visit_Import'))
        self.assertTrue(hasattr(AutoAstValidator, 'visit_ImportFrom'))
        self.assertTrue(hasattr(AutoAstValidator, 'visit_Exec'))
        self.assertTrue(hasattr(AutoAstValidator, 'visit_Delete'))

class EmptyCustomDialect_TestCase(unittest.TestCase):
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
        
class CustomDialect_TestCase(unittest.TestCase):
    def test_parent_flag(self):
        class MyDialect(Dialect):
            allow_statements_exceptions = False
        
        self.assertEquals(False, MyDialect.allow_statement_try_finally)
        self.assertEquals(False, MyDialect.allow_statement_try_except)
        self.assertEquals(False, MyDialect.allow_statement_raise)
        
    def test_nested_flag_behavior(self):
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
        
        
        
        
