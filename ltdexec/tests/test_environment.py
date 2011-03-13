import unittest
import textwrap

from ltdexec.environment import Environment, EnvironmentFactory
from ltdexec.dialect import Dialect
from ltdexec import wrapper

from .base import LtdExec_TestCaseBase
from .util import TestObj, ThrowingTestObj, ThrowsOnClose

#==============================================================================#
class EnvironmentFactory_TestCase(LtdExec_TestCaseBase):
    def test_basic(self):
        self.assertEquals(0, len(wrapper._local.key_stack))
        envfactory = EnvironmentFactory(Dialect)
        env = envfactory()
        self.assertTrue(isinstance(env, Environment))
        env.close()

#==============================================================================#
class Environment_TestCase(LtdExec_TestCaseBase):

    def test_basic(self):
        self.assertEquals(0, len(wrapper._local.key_stack))
        environment = Environment({}, {'x':5})
        self.assertEquals(1, len(wrapper._local.key_stack))
        environment.close()
        self.assertTrue("Good. No exceptions thrown.")
        self.assertEquals(0, len(wrapper._local.key_stack))
        self.assertEquals(5, environment.globals['x'])

    def test_simple_objects(self):
        objects = {
            'a': wrapper.defname(TestObj),
            'b': wrapper.defname(TestObj, method_on_close='close'),
            }
        self.assertEquals(0, len(wrapper._local.key_stack))
        environment = Environment(objects, {})
        self.assertEquals(True, environment.globals['a'].initialized)
        self.assertEquals(False, environment.globals['a'].closed)
        self.assertEquals(True, environment.globals['b'].initialized)
        self.assertEquals(False, environment.globals['b'].closed)
        environment.close()
        self.assertEquals(True, environment.globals['a'].initialized)
        self.assertEquals(False, environment.globals['a'].closed)
        self.assertEquals(True, environment.globals['b'].initialized)
        self.assertEquals(True, environment.globals['b'].closed)
        self.assertEquals(0, len(wrapper._local.key_stack))

    def test_exception_during_construction(self):
        # In experiments, the order of items in the dict was 'a', 'c', 'b', 'd'.
        # The expected output of this test will change if this does not hold.
        self.assertEquals(['a','c','b','d'], {'a':0,'b':0,'c':0,'d':0}.keys())
        TestObj.clear_instances()
        objects = {
            'a': wrapper.defname(TestObj, args=['a']),
            'c': wrapper.defname(TestObj, args=['c'], method_on_close='close'),
            'b': wrapper.defname(ThrowingTestObj, args=['b'], method_on_close='close'),
            'd': wrapper.defname(TestObj, args=['d']),
            }
        self.assertEquals(0, len(wrapper._local.key_stack))
        with self.assertRaises(RuntimeError) as cm:
            environment = Environment(objects, {})
        self.assertEquals('ThrowingTestObj', cm.exception.args[0])
        self.assertEquals(True, TestObj.instances['a'].initialized)
        self.assertEquals(False, TestObj.instances['a'].closed)
        self.assertEquals(True, TestObj.instances['c'].initialized)
        self.assertEquals(True, TestObj.instances['c'].closed)
        self.assertEquals(False, TestObj.instances['b'].initialized)
        self.assertEquals(False, TestObj.instances['b'].closed)
        self.assertTrue('d' not in TestObj.instances)

    def test_exception_during_construction2(self):
        # In experiments, the order of items in the dict was 'a', 'c', 'b', 'd'.
        # The expected output of this test will change if this does not hold.
        self.assertEquals(['a','c','b','d'], {'a':0,'b':0,'c':0,'d':0}.keys())
        TestObj.clear_instances()
        objects = {
            'a': wrapper.defname(ThrowsOnClose, args=['a'], method_on_close='close'),
            'c': wrapper.defname(TestObj, args=['c'], method_on_close='close'),
            'b': wrapper.defname(ThrowingTestObj, args=['b'], method_on_close='close'),
            'd': wrapper.defname(TestObj, args=['d']),
            }
        self.assertEquals(0, len(wrapper._local.key_stack))
        with self.assertRaises(RuntimeError) as cm:
            environment = Environment(objects, {})
        self.assertEquals('ThrowingTestObj', cm.exception.args[0])
        self.assertEquals(0, len(wrapper._local.key_stack))

        self.assertEquals(True, TestObj.instances['a'].initialized)
        self.assertEquals(False, TestObj.instances['a'].closed)
        self.assertEquals(True, TestObj.instances['c'].initialized)
        self.assertEquals(True, TestObj.instances['c'].closed) # This is closed even though 'a' raised an exception
        self.assertEquals(False, TestObj.instances['b'].initialized)
        self.assertEquals(False, TestObj.instances['b'].closed)
        self.assertTrue('d' not in TestObj.instances)

    def test_exception_during_destruction(self):
        # In experiments, the order of items in the dict was 'a', 'c', 'b', 'd'.
        # The expected output of this test will change if this does not hold.
        self.assertEquals(['a','c','b','d'], {'a':0,'b':0,'c':0,'d':0}.keys())
        TestObj.clear_instances()
        objects = {
            'a': wrapper.defname(ThrowsOnClose, args=['a'], method_on_close='close'),
            'c': wrapper.defname(TestObj, args=['c'], method_on_close='close'),
            'b': wrapper.defname(TestObj, args=['b'], method_on_close='close'),
            'd': wrapper.defname(TestObj, args=['d']),
            }
        self.assertEquals(0, len(wrapper._local.key_stack))

        env = Environment(objects, {})
        with self.assertRaises(RuntimeError) as cm:
            env.close()

        self.assertEquals('ThrowsOnClose', cm.exception.args[0])
        self.assertEquals(0, len(wrapper._local.key_stack))

        self.assertEquals(True,  env.globals['a'].initialized)
        self.assertEquals(False, env.globals['a'].closed)
        self.assertEquals(True,  env.globals['c'].initialized)
        self.assertEquals(True,  env.globals['c'].closed)
        self.assertEquals(True,  env.globals['b'].initialized)
        self.assertEquals(True,  env.globals['b'].closed)
        self.assertEquals(True,  env.globals['d'].initialized)
        self.assertEquals(False, env.globals['d'].closed)
        
    def test_import(self):
        src = """\
        _LX_import_module('math')
        x = math.sqrt(16.0)
        """
        src = textwrap.dedent(src)
        with Environment({}, {}) as env:
            co = compile(src, '<no_name>', mode='exec')
            r = eval(co, env.globals, env.locals)
            self.assertTrue('Good. No exception.')
            self.assertEquals(4.0, env.globals['x'])
        
    def test_import_from(self):
        src = """\
        _LX_import_module('math', froms=[('sqrt',None)])
        x = sqrt(16.0)
        """
        src = textwrap.dedent(src)
        with Environment({}, {}) as env:
            co = compile(src, '<no_name>', mode='exec')
            r = eval(co, env.globals, env.locals)
            self.assertTrue('Good. No exception.')
            self.assertEquals(4.0, env.globals['x'])




#==============================================================================#