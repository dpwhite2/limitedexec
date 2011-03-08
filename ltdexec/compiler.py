import ast

class BaseCompiler(object):

    def __init__(self, dialect):
        self.dialect = dialect
        self.processor = dialect.Processor()

    def __call__(self, source, filename):
        assert isinstance(source, basestring)
        code = self.do_compile(source, filename)
        script = self.script_factory(source, code, filename)
        return script

    def compile_to_ast(self, source, filename):
        return compile(source, filename, 'exec', flags=ast.PyCF_ONLY_AST)

    def compile_to_code(self, ast_tree, filename):
        return compile(ast_tree, filename, 'exec')

    def script_factory(self, source, code, filename):
        # use self.dialect
        # TODO...
        pass


class Compiler(BaseCompiler):

    def __init__(self, dialect):
        super(Compiler, self).__init__(dialect)

    def do_compile(self, source, filename):
        try:
            source = self.processor.process_source(source)
            ast_tree = self.compile_to_ast(source, filename)

            ast_tree = self.processor.process_ast(ast_tree)
            code = self.compile_to_code(ast_tree, filename)
        except:
            # TODO: reraise exception with additional info
            raise

        return code


class MultiCompiler(BaseCompiler):

    def __init__(self, dialect):
        super(MultiCompiler, self).__init__(dialect)

    def do_compile(self, source, filename):
        try:
            source = processor.process_whole_source(source)
            sources = processor.split_source(source)

            trees = [self.do_single_compile(src, filename) for src in sources]

            ast_tree = self.processor.merge_asts(trees)
            ast_tree = self.processor.process_merged_ast(ast_tree)

            code = self.compile_to_code(ast_tree, filename)
        except:
            # TODO: reraise exception with additional info
            raise

        return code

    def do_single_compile(self, source, filename):
        source = self.processor.process_source(source)
        tree = self.compile_to_ast(source, filename)
        return self.processor.process_ast(tree)


