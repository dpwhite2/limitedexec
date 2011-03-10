import ast
import __builtin__

from .source import Source

#==============================================================================#
def compile(source, filename, dialect):
    from .dialect import Dialect, dialects
    
    if isinstance(dialect, basestring):
        dialect = dialects[dialect]
    elif isinstance(dialect, type):
        dialect = dialects[dialect.name]
    assert isinstance(dialect, Dialect)
    compiler = dialect.compiler_instance()
    return compiler(source, filename)

#==============================================================================#
class BaseCompiler(object):

    def __init__(self, dialect):
        self.dialect = dialect
        self.processor = dialect.Processor(dialect)

    def __call__(self, src, filename):
        assert isinstance(src, basestring)
        source = Source(src, filename)
        try:
            code = self.do_compile(src, filename)
        except:
            # TODO: reraise exception with additional info
            raise
        script = self.script_factory(source, code)
        return script

    def compile_to_ast(self, src, filename):
        return __builtin__.compile(src, filename, 'exec', 
                                   flags=ast.PyCF_ONLY_AST)

    def compile_to_code(self, ast_tree, filename):
        # TODO: if root is Module, compile using 'exec'; 
        #       if root is Expression, compile using 'eval'
        return __builtin__.compile(ast_tree, filename, 'exec')

    def script_factory(self, source, code):
        EnvironmentFactory = self.dialect.environment_factory_class()
        return Script(code, source, EnvironmentFactory(self.dialect))


#==============================================================================#
class Compiler(BaseCompiler):

    def __init__(self, dialect):
        super(Compiler, self).__init__(dialect)

    def do_compile(self, src, filename):
        try:
            src = self.processor.process_source(src)
            ast_tree = self.compile_to_ast(src, filename)

            ast_tree = self.processor.process_ast(ast_tree)
            code = self.compile_to_code(ast_tree, filename)
        except:
            # TODO: reraise exception with additional info
            raise

        return code


#==============================================================================#
class SplitSourceCompiler(BaseCompiler):

    def __init__(self, dialect):
        super(SplitSourceCompiler, self).__init__(dialect)

    def do_compile(self, src, filename):
        try:
            src = processor.process_whole_source(src)
            sources = processor.split_source(src)

            trees = [self.do_single_compile(src, filename) for src in sources]

            ast_tree = self.processor.merge_asts(trees)
            ast_tree = self.processor.process_merged_ast(ast_tree)

            code = self.compile_to_code(ast_tree, filename)
        except:
            # TODO: reraise exception with additional info
            raise

        return code

    def do_single_compile(self, src, filename):
        src = self.processor.process_source(src)
        tree = self.compile_to_ast(src, filename)
        return self.processor.process_ast(tree)

#==============================================================================#


