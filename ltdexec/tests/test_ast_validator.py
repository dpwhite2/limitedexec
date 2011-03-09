import unittest
import ast

from ltdexec.dialect.base import Dialect
from ltdexec import exceptions

from .base import LtdExec_TestCaseBase

#==============================================================================#
class DefaultAstValidator_TestCase(LtdExec_TestCaseBase):
    def setUp(self):
        super(DefaultAstValidator_TestCase, self).setUp()
        self.AstValidator = Dialect().AstValidator
        self.validator = self.AstValidator(Dialect())
        
    def test_empty(self):
        tree = ast.parse("")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')
        
    def test_import(self):
        tree = ast.parse("import module")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(0, cm.exception.offset)
        self.assertEquals('node_Import', cm.exception.reason)
        
        tree = ast.parse("from package import name")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(0, cm.exception.offset)
        self.assertEquals('node_ImportFrom', cm.exception.reason)
        
    def test_forbidden_name(self):
        tree = ast.parse("x = type(y)")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(4, cm.exception.offset)
        self.assertEquals('forbidden_name', cm.exception.reason)
        
    def test_forbidden_attr(self):
        tree = ast.parse("x = a.__class__")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(4, cm.exception.offset)
        self.assertEquals('forbidden_attr', cm.exception.reason)
        
    def test_allowed_attr(self):
        tree = ast.parse("x = a.__name__")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')
            
        
#==============================================================================#
class ImportsDialect_TestCase(LtdExec_TestCaseBase):
    def setUp(self):
        super(ImportsDialect_TestCase, self).setUp()
        class MyDialect(Dialect):
            allow_statement_import = True
            allow_statement_import_from = True
        
        self.MyDialect = MyDialect()
        self.AstValidator = MyDialect().AstValidator
        self.validator = self.AstValidator(MyDialect)
        
    def test_basic(self):
        self.assertEqual(True, self.MyDialect.allow_statement_import)
        self.assertEqual(True, self.MyDialect.allow_statement_import_from)
        
    def test_empty(self):
        tree = ast.parse("")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')
        
    def test_import(self):
        tree = ast.parse("import module")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')
        
        tree = ast.parse("from package import name")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

#==============================================================================#








