import unittest
import types
import ast
import textwrap

from ltdexec.dialect.base import Dialect
from ltdexec import exceptions, compiler
from ltdexec.script import Script

from .base import LtdExec_TestCaseBase

#==============================================================================#
class Compiler_DoCompile_TestCase(LtdExec_TestCaseBase):
    def test_basic(self):
        mycompiler = compiler.Compiler(Dialect())
        co = mycompiler.do_compile('','<no_file>')
        self.assertTrue(isinstance(co, types.CodeType))

class Compiler_CompileToCode_TestCase(LtdExec_TestCaseBase):
    def setUp(self):
        super(Compiler_CompileToCode_TestCase, self).setUp()
        self.compiler = compiler.Compiler(Dialect())

    def test_exec(self):
        filename = '<no_file>'
        tree = ast.parse('a = 5', filename=filename, mode='exec')
        co = self.compiler.compile_to_code(tree, filename)
        self.assertTrue(isinstance(co, types.CodeType))

    def test_eval(self):
        filename = '<no_file>'
        tree = ast.parse('3 + 7', filename=filename, mode='eval')
        co = self.compiler.compile_to_code(tree, filename)
        self.assertTrue(isinstance(co, types.CodeType))

    def test_bad_asttree(self):
        filename = '<no_file>'
        tree = 'I am not an AST tree.'
        with self.assertRaises(RuntimeError) as cm:
            co = self.compiler.compile_to_code(tree, filename)


class DefaultCompiler_TestCase(LtdExec_TestCaseBase):
    def test_empty(self):
        comp = compiler.Compiler(Dialect())
        script = comp('', 'my_file')
        self.assertTrue(isinstance(script, Script))
        self.assertEquals('my_file', script.filename)

    def test_syntax_error(self):
        comp = compiler.Compiler(Dialect())
        with self.assertRaises(exceptions.CompilationError) as cm:
            script = comp('not * 5', 'my_file')
        self.assertEquals('not * 5', str(cm.exception.source))
        self.assertEquals('my_file', cm.exception.source.filename)
        type, value, tb = cm.exception.exc_info
        self.assertEquals(SyntaxError, type)
        self.assertEquals(1, value.lineno)
        self.assertEquals(5, value.offset)
        self.assertEquals('my_file', value.filename)
        self.assertEquals('not * 5\n', value.text)

        fe = cm.exception.format_exception()
        self.assertEquals('Traceback (most recent call last):\n', fe[0])
        self.assertEquals('  File "my_file", line 1\n', fe[-4])
        self.assertEquals('    not * 5\n', fe[-3])
        self.assertEquals('        ^\n', fe[-2])
        self.assertEquals('SyntaxError: invalid syntax\n', fe[-1])

    def test_lx_syntax_error(self):
        comp = compiler.Compiler(Dialect())
        with self.assertRaises(exceptions.CompilationError) as cm:
            script = comp('import module', 'my_file')
        self.assertEquals('import module', str(cm.exception.source))
        self.assertEquals('my_file', cm.exception.source.filename)
        type, value, tb = cm.exception.exc_info
        self.assertEquals(exceptions.SyntaxError, type)
        self.assertEquals(1, value.lineno)
        self.assertEquals(1, value.offset)
        self.assertEquals('my_file', value.filename)
        self.assertEquals('import module\n', value.text)

        ##print cm.exception
        fe = cm.exception.format_exception()
        self.assertEquals('Traceback (most recent call last):\n', fe[0])
        self.assertEquals('  File "my_file", line 1\n', fe[-4])
        self.assertEquals('    import module\n', fe[-3])
        self.assertEquals('    ^\n', fe[-2])
        self.assertEquals('SyntaxError: The following is not allowed in this script: import statement.\n', fe[-1])

#==============================================================================#