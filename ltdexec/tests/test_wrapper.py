import unittest

from ltdexec.wrapper import WrapperBase, wrap_class

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
