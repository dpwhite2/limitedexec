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
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('node_Import', cm.exception.reason)

        tree = ast.parse("from package import name")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('node_ImportFrom', cm.exception.reason)

    def test_forbidden_name(self):
        tree = ast.parse("x = type(y)")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(5, cm.exception.offset)
        self.assertEquals('forbidden_name', cm.exception.reason)

    def test_forbidden_attr(self):
        tree = ast.parse("x = a.__class__")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(5, cm.exception.offset)
        self.assertEquals('forbidden_attr', cm.exception.reason)

    def test_allowed_attr(self):
        tree = ast.parse("x = a.__name__")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

    def test_private_prefix_name(self):
        tree = ast.parse("_LX_not_allowed")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('private_prefix_name', cm.exception.reason)

    def test_private_prefix_attr(self):
        tree = ast.parse("a._LX_not_allowed")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('private_prefix_attr', cm.exception.reason)



#==============================================================================#
class ImportsDialectAstValidator_TestCase(LtdExec_TestCaseBase):
    def setUp(self):
        super(ImportsDialectAstValidator_TestCase, self).setUp()
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

    def test_forbidden_name_import(self):
        tree = ast.parse("import type")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('import_forbidden_name', cm.exception.reason)

        tree = ast.parse("from module import type")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('import_forbidden_name', cm.exception.reason)

        tree = ast.parse("from module import abc as type")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('import_forbidden_name', cm.exception.reason)

    def test_relative_import(self):
        tree = ast.parse("from . import name")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('relative_import', cm.exception.reason)

        tree = ast.parse("from .package import name")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('relative_import', cm.exception.reason)

        tree = ast.parse("from .. import name")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('relative_import', cm.exception.reason)


#==============================================================================#
class ImportsDialectAstValidator2_TestCase(LtdExec_TestCaseBase):
    def setUp(self):
        super(ImportsDialectAstValidator2_TestCase, self).setUp()
        class MyDialect(Dialect):
            allow_statements_imports = True
            allowed_imports = {
                'math': set(),
                }

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

    def test_import_allowed(self):
        tree = ast.parse("import math")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("from math import sin")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

    def test_import_not_allowed(self):
        tree = ast.parse("import sys")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('not_in_allowed_imports', cm.exception.reason)

        tree = ast.parse("from sys import names")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('not_in_allowed_imports', cm.exception.reason)

#==============================================================================#
class ImportsDialectAstValidator3_TestCase(LtdExec_TestCaseBase):
    def setUp(self):
        super(ImportsDialectAstValidator3_TestCase, self).setUp()
        class MyDialect(Dialect):
            allow_statements_imports = True
            forbidden_imports = set(('sys',))

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

    def test_import_not_forbidden(self):
        tree = ast.parse("import math")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("from math import cos")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

    def test_import_forbidden(self):
        tree = ast.parse("import sys")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('forbidden_import', cm.exception.reason)

        tree = ast.parse("from sys import names")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('forbidden_import', cm.exception.reason)


#==============================================================================#
class ImportsDialectAstValidator4_TestCase(LtdExec_TestCaseBase):
    def setUp(self):
        super(ImportsDialectAstValidator4_TestCase, self).setUp()
        class MyDialect(Dialect):
            allow_statements_imports = True
            allowed_imports = {
                'sys': set(('exc_info','version_info',)),
                'math': None,
                }

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

    def test_import_allowed(self):
        tree = ast.parse("import math")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("import sys")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("from sys import exc_info")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("from sys import exc_info, version_info")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

    def test_import_not_allowed(self):
        tree = ast.parse("from sys import path")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('not_in_allowed_imports_froms', cm.exception.reason)

        tree = ast.parse("from sys import exc_info, exit")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('not_in_allowed_imports_froms', cm.exception.reason)

#==============================================================================#
class NoDoubleUnderscoreNames_AstValidator_TestCase(LtdExec_TestCaseBase):
    def setUp(self):
        super(NoDoubleUnderscoreNames_AstValidator_TestCase, self).setUp()
        class MyDialect(Dialect):
            no_double_underscore_names = True

        self.MyDialect = MyDialect()
        self.AstValidator = self.MyDialect.AstValidator
        self.validator = self.AstValidator(self.MyDialect)

    def test_empty(self):
        tree = ast.parse("")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

    def test_allowed_names(self):
        tree = ast.parse("name")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("__name")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("name__")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("_name_")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("__name_")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("_name__")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("_")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("a.__attr__")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

    def test_forbidden_names(self):
        tree = ast.parse("__abc__")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('double_underscore_name', cm.exception.reason)

        tree = ast.parse("__")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('double_underscore_name', cm.exception.reason)

        tree = ast.parse("___xtra_underscores___")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('double_underscore_name', cm.exception.reason)

        tree = ast.parse("__abc__.__attr__")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('double_underscore_name', cm.exception.reason)

#==============================================================================#
class NoDoubleUnderscoreAttrs_AstValidator_TestCase(LtdExec_TestCaseBase):
    def setUp(self):
        super(NoDoubleUnderscoreAttrs_AstValidator_TestCase, self).setUp()
        class MyDialect(Dialect):
            no_double_underscore_attrs = True

        self.MyDialect = MyDialect()
        self.AstValidator = self.MyDialect.AstValidator
        self.validator = self.AstValidator(self.MyDialect)

    def test_empty(self):
        tree = ast.parse("")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

    def test_allowed_attrs(self):
        tree = ast.parse("a.name")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("a.__name")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("a.name__")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("a._name_")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("a.__name_")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("a._name__")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("a._")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

        tree = ast.parse("__abc__")
        self.validator(tree)
        self.assertTrue('Good.  No exception was thrown.')

    def test_forbidden_attrs(self):
        tree = ast.parse("a.__abc__")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('double_underscore_attr', cm.exception.reason)

        tree = ast.parse("a.__")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('double_underscore_attr', cm.exception.reason)

        tree = ast.parse("a.___xtra_underscores___")
        with self.assertRaises(exceptions.SyntaxError) as cm:
            self.validator(tree)
        self.assertEquals(1, cm.exception.lineno)
        self.assertEquals(1, cm.exception.offset)
        self.assertEquals('double_underscore_attr', cm.exception.reason)


#==============================================================================#






