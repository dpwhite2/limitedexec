import threading
import uuid
import types
import functools
import sys

from . import config

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
        if name.startswith(config.names.LTDEXEC_PRIVATE_PREFIX):
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
        if name.startswith(config.names.LTDEXEC_PRIVATE_PREFIX):
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


class ModuleWrapper(object):
    def __init__(self, modname, module_settings=None):
        # options:  allow all names, forbid names not in __all__, 
        #   forbid names beginning with underscore, allow listed names, 
        #   forbid listed names, forbid indirect modules
        module_settings = module_settings or {}
        readable_names = module_settings.get('readable_names', set())
        unreadable_names = module_settings.get('unreadable_names', set())
        
        forbid_underscore_names = module_settings.get('forbid_underscore_names', True)
        allow_names_in_all = module_settings.get('allow_names_in_all', True)
        
        self._LX_modname = modname
        __import__(modname, globals(), locals(), [], 0)
        mod = sys.modules[modname]
        members = {}
        for k,v in mod.__dict__.iteritems():
            if k == '__all__':
                continue
            elif readable_names:
                if k in readable_names and not isinstance(v, types.ModuleType):
                    members[k] = v
            else:
                if isinstance(v, types.ModuleType):
                    pass
                elif k in unreadable_names:
                    pass
                elif forbid_underscore_names and k.startswith('_'):
                    pass
                elif (allow_names_in_all and
                  (('__all__' in mod.__dict__ and k not in mod.__all__) or
                   ('__all__' not in mod.__dict__ and k.startswith('_')))):
                    pass
                else:
                    members[k] = v
        self._LX_members = members
        
    def _LX_names(self):
        return self._LX_members.keys()
        
    def _LX_add_submodule(self, modname, module):
        assert modname.startswith(self._LX_modname)
        assert modname == (self._LX_modname + '.' + modname.rpartition('.')[2])
        name = modname.rpartition('.')[2]
        self._LX_members[name] = module
        
    def __getattribute__(self, name):
        super_getattr = super(ModuleWrapper, self).__getattribute__
        if name.startswith(config.names.LTDEXEC_PRIVATE_PREFIX):
            return super_getattr(name)
        else:
            return super_getattr('_LX_members')[name]
        
    def __setattr__(self, name, value):
        if name.startswith(config.names.LTDEXEC_PRIVATE_PREFIX):
            super(ModuleWrapper, self).__setattr__(name, value)
        else:
            raise RuntimeError('TODO')
            
        


#==============================================================================#
