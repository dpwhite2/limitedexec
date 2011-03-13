import uuid
import sys

from . import wrapper
from .dialect import util as dialect_util

#==============================================================================#
class Environment(object):
    """ A script is executed in an Environment.  This contains the globals and
        locals dicts that are available to the script when it begins execution.
    """
    def __init__(self, objects, globals):
        assert isinstance(objects, dict)
        assert isinstance(globals, dict)

        self.startup_objects = []
        self.key = wrapper.create_envkey()
        _globals = {}
        try:
            for name, objdef in objects.iteritems():
                _globals[name] = objdef.construct()
                self.startup_objects.append(
                    (_globals[name], {'method_on_close': objdef.method_on_close,},)
                    )
        except:
            exc = sys.exc_info()
            try:
                self._close_startup_objects()
            except:
                pass
            wrapper.pop_envkey(self.key)
            raise exc[0], exc[1], exc[2]

        _globals.update(globals)

        # locals and globals must refer to the same dict.  Otherwise, 
        # module-scope names are only placed in the locals dict.  In that case, 
        # module-scope names could not be used from within local scopes.
        self.globals = _globals
        self.locals = self.globals
        
        self.modules = {}
        self.module_settings = {}
        
        self.globals['_LX_import_module'] = self.import_module
                
    def _close_startup_object(self, obj, info):
        try:
            obj._LX_unlock(self.key)
        except AttributeError:
            pass
        finally:
            getattr(obj, info['method_on_close'], lambda: None)()
                
    def _close_startup_objects(self):
        exc = None
        for obj, info in self.startup_objects:
            try:
                self._close_startup_object(obj, info)
            except:
                exc = sys.exc_info()
        self.startup_objects = []
        if exc:
            raise exc[0], exc[1], exc[2]

    def close(self):
        """ Called when a script has completed execution.  Any cleanup required
            by the environment members should be performed during this call.
        """
        key = self.key
        exc = None
        try:
            self._close_startup_objects()
        except:
            exc = sys.exc_info()
        self.globals.pop('_LX_import_module')  # _LX_import_module is an implementation detail
        wrapper.pop_envkey(key)
        if exc:
            raise exc[0], exc[1], exc[2]

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        
    def import_module(self, modname, asname=None, froms=None):
        """Load the given module and any parent modules.  The top-most module 
           is placed in the Environment's globals dict.  The child module(s) 
           can be accessed through their parents' attributes.
        """
        self.load_module(modname)
        if froms:
            mod = self.modules[modname]
            for name,asname in froms:
                asname = asname or name
                self.globals[asname] = getattr(mod, name)
        elif asname:
            mod = self.modules[modname]
            self.globals[asname] = mod
        else:
            toplevel = modname.partition('.')[0]
            mod = self.modules[toplevel]
            self.globals[toplevel] = mod

    def load_module(self, modname):
        """Load the given module, and parent modules.  All are placed in the 
           Environment's modules dict.  (To be accessible to scripts, the 
           module must be imported.)"""
        try:
            return self.modules[modname]
        except KeyError:
            pass
        mod = wrapper.ModuleWrapper(modname, self.module_settings.get(modname,{}))
        parentname = modname.rpartition('.')[0]
        if parentname:
            parent = self.load_module(parentname)
            parent._LX_add_submodule(modname, mod)
        self.modules[modname] = mod
        return mod


#==============================================================================#
class EnvironmentFactory(object):
    """ A Script contains an EnvironmentFactory, which it uses to construct the
        Environment each time it runs.
    """
    Environment = Environment

    def __init__(self, dialect):
        dialect = dialect_util.get_dialect_object(dialect)
        try:
            self.objects = dialect.objects
        except AttributeError:
            self.objects = {}
        self.objects.update(dialect.builtin_objects)

    def __call__(self, globals=None):
        """ Create an Environment object. """
        globals = globals or {}
        return self.Environment(self.objects, globals)


#==============================================================================#



