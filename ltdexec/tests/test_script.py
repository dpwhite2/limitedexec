import unittest

from ltdexec import script, source
from ltdexec.dialect import Dialect

from .base import LtdExec_TestCaseBase

#==============================================================================#
class Script_TestCase(LtdExec_TestCaseBase):
    def test_basic(self):
        text = 'print("Hello World!")'
        filename = '<script>'
        mode = 'exec'
        co = compile(text, filename=filename, mode=mode)
        src = source.Source(text, filename)
        my_script = script.Script(co, src, Dialect)

        self.assertEquals(Dialect(), my_script.dialect)

    def test_simple_run_exec(self):
        text = 'x = 7'
        filename = '<script>'
        mode = 'exec'
        co = compile(text, filename=filename, mode=mode)
        src = source.Source(text, filename)
        my_script = script.Script(co, src, Dialect)

        result = my_script.run()

        self.assertEquals(None, result.result)
        self.assertEquals(7, result.locals['x'])

#==============================================================================#