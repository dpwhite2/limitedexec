import unittest

from ltdexec import script, source, wrapper
from ltdexec.dialect import Dialect

from .base import LtdExec_TestCaseBase
from .util import TestObj, ThrowingTestObj, ThrowsOnClose

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

    def test_simple_run_eval(self):
        text = '2 + 9'
        filename = '<script>'
        mode = 'eval'
        co = compile(text, filename=filename, mode=mode)
        src = source.Source(text, filename)
        my_script = script.Script(co, src, Dialect)

        result = my_script.run()

        self.assertEquals(11, result.result)
        #self.assertEquals(0, len(result.locals))

    def test_simple_raise_exception(self):
        text = 'raise RuntimeError("I raised it!")'
        filename = '<script>'
        mode = 'exec'
        co = compile(text, filename=filename, mode=mode)
        src = source.Source(text, filename)
        my_script = script.Script(co, src, Dialect)

        result = my_script.run()
        self.assertTrue("Good. No exception was raised.")

        self.assertEquals(None, result.result)
        self.assertEquals(True, result.exception)
        exc_type, exc_value, exc_tb = result.exc_info
        self.assertEquals(RuntimeError, exc_type)
        self.assertEquals("I raised it!", exc_value.args[0])

    def test_raising_on_environment_construction(self):
        # In experiments, the order of items in the dict was 'a', 'c', 'b', 'd'.
        # The expected output of this test will change if this does not hold.
        self.assertEquals(['a','c','b','d'], {'a':0,'b':0,'c':0,'d':0}.keys())
        TestObj.clear_instances()

        class MyDialect(Dialect):
            objects = {
                'a': wrapper.defname(TestObj, args=['a']),
                'c': wrapper.defname(TestObj, args=['c'], method_on_close='close'),
                'b': wrapper.defname(ThrowingTestObj, args=['b'], method_on_close='close'),
                'd': wrapper.defname(TestObj, args=['d']),
            }

        text = 'x = 5'
        filename = '<script>'
        mode = 'exec'
        co = compile(text, filename=filename, mode=mode)
        src = source.Source(text, filename)
        my_script = script.Script(co, src, MyDialect)

        with self.assertRaises(RuntimeError) as cm:
            result = my_script.run()
        self.assertEquals('ThrowingTestObj', cm.exception.args[0])

        self.assertEquals(True, TestObj.instances['a'].initialized)
        self.assertEquals(False, TestObj.instances['a'].closed)
        self.assertEquals(True, TestObj.instances['c'].initialized)
        self.assertEquals(True, TestObj.instances['c'].closed)
        self.assertEquals(False, TestObj.instances['b'].initialized)
        self.assertEquals(False, TestObj.instances['b'].closed)
        self.assertTrue('d' not in TestObj.instances)


#==============================================================================#