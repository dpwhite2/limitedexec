from __future__ import absolute_import

import exceptions

#==============================================================================#
class Exception(exceptions.Exception):
    pass


class SyntaxError(exceptions.SyntaxError, Exception):
    def __init__(self, msg, filename, lineno, offset, text, reason=None):
        super(SyntaxError, self).__init__(msg)
        self.filename = filename
        self.lineno = lineno
        self.offset = offset
        self.text = text
        self.reason = reason  # this is used in testing


class InternalError(Exception):
    """ A library-internal invariant was violated. """
    pass


#==============================================================================#
