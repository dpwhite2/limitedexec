import unittest
import sys
import traceback
import textwrap
import ast
import __builtin__

from ltdexec import exceptions

from .base import LtdExec_TestCaseBase

#==============================================================================#
class SanitizeTraceback_TestCase(LtdExec_TestCaseBase):
    def test_raw_traceback(self):
        filename = 'my_file'
        co = compile('raise RuntimeError()', filename=filename, mode='exec')
        try:
            eval(co)
            self.fail('Expected an exception.')
        except RuntimeError as e:
            tb = sys.exc_info()[2]
            tblist = exceptions.sanitize_traceback(tb, filename)
        except:
            self.fail('Expected a RuntimeError exception.')
            
        self.assertEquals(1, len(tblist))
        tb_file, tb_lineno, tb_func, tb_text = tblist[0]
        self.assertEquals('my_file', tb_file)
        self.assertEquals(1, tb_lineno)
        self.assertEquals('<module>', tb_func)
        self.assertEquals(None, tb_text)
    
    def test_preformatted_traceback(self):
        filename = 'my_file'
        co = compile('raise RuntimeError()', filename=filename, mode='exec')
        try:
            eval(co)
            self.fail('Expected an exception.')
        except RuntimeError as e:
            tb = traceback.extract_tb(sys.exc_info()[2])
            self.assertEquals(2, len(tb))
            tblist = exceptions.sanitize_traceback(tb, filename)
        except:
            self.fail('Expected a RuntimeError exception.')
            
        self.assertEquals(1, len(tblist))
        tb_file, tb_lineno, tb_func, tb_text = tblist[0]
        self.assertEquals('my_file', tb_file)
        self.assertEquals(1, tb_lineno)
        self.assertEquals('<module>', tb_func)
        self.assertEquals(None, tb_text)
        
        
    def test_multiple_calls_in_file(self):
        filename = 'my_file'
        src = '''\
        def throw_func():
            raise RuntimeError()
        def func():
            throw_func()
        func()
        '''
        src = textwrap.dedent(src)
        co = compile(src, filename=filename, mode='exec')
        globals = {}
        locals = globals
        try:
            eval(co, globals, locals)
            self.fail('Expected an exception.')
        except RuntimeError as e:
            tb = traceback.extract_tb(sys.exc_info()[2])
            self.assertEquals(4, len(tb))
            tblist = exceptions.sanitize_traceback(tb, filename)
            
        self.assertEquals(3, len(tblist))
        
        tb_file, tb_lineno, tb_func, tb_text = tblist[0]
        self.assertEquals('my_file', tb_file)
        self.assertEquals(5, tb_lineno)
        self.assertEquals('<module>', tb_func)
        self.assertEquals(None, tb_text)
        
        tb_file, tb_lineno, tb_func, tb_text = tblist[1]
        self.assertEquals('my_file', tb_file)
        self.assertEquals(4, tb_lineno)
        self.assertEquals('func', tb_func)
        self.assertEquals(None, tb_text)
        
        tb_file, tb_lineno, tb_func, tb_text = tblist[2]
        self.assertEquals('my_file', tb_file)
        self.assertEquals(2, tb_lineno)
        self.assertEquals('throw_func', tb_func)
        self.assertEquals(None, tb_text)
        
    def test_exception_in_ltdexec_library(self):
        # Check that modules within ltdexec really are stripped when the stack 
        # trace is sanitized.
        from ltdexec.dialect.registry import dialects
        filename = 'my_file'
        src = '''\
        def func():
            return dialects['not_a_dialect_name']  # this raises KeyError
        
        func()
        '''
        src = textwrap.dedent(src)
        co = compile(src, filename=filename, mode='exec')
        globals = { 'dialects': dialects, }
        locals = globals
        try:
            eval(co, globals, locals)
            self.fail('Expected an exception.')
        except KeyError as e:
            tb = traceback.extract_tb(sys.exc_info()[2])
            self.assertEquals(4, len(tb))
            tblist = exceptions.sanitize_traceback(tb, filename)
            
        self.assertEquals(2, len(tblist))
        
        tb_file, tb_lineno, tb_func, tb_text = tblist[0]
        self.assertEquals('my_file', tb_file)
        self.assertEquals(4, tb_lineno)
        self.assertEquals('<module>', tb_func)
        self.assertEquals(None, tb_text)
        
        tb_file, tb_lineno, tb_func, tb_text = tblist[1]
        self.assertEquals('my_file', tb_file)
        self.assertEquals(2, tb_lineno)
        self.assertEquals('func', tb_func)
        self.assertEquals(None, tb_text)
        
        
#