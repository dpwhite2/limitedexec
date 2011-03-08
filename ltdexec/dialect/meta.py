import sys

from .. import config

#==============================================================================#
class Builder(object):
    def __init__(self, clsname, bases, attrs):
        self.clsname = clsname
        self.bases = bases
        self.attrs = attrs

    def __call__(self):
        """ Populate a class attributes dict with attributes. """
        self.set_defaults()
        self.process_flags()
        self.forbidden_names()
        self.forbidden_attrs()
        self.unassignable_names()
        self.unassignable_attrs()
        return self.attrs

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
        if default=='throw':
            raise RuntimeError('Attribute "{0}" could not be inherited.'.format(attrname))
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
        for parentname in traits.parents:
            if parentname in self.attrs:
                self.attrs[traits.name] = self.attrs[parentname]
                return

    def set_defaults(self):
        """ Set class default values if they are not defined. """
        if not self.attrs.get("name"):
            module = self.attrs["__module__"]
            self.attrs["name"] = '.'.join([sys.modules[module].__name__, self.clsname])

    def process_flags(self):
        for traits in config.flags.leafflag_traits.itervalues():
            if traits.name not in self.attrs:
                self.set_flag(traits)

    def forbidden_names(self):
        self.set_name_list('forbidden_names', config.names.DEFAULT_FORBIDDEN_NAMES)

        for traits in config.flags.builtin_leafflag_traits.itervalues():
            self.check_builtin_flag(traits.name, traits.builtin_name)

        self.attrs['forbidden_names_set'] = set(self.attrs['forbidden_names'])
        self.attrs['forbidden_names_set'].update(config.names.ALWAYS_FORBIDDEN_NAMES)  # ALWAYS_FORBIDDEN_NAMES = internal names

    def forbidden_attrs(self):
        self.set_name_list('forbidden_attrs', config.names.DEFAULT_FORBIDDEN_ATTRS)

        for traits in config.flags.attribute_leafflag_traits.itervalues():
            self.check_attribute_flag(traits.name, traits.attr_name)

        self.attrs['forbidden_attrs_set'] = set(self.attrs['forbidden_attrs'])
        self.attrs['forbidden_attrs_set'].update(config.names.ALWAYS_FORBIDDEN_ATTRS)  # ALWAYS_FORBIDDEN_ATTRS = internal attributes

    def unassignable_names(self):
        self.set_name_list('unassignable_names', config.names.DEFAULT_UNASSIGNABLE_NAMES)

        objects = self.attrs.get('objects', self.inherit_value('objects', None))
        if objects:
            self.attrs['unassignable_names'].extend(objects.keys())

        self.attrs['unassignable_names_set'] = set(self.attrs['unassignable_names'])
        self.attrs['unassignable_names_set'].update(config.names.ALWAYS_UNASSIGNABLE_NAMES)

    def unassignable_attrs(self):
        self.set_name_list('unassignable_attrs', config.names.DEFAULT_UNASSIGNABLE_ATTRS)

        self.attrs['unassignable_attrs_set'] = set(self.attrs['unassignable_attrs'])
        self.attrs['unassignable_attrs_set'].update(config.names.ALWAYS_UNASSIGNABLE_ATTRS)


#==============================================================================#
class DialectMeta(type):
    def __new__(mcls, clsname, bases, attrs):
        new = super(DialectMeta, mcls).__new__
        builder = Builder(clsname, bases, attrs)
        attrs = builder()
        langd = new(mcls, clsname, bases, attrs)

        # TODO: register LangDescriptor

        return langd

#==============================================================================#
