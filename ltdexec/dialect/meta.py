import sys
import collections


from . import registry
from .. import config, exceptions

#==============================================================================#
class Builder(object):
    def __init__(self, clsname, bases, attrs):
        self.clsname = clsname
        self.bases = bases
        self.attrs = attrs

    def __call__(self):
        """ Populate a class attributes dict with attributes. """
        self.check_attrs()
        self.set_defaults()
        self.process_flags()
        self.forbidden_names()
        self.forbidden_attrs()
        self.unassignable_names()
        self.unassignable_attrs()
        self.initialize_objects()
        return self.attrs

    #--------------------------------------------------------------------------#
    def inherit_value(self, attrname, default='throw'):
        """ Look in base classes for the given attribute.  If it is found, that
            value is returned.  If not, the default is returned.  If default is
            'throw', an exception is thrown instead of returning a value.
        """
        for base in self.bases:
            try:
                return getattr(base, attrname)
            except AttributeError:
                pass
        if default == 'throw':
            m = 'Attribute "{0}" could not be inherited.'.format(attrname)
            raise exceptions.InternalError(m)
        else:
            return default

    def set_name_list(self, listname, default):
        """ Set a 'name list' in the class attr dict.  If it is not defined for
            this class, search the base classes.  Also ensure the name list is
            an actual list.
        """
        attrs = self.attrs
        if listname not in attrs:
            names = self.inherit_value(listname, default)
            attrs[listname] = names[:]
        elif not isinstance(attrs[listname], list):
            attrs[listname] = list(attrs[listname])
        return attrs[listname]

    def check_flag(self, flag, name, namelist):
        """ Check that the contents of a name list and a flag both agree. """
        allowname = self.attrs.get(flag, self.inherit_value(flag))
        if not allowname and name not in self.attrs[namelist]:
            self.attrs[namelist].append(name)
        elif name in self.attrs[namelist]:
            self.attrs[flag] = False

    def check_builtin_flag(self, flag, name):
        self.check_flag(flag, name, 'forbidden_names')

    def check_attribute_flag(self, flag, name):
        self.check_flag(flag, name, 'forbidden_attrs')

    def set_flag(self, traits):
        """ Scans the parent flags for a value.  Note: this is different than
            checking base classes. """
        for parentname in traits.parents:
            if parentname in self.attrs:
                self.attrs[traits.name] = self.attrs[parentname]
                return

    #--------------------------------------------------------------------------#
    def check_attrs(self):
        """ Check that attributes meet preconditions. """
        # TODO: raise a specific exception; don't just assert
        if 'name' in self.attrs:
            assert isinstance(self.attrs['name'], basestring)
        if 'allowed_imports' in self.attrs:
            assert isinstance(self.attrs['allowed_imports'], dict)
        if 'objects' in self.attrs:
            assert isinstance(self.attrs['objects'], dict)
        assert 'forbidden_names_set' not in self.attrs
        assert 'forbidden_attrs_set' not in self.attrs
        assert 'unassignable_names_set' not in self.attrs
        assert 'unassignable_attrs_set' not in self.attrs

    def set_defaults(self):
        """ Set class default values if they are not defined. """
        if not self.attrs.get("name"):
            module = self.attrs["__module__"]
            self.attrs["name"] = '.'.join([sys.modules[module].__name__,
                                          self.clsname])

    def process_flags(self):
        """ Checks all known leaf flags to see if they are set.

            It will look at parent flags for a value when it finds a flag that
            is not set.  If a flag is not set, and no parent flags are set,
            then nothing is done here.  This lets allows the flag value to be
            picked up using Python's normal inheritence mechanism.
        """
        for traits in config.flags.leafflag_traits.itervalues():
            if traits.name not in self.attrs:
                self.set_flag(traits)

    def forbidden_names(self):
        DEFAULT_FORBIDDEN_NAMES = config.names.DEFAULT_FORBIDDEN_NAMES
        self.set_name_list('forbidden_names', DEFAULT_FORBIDDEN_NAMES)

        for traits in config.flags.builtin_leafflag_traits.itervalues():
            self.check_builtin_flag(traits.name, traits.builtin_name)

        self.attrs['forbidden_names_set'] = set(self.attrs['forbidden_names'])
        ALWAYS_FORBIDDEN_NAMES = config.names.ALWAYS_FORBIDDEN_NAMES
        self.attrs['forbidden_names_set'].update(ALWAYS_FORBIDDEN_NAMES)

    def forbidden_attrs(self):
        DEFAULT_FORBIDDEN_ATTRS = config.names.DEFAULT_FORBIDDEN_ATTRS
        self.set_name_list('forbidden_attrs', DEFAULT_FORBIDDEN_ATTRS)

        for traits in config.flags.attribute_leafflag_traits.itervalues():
            self.check_attribute_flag(traits.name, traits.attr_name)

        self.attrs['forbidden_attrs_set'] = set(self.attrs['forbidden_attrs'])
        ALWAYS_FORBIDDEN_ATTRS = config.names.ALWAYS_FORBIDDEN_ATTRS
        self.attrs['forbidden_attrs_set'].update(ALWAYS_FORBIDDEN_ATTRS)

    def unassignable_names(self):
        DEFAULT_UNASSIGNABLE_NAMES = config.names.DEFAULT_UNASSIGNABLE_NAMES
        self.set_name_list('unassignable_names', DEFAULT_UNASSIGNABLE_NAMES)

        objects = self.attrs.get('objects', self.inherit_value('objects', None))
        if objects:
            self.attrs['unassignable_names'].extend(objects.keys())

        self.attrs['unassignable_names_set'] = \
                set(self.attrs['unassignable_names'])
        ALWAYS_UNASSIGNABLE_NAMES = config.names.ALWAYS_UNASSIGNABLE_NAMES
        self.attrs['unassignable_names_set'].update(ALWAYS_UNASSIGNABLE_NAMES)

    def unassignable_attrs(self):
        DEFAULT_UNASSIGNABLE_ATTRS = config.names.DEFAULT_UNASSIGNABLE_ATTRS
        self.set_name_list('unassignable_attrs', DEFAULT_UNASSIGNABLE_ATTRS)

        self.attrs['unassignable_attrs_set'] = \
                set(self.attrs['unassignable_attrs'])
        ALWAYS_UNASSIGNABLE_ATTRS = config.names.ALWAYS_UNASSIGNABLE_ATTRS
        self.attrs['unassignable_attrs_set'].update(ALWAYS_UNASSIGNABLE_ATTRS)

    def initialize_objects(self):
        # Add some default objects that should always be present.
        if 'builtin_objects' not in self.attrs:
            self.attrs['builtin_objects'] = {}



#==============================================================================#
class DialectMeta(type):
    """ Meta class for dialects.  This ensures that Dialects possess all the
        attributes the rest of the library expects.  It also registers the new
        dialect.
    """
    def __new__(mcls, clsname, bases, attrs):
        from ..wrapper import deffunc

        new = super(DialectMeta, mcls).__new__
        attrs['_locked'] = False
        builder = Builder(clsname, bases, attrs)
        attrs = builder()
        dialect_cls = new(mcls, clsname, bases, attrs)

        dialect_cls.builtin_objects['getattr'] = deffunc(dialect_cls.getattr)
        dialect_cls.builtin_objects['hasattr'] = deffunc(dialect_cls.hasattr)
        dialect_cls.builtin_objects['setattr'] = deffunc(dialect_cls.setattr)
        dialect_cls.builtin_objects['delattr'] = deffunc(dialect_cls.delattr)

        registry.dialects.register(dialect_cls)
        dialect_cls = registry.dialects.get_class(dialect_cls.name)

        dialect_cls._locked = True
        return dialect_cls

    def __call__(cls, *args, **kwargs):
        # Constructing an instance of the class always returns the same
        # instance.  It is the registry's job to maintain the single instance.
        # The registry will call _construct() when it constructs the instance.
        return registry.dialects[cls.name]

    def __setattr__(cls, name, value):
        if cls._locked:
            raise RuntimeError('A Dialect is immutable.  It cannot be modified once created.')
        else:
            super(DialectMeta, cls).__setattr__(name, value)

    def _construct(cls, *args, **kwargs):
        # Construct an instance of the class.  This is separated from
        # __call__() on purpose.  It is called from the registry when an
        # instance needs to be created.
        inst = super(DialectMeta, cls).__call__(*args, **kwargs)
        inst._locked_inst = True
        return inst

#==============================================================================#