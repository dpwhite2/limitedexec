import unittest

from ltdexec.wrapper import WrapperBase, wrap_class, ModuleWrapper

from .base import LtdExec_TestCaseBase

#==============================================================================#
class Struct(object):
    pass
#==============================================================================#
class WrapperBase_TestCase(LtdExec_TestCaseBase):
    def test_basic(self):
        obj = Struct()
        obj.abc = 123
        wrapper = WrapperBase(obj)
        self.assertEquals(123, wrapper.abc)
        wrapper.xyz = 5
        self.assertEquals(5, wrapper.xyz)
        self.assertEquals(obj, wrapper._LX_obj)
        self.assertEquals(5, obj.xyz)
        
    def test_readable_attrs(self):
        class MyWrapper(WrapperBase):
            _LX_readable_attrs = set(('xyz',))
        obj = Struct()
        obj.abc = 123
        obj.xyz = 789
        wrapper = MyWrapper(obj)
        self.assertEquals(789, wrapper.xyz)
        wrapper.xyz = 5
        self.assertEquals(5, wrapper.xyz)
        with self.assertRaises(RuntimeError) as cm:
            x = wrapper.abc
        wrapper.abc = 321
        with self.assertRaises(RuntimeError) as cm:
            x = wrapper.abc
        self.assertEquals(obj, wrapper._LX_obj)
        self.assertEquals(321, obj.abc)
        self.assertEquals(5, obj.xyz)
        
    def test_writable_attrs(self):
        class MyWrapper(WrapperBase):
            _LX_writable_attrs = set(('a',))
        obj = Struct()
        obj.a = 123
        obj.b = 789
        wrapper = MyWrapper(obj)
        self.assertEquals(123, wrapper.a)
        self.assertEquals(789, wrapper.b)
        wrapper.a = 5
        self.assertEquals(5, wrapper.a)
        with self.assertRaises(RuntimeError) as cm:
            wrapper.b = 9
        self.assertEquals(obj, wrapper._LX_obj)
        self.assertEquals(5, obj.a)
        self.assertEquals(789, obj.b)
        
    def test_unreadable_attrs(self):
        class MyWrapper(WrapperBase):
            _LX_unreadable_attrs = set(('abc',))
        obj = Struct()
        obj.abc = 123
        obj.xyz = 789
        wrapper = MyWrapper(obj)
        self.assertEquals(789, wrapper.xyz)
        wrapper.xyz = 5
        self.assertEquals(5, wrapper.xyz)
        with self.assertRaises(RuntimeError) as cm:
            x = wrapper.abc
        wrapper.abc = 321
        with self.assertRaises(RuntimeError) as cm:
            x = wrapper.abc
        self.assertEquals(obj, wrapper._LX_obj)
        self.assertEquals(321, obj.abc)
        self.assertEquals(5, obj.xyz)
        
    def test_unwritable_attrs(self):
        class MyWrapper(WrapperBase):
            _LX_unwritable_attrs = set(('b',))
        obj = Struct()
        obj.a = 123
        obj.b = 789
        wrapper = MyWrapper(obj)
        self.assertEquals(123, wrapper.a)
        self.assertEquals(789, wrapper.b)
        wrapper.a = 5
        self.assertEquals(5, wrapper.a)
        wrapper.c = 2
        self.assertEquals(2, wrapper.c)
        with self.assertRaises(RuntimeError) as cm:
            wrapper.b = 9
        self.assertEquals(obj, wrapper._LX_obj)
        self.assertEquals(5, obj.a)
        self.assertEquals(789, obj.b)
        
#==============================================================================#
class ModuleWrapper_TestCase(LtdExec_TestCaseBase):
    def test_basic(self):
        import sys
        mod = ModuleWrapper('sys')
        self.assertEquals(sys.version_info, mod.version_info)
        self.assertTrue('_current_frames' in sys.__dict__)
        # by default, names with a leading underscore are not available
        self.assertTrue('_current_frames' not in mod._LX_names())
        
    def test_readable(self):
        import math
        settings = {'readable_names': set(('sin','cos',))}
        mod = ModuleWrapper('math', settings)
        self.assertEquals(math.sin, mod.sin)
        self.assertEquals(math.cos, mod.cos)
        self.assertTrue('tan' in math.__dict__)
        self.assertTrue('atan' in math.__dict__)
        self.assertTrue('tan' not in mod._LX_names())
        self.assertTrue('atan' not in mod._LX_names())
        self.assertEquals(2, len(mod._LX_names()))
        
    def test_unreadable(self):
        import math
        settings = {'unreadable_names': set(('tan','atan',))}
        mod = ModuleWrapper('math', settings)
        self.assertEquals(math.sin, mod.sin)
        self.assertEquals(math.cos, mod.cos)
        self.assertEquals(math.fabs, mod.fabs)
        self.assertTrue('tan' in math.__dict__)
        self.assertTrue('atan' in math.__dict__)
        self.assertTrue('tan' not in mod._LX_names())
        self.assertTrue('atan' not in mod._LX_names())
        
    def test_module_with_all(self):
        import csv
        #settings = {'readable_names': set(('sin','cos',))}
        mod = ModuleWrapper('csv')
        self.assertEquals(csv.writer, mod.writer)
        self.assertEquals(csv.reader, mod.reader)
        self.assertTrue('re' in csv.__dict__)
        self.assertTrue('re' not in mod._LX_names())
        self.assertTrue('_Dialect' in csv.__dict__)
        self.assertTrue('_Dialect' not in mod._LX_names())
        self.assertTrue('reduce' in csv.__dict__)
        self.assertTrue('reduce' not in mod._LX_names())
        
    def test_module_with_submodules(self):
        import os
        import os.path
        osmod = ModuleWrapper('os')
        self.assertTrue('path' in os.__dict__)
        self.assertTrue('path' not in osmod._LX_names())
        pathmod = ModuleWrapper('os.path')
        osmod._LX_add_submodule('os.path', pathmod)
        self.assertTrue('path' in osmod._LX_names())
        self.assertEquals(pathmod, osmod.path)

#==============================================================================#
