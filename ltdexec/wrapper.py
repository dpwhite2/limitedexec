import threading
import uuid
import types
import functools

#==============================================================================#
_local = threading.local()
_local.key_stack = []

def create_envkey():
    if not _local.key_stack:
        key = uuid.uuid4().hex
    else:
        key = _local.key_stack[-1]
    _local.key_stack.append(key)
    return key

def pop_envkey(key):
    if key != _local.key_stack[-1]:
        raise RuntimeError('TODO')
    _local.key_stack.pop()

#==============================================================================#
# The following are used when defining what objects appear in a Dialect's
# namespace.

class defname(object):
    def __init__(self, callable, args=None, kwargs=None, method_on_close=None):
        self.callable = callable
        self.args = args or []
        self.kwargs = kwargs or {}
        self.method_on_close = method_on_close or ''

    def construct(self):
        return self.callable(*self.args, **self.kwargs)


def wrap_function(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return _wrapper


class deffunc(defname):
    def __init__(self, function):
        super(deffunc, self).__init__(wrap_function, args=[function])

#==============================================================================#
class definstance(defname):
    def __init__(self, callable, args=None, kwargs=None, readable_attrs=None, 
                 writable_attrs=None, unreadable_attrs=None, 
                 unwritable_attrs=None, method_on_close=None):
        super(definstance, self).__init__(self, callable, args, kwargs, 
                                          method_on_close)
        # create instance of callable with protected attrs
        # callable must be a class.
        assert isinstance(callable, type)
        # create subclass of WrapperBase, InstanceWrapper.
        @wrap_class(readable_attrs=readable_attrs, 
                       writable_attrs=writable_attrs, 
                       unreadable_attrs=unreadable_attrs, 
                       unwritable_attrs=unwritable_attrs)
        class InstanceWrapper(WrapperBase):
            pass
        self.InstanceWrapper = InstanceWrapper
        
    def construct(self):
        # when construct is called, create the instance of callable... 
        obj = super(definstance, self).construct()
        # then wrap it in an instance of InstanceWrapper.
        return self.InstanceWrapper(obj)
        
    
#==============================================================================#

def wrap_class(readable_attrs=None, writable_attrs=None, 
                   unreadable_attrs=None, unwritable_attrs=None):
    def _inner(cls):
        assert isinstance(cls, WrapperBase)
        if readable_attrs is not None:
            cls._LX_readable_attrs = readable_attrs
        if writable_attrs is not None:
            cls._LX_writable_attrs = writable_attrs
        if unreadable_attrs is not None:
            cls._LX_unreadable_attrs = unreadable_attrs
        if unwritable_attrs is not None:
            cls._LX_unwritable_attrs = unwritable_attrs
            
        cls._LX_readable_attrs = cls._LX_readable_attrs | cls._LX_writable_attrs
        cls._LX_unwritable_attrs = cls._LX_unreadable_attrs | cls._LX_unwritable_attrs
        return cls
    return _inner


#==============================================================================#
class WrapperBase(object):
    _LX_readable_attrs = set()
    _LX_writable_attrs = set()
    _LX_unreadable_attrs = set()
    _LX_unwritable_attrs = set()
    
    def __init__(self, obj):
        self._LX_obj = obj
        
    def __getattribute__(self, name):
        super_getattr = super(WrapperBase, self).__getattribute__
        if name.startswith('_LX_'):
            return super_getattr(name)
        else:
            if super_getattr('_LX_readable_attrs'):
                if name in super_getattr('_LX_readable_attrs'):
                    obj = super_getattr('_LX_obj')
                    return getattr(obj, name)
                else:
                    raise RuntimeError('TODO')
            elif super_getattr('_LX_unreadable_attrs'):
                if name not in super_getattr('_LX_unreadable_attrs'):
                    obj = super_getattr('_LX_obj')
                    return getattr(obj, name)
                else:
                    raise RuntimeError('TODO')
            else:
                obj = super_getattr('_LX_obj')
                return getattr(obj, name)
    
    def __setattr__(self, name, value):
        if name.startswith('_LX_'):
            return super(WrapperBase, self).__setattr__(name, value)
        else:
            super_getattr = super(WrapperBase, self).__getattribute__
            if super_getattr('_LX_writable_attrs'):
                if name in super_getattr('_LX_writable_attrs'):
                    obj = super_getattr('_LX_obj')
                    return setattr(obj, name, value)
                else:
                    raise RuntimeError('TODO')
            elif super_getattr('_LX_unwritable_attrs'):
                if name not in super_getattr('_LX_unwritable_attrs'):
                    obj = super_getattr('_LX_obj')
                    return setattr(obj, name, value)
                else:
                    raise RuntimeError('TODO')
            else:
                obj = super_getattr('_LX_obj')
                return setattr(obj, name, value)


# class WrapperBase(object):
    # _LX_delay_lock = False
    # _LX_read_lockable = False
    # _LX_write_lockable = True

    # def __init__(self):
        # self._LX_lockable = self._LX_read_lockable or self._LX_write_lockable
        # if self._LX_lockable and not self._LX_delay_lock and _local.key_stack:
            # self._LX_lock(_local.key_stack[-1])

    # def _LX_lock(self, key):
        # if self._LX_lockable:
            # if not key:
                # raise RuntimeError('TODO')
            # if self._LX_key:
                # raise RuntimeError('TODO')
            # if key != _local.key_stack[-1]:
                # raise RuntimeError('TODO')
            # self._LX_key = key

    # def _LX_unlock(self, other):
        # if self._LX_lockable:
            # key = self._LX_key
            # if key == other == _local.key_stack[-1]:
                # self._LX_key = None
            # else:
                # raise RuntimeError('TODO')

    # def _LX_check_read_lock(self):
        # if self._LX_read_lockable and self._LX_key:
            # raise RuntimeError('TODO')


# class Wrapper(object):
    # def __init__(self, obj):
        # super(Wrapper, self).__setattr__('_LX_obj', obj)
        # super(Wrapper, self).__init__()

    # def __getattribute__(self, name):
        # if name.startswith('_LX_'):
            # return super(Wrapper, self).__getattribute__(name)
        # try:
            # val = super(Wrapper, self).__getattribute__(name)
        # except AttributeError:
            # readable = super(Wrapper, self).__getattribute__('_LX_readable_attrs')
            # unreadable = super(Wrapper, self).__getattribute__('_LX_unreadable_attrs')
            # if readable and name not in readable:
                # raise RuntimeError('TODO')
            # elif name in unreadable:
                # raise RuntimeError('TODO')
            # obj = super(Wrapper, self).__getattribute__('_LX_obj')
            # val = getattr(obj, name)
        # return val

    # def __setattr__(self, name, val):
        # if name.startswith('_LX_'):
            # super(Wrapper, self).__setattr__(name, val)
            # return
        # try:
            # super(Wrapper, self).__getattribute__(name)
            # super(Wrapper, self).__setattr__(name, val)
        # except AttributeError:
            # writeable = super(Wrapper, self).__getattribute__('_LX_writeable_attrs')
            # unwriteable = super(Wrapper, self).__getattribute__('_LX_unwriteable_attrs')
            # if writeable and name not in writeable:
                # raise RuntimeError('TODO')
            # elif name in unwriteable:
                # raise RuntimeError('TODO')
            # obj = super(Wrapper, self).__getattribute__('_LX_obj')
            # setattr(obj, name, val)


# class WrapperBase(object):
    # _LX_lockable = True
    # _LX_delay_lock = False

    # def __init__(self):
        # if self._LX_lockable and not self._LX_delay_lock and _local.key_stack:
            # self._LX_lock(_local.key_stack[-1])

    # def _LX_lock(self, key):
        # if super(WrapperBase, self).__getattribute__('_LX_lockable'):
            # if not key:
                # raise RuntimeError('TODO')
            # if self._LX_key:
                # raise RuntimeError('TODO')
            # self._LX_key = key

    # def _LX_unlock(self, other):
        # if super(WrapperBase, self).__getattribute__('_LX_lockable'):
            # key = super(WrapperBase, self).__getattribute__('_LX_key')
            # if key == other == _local.key_stack[-1]:
                # super(WrapperBase, self).__setattr__('_LX_key', None)
            # else:
                # raise RuntimeError('TODO')

    # def __setattr__(self, name, val):
        # if name.startswith('_LX_') or not self._LX_key:
            # super(WrapperBase, self).__setattr__(name, val)
        # else:
            # raise RuntimeError('TODO')


#==============================================================================#
