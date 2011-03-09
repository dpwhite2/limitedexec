import unittest
import types

from ltdexec.dialect.base import Dialect
from ltdexec import exceptions, compiler

from .base import LtdExec_TestCaseBase

#==============================================================================#
class Compiler_DoCompile_TestCase(LtdExec_TestCaseBase):
    def test_basic(self):
        mycompiler = compiler.Compiler(Dialect())
        co = mycompiler.do_compile('','<no_file>')
        self.assertTrue(isinstance(co, types.CodeType))

#==============================================================================#
