import threading
import uuid

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
def object_wrapper(readable_attrs=None, writeable_attrs=None):
    pass

#==============================================================================#

class WrapperBase(object):
    _LX_delay_lock = False
    _LX_read_lockable = False
    _LX_write_lockable = True

    def __init__(self):
        self._LX_lockable = self._LX_read_lockable or self._LX_write_lockable
        if self._LX_lockable and not self._LX_delay_lock and _local.key_stack:
            self._LX_lock(_local.key_stack[-1])

    def _LX_lock(self, key):
        if self._LX_lockable:
            if not key:
                raise RuntimeError('TODO')
            if self._LX_key:
                raise RuntimeError('TODO')
            if key != _local.key_stack[-1]:
                raise RuntimeError('TODO')
            self._LX_key = key

    def _LX_unlock(self, other):
        if self._LX_lockable:
            key = self._LX_key
            if key == other == _local.key_stack[-1]:
                self._LX_key = None
            else:
                raise RuntimeError('TODO')

    def _LX_check_read_lock(self):
        if self._LX_read_lockable and self._LX_key:
            raise RuntimeError('TODO')


class Wrapper(object):
    def __init__(self, obj):
        super(Wrapper, self).__setattr__('_LX_obj', obj)
        super(Wrapper, self).__init__()

    def __getattribute__(self, name):
        if name.startswith('_LX_'):
            return super(Wrapper, self).__getattribute__(name)
        try:
            val = super(Wrapper, self).__getattribute__(name)
        except AttributeError:
            readable = super(Wrapper, self).__getattribute__('_LX_readable_attrs')
            unreadable = super(Wrapper, self).__getattribute__('_LX_unreadable_attrs')
            if readable and name not in readable:
                raise RuntimeError('TODO')
            elif name in unreadable:
                raise RuntimeError('TODO')
            obj = super(Wrapper, self).__getattribute__('_LX_obj')
            val = getattr(obj, name)
        return val

    def __setattr__(self, name, val):
        if name.startswith('_LX_'):
            super(Wrapper, self).__setattr__(name, val)
            return
        try:
            super(Wrapper, self).__getattribute__(name)
            super(Wrapper, self).__setattr__(name, val)
        except AttributeError:
            writeable = super(Wrapper, self).__getattribute__('_LX_writeable_attrs')
            unwriteable = super(Wrapper, self).__getattribute__('_LX_unwriteable_attrs')
            if writeable and name not in writeable:
                raise RuntimeError('TODO')
            elif name in unwriteable:
                raise RuntimeError('TODO')
            obj = super(Wrapper, self).__getattribute__('_LX_obj')
            setattr(obj, name, val)


class WrapperBase(object):
    _LX_lockable = True
    _LX_delay_lock = False

    def __init__(self):
        if self._LX_lockable and not self._LX_delay_lock and _local.key_stack:
            self._LX_lock(_local.key_stack[-1])

    def _LX_lock(self, key):
        if super(WrapperBase, self).__getattribute__('_LX_lockable'):
            if not key:
                raise RuntimeError('TODO')
            if self._LX_key:
                raise RuntimeError('TODO')
            self._LX_key = key

    def _LX_unlock(self, other):
        if super(WrapperBase, self).__getattribute__('_LX_lockable'):
            key = super(WrapperBase, self).__getattribute__('_LX_key')
            if key == other == _local.key_stack[-1]:
                super(WrapperBase, self).__setattr__('_LX_key', None)
            else:
                raise RuntimeError('TODO')

    def __setattr__(self, name, val):
        if name.startswith('_LX_') or not self._LX_key:
            super(WrapperBase, self).__setattr__(name, val)
        else:
            raise RuntimeError('TODO')


#==============================================================================#
class FunctionWrapper(object):
    def __init__(self, func):
        self._LX_func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
        self._LX_locked = True

    def __setattr__(self, name, val):
        if name.startswith('_LX_'):
            super(FunctionWrapper, self).__setattr__(name, val)
        elif self._LX_locked:
            raise RuntimeError('TODO')
        elif name.startswith('__'):
            super(FunctionWrapper, self).__setattr__(name, val)
        else:
            setattr(self._LX_func, name, val)

    def __call__(self, *args, **kwargs):
        return self._LX_func(*args, **kwargs)


#==============================================================================#
