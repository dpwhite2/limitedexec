import ast
import sys
import __builtin__

from . import exceptions, config
from .source import Source
from .script import Script

#==============================================================================#
def compile(source, filename, dialect):
    """Compile a script using the given dialect.
       
       The `dialect` parameter may be a dialect class, a dialect class 
       instance, or the name of a previously registered dialect.
       """
    from .dialect import util as dialect_util
    dialect = dialect_util.get_dialect_object(dialect)
    return dialect.compile(source, filename)

#==============================================================================#
class BaseCompiler(object):
    """Base class for all compiler objects."""

    def __init__(self, dialect):
        from .dialect import util as dialect_util
        self.dialect = dialect_util.get_dialect_object(dialect)
        self.processor = dialect.Processor(dialect)

    def __call__(self, src, filename):
        """Compile the given source using this compiler's dialect."""
        assert isinstance(src, basestring)
        source = Source(src, filename)
        try:
            code = self.do_compile(src, filename)
        except SyntaxError:
            typ, e, tb = sys.exc_info()
            if e.filename == config.misc.DEFAULT_SCRIPT_FILE_NAME:
                e.filename = filename
                e.text = source[e.lineno] + '\n'
            raise exceptions.CompilationError((typ,e,tb), source, 
                                              sanitize=False)
        except:
            raise exceptions.CompilationError(sys.exc_info(), source, 
                                              sanitize=False)
        return self.script_factory(source, code)

    def do_compile(self, src, filename):
        """Compilation entry-point for derived classes.  The returned value is 
           a code object.  Concrete compiler implementations should override 
           this method """
        raise NotImplementedError()

    def compile_to_ast(self, src, filename, mode='exec'):
        """Compile a string to an abstract syntax tree."""
        return __builtin__.compile(src, filename, mode,
                                   flags=ast.PyCF_ONLY_AST)

    def compile_to_code(self, ast_tree, filename):
        """Compile an abstract syntax tree to a Python bytecode object."""
        if isinstance(ast_tree, ast.Module):
            mode = 'exec'
        elif isinstance(ast_tree, ast.Expression):
            mode = 'eval'
        else:
            raise RuntimeError('TODO')  # ValueError?
        return __builtin__.compile(ast_tree, filename, mode)

    def script_factory(self, source, code):
        return Script(code, source, self.dialect)


#==============================================================================#
class Compiler(BaseCompiler):

    def __init__(self, dialect):
        super(Compiler, self).__init__(dialect)

    def do_compile(self, src, filename):
        src = self.processor.process_source(src)
        ast_tree = self.compile_to_ast(src, filename)

        ast_tree = self.processor.process_ast(ast_tree)
        code = self.compile_to_code(ast_tree, filename)

        return code


#==============================================================================#
class SplitSourceCompiler(BaseCompiler):

    def __init__(self, dialect):
        super(SplitSourceCompiler, self).__init__(dialect)

    def do_compile(self, src, filename):
        src = processor.process_whole_source(src)
        sources = processor.split_source(src)

        trees = [self.do_single_compile(src, filename) for src in sources]

        ast_tree = self.processor.merge_asts(trees)
        ast_tree = self.processor.process_merged_ast(ast_tree)

        code = self.compile_to_code(ast_tree, filename)

        return code

    def do_single_compile(self, src, filename):
        src = self.processor.process_source(src)
        tree = self.compile_to_ast(src, filename)
        return self.processor.process_ast(tree)

#==============================================================================#

