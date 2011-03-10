from . import registry, defobjects
from . import base

Dialect = base.Dialect
deffunc = defobjects.deffunc
defname = defobjects.defname

del defobjects
del base
