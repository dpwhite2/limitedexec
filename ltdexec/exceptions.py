from __future__ import absolute_import

import exceptions
import types
import traceback
import itertools
import re

from . import config

#==============================================================================#
class Exception(exceptions.Exception):
    pass

#==============================================================================#
class SyntaxError(exceptions.SyntaxError, Exception):
    def __init__(self, msg, filename, lineno, offset, text, reason=None):
        super(SyntaxError, self).__init__(msg,(filename, lineno, offset, text))
        #self.filename = filename
        #self.lineno = lineno
        #self.offset = offset
        #self.text = text
        self.reason = reason  # this is used in testing
        
        
    # Yes, these filename and text properties are hackish.  But, I tried 
    # several other ways and was unable to modify the properties on the 
    # *underlying* builtin SyntaxError object.  For one, assigning to 
    # super(...).filename did not work (though reading from it does).
    def set_filename(self, newfilename):
        msg = self.args[0]
        filename,lineno,offset,text = self.args[1]
        super(SyntaxError, self).__init__(msg,(newfilename, lineno, offset, text))
    def get_filename(self):
        return super(SyntaxError, self).filename
    filename = property(get_filename, set_filename)
        
    def set_text(self, newtext):
        msg = self.args[0]
        filename,lineno,offset,text = self.args[1]
        super(SyntaxError, self).__init__(msg,(filename, lineno, offset, newtext))
    def get_text(self):
        return super(SyntaxError, self).text
    text = property(get_text, set_text)
        
    def __str__(self):
        return self.args[0]

#==============================================================================#
class InternalError(Exception):
    """ A library-internal invariant was violated, likely by a library-internal 
        operation. 
    """
    pass
    
class ImmutableError(Exception):
    """ An attempt was made to modify an immutable object. """
    pass
    
class DialectSetupError(Exception):
    """ An error was detected in a Dialect configuration. """
    pass

class UnregisteredDialectError(Exception):
    """ An attempt was made to retrieve an unregistered Dialect from the 
        registry. 
    """
    pass
    
#==============================================================================#
class LXPrivateObjectError(Exception):
    """ An attempt was made to retrieve a LimitedExec internal variable at 
        runtime.  (Compile time violations of this rule are raised as 
        SyntaxErrors.) 
    """
    pass
    
class LXPrivateNameError(LXPrivateObjectError):
    pass

class LXPrivateAttrError(LXPrivateObjectError):
    pass

#==============================================================================#
class LXNameError(Exception):
    pass

class ForbiddenNameError(LXNameError):
    pass
    
class ForbiddenAttrError(LXNameError):
    pass
    
class UnassignableNameError(LXNameError):
    pass
    
class UnassignableAttrError(LXNameError):
    pass

#==============================================================================#
re_remove_path = re.compile(r'ltdexec[\\/](?!tests[\\/])')

def check_tb_entry(entry):
    filename = entry[0]
    return re_remove_path.search(filename) is None
    
def filename_no_match(filename):
    def _inner(entry):
        return entry[0] != filename
    return _inner
    
def sanitize_traceback(tb, filename):
    # Expects a traceback object, or a list of preprocessed trace entries such 
    # as produced by traceback.extract_tb().
    if isinstance(tb, types.TracebackType):
        tb = traceback.extract_tb(tb)
    i = itertools
    newtb = [entry for entry in 
                i.ifilter( check_tb_entry, 
                           i.dropwhile(filename_no_match(filename), tb)
                         )]
    return newtb
    
def fix_missing_traceback_text(tb, source):
    # Expects a traceback object, or a list of preprocessed trace entries such 
    # as produced by traceback.extract_tb().
    if isinstance(tb, types.TracebackType):
        tb = traceback.extract_tb(tb)
    def _fix_entry(entry):
        if entry[0] == source.filename:
            lineno = entry[1]
            entry = entry[:3] + (source[lineno],)
        return entry
    return [_fix_entry(entry) for entry in tb]
    
def fix_missing_traceback_filename(tb, source):
    # Expects a traceback object, or a list of preprocessed trace entries such 
    # as produced by traceback.extract_tb().
    if isinstance(tb, types.TracebackType):
        tb = traceback.extract_tb(tb)
    def _fix_entry(entry):
        if entry[0] == config.misc.DEFAULT_SCRIPT_FILE_NAME:
            entry = (source.filename,) + entry[1:]
        return entry
    return [_fix_entry(entry) for entry in tb]
    

class WrappedException(Exception):
    def __init__(self, exc_info, source, sanitize=True):
        self.exc_info = exc_info
        self.sanitize = sanitize
        self.source = source
        
    def extract_tb(self):
        tb = traceback.extract_tb(self.exc_info[2])
        #if isinstance(self.exc_info[1], SyntaxError):
        #    exc_val = self.exc_info[1]
        #    filename = exc_val.filename
        #    lineno = exc_val.lineno
        #    funcname = ''
        #    text = exc_val.text
        #    tb.append((filename, lineno, funcname, text))
        tb = fix_missing_traceback_filename(tb, self.source)
        if self.sanitize:
            tb = sanitize_traceback(tb, self.source.filename)
        return fix_missing_traceback_text(tb, self.source)
        
    def format_tb(self):
        tb = self.extract_tb()
        return traceback.format_list(tb)
    
    def heading(self):
        return 'Traceback (most recent call last):\n'
        
    def format_exception_only(self):
        ty, val, tb = self.exc_info
        return traceback.format_exception_only(ty, val)
        
    def format_exception(self):
        return ([self.heading()] + self.format_tb() + 
                self.format_exception_only())
                
    def __str__(self):
        return ''.join(self.format_exception())
        

class CompilationError(WrappedException):
    def __init__(self, exc_info, source, sanitize=True):
        super(CompilationError, self).__init__(exc_info, source, sanitize)

class ExecutionError(WrappedException):
    def __init__(self, exc_info, source, sanitize=True, 
                 globals=None, locals=None):
        super(ExecutionError, self).__init__(exc_info, source, sanitize)
        self.globals = globals or {}
        self.locals = locals or {}

    
    

#==============================================================================#
