import textwrap
import types

from ltdexec.dialect import Dialect
from ltdexec import compiler
from ltdexec.wrapper import ModuleWrapper

from .base import LtdExec_TestCaseBase
from .util import TestObj, ThrowingTestObj, ThrowsOnClose

#==============================================================================#

class Run_TestCase(LtdExec_TestCaseBase):
    def test_imported_module(self):
        class MyDialect(Dialect):
            allow_statement_import = True
            
        filename = '<my_file>'
        src = """\
        import math
        """
        src = textwrap.dedent(src)
        script = compiler.compile(src, filename, MyDialect)
        result = script.run()
        globals = result.globals
        self.assertFalse(isinstance(result.globals['math'], types.ModuleType))
        self.assertTrue(isinstance(result.globals['math'], ModuleWrapper))
        





