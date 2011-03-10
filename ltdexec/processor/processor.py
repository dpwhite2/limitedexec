"""
ltdexec.processor.processor
===========================

Processors that handle a script before it is compiled.

"""
class Processor(object):
    """ Perform modifications and checks of a script before it is compiled.

        A Processor has the opportunity to modify and validate the raw source
        code and the compiled abstract syntax tree.
    """
    def __init__(self, dialect):
        self.dialect = dialect
        self.SourceValidator = dialect.SourceValidator
        self.SourceTransform = dialect.SourceTransform
        self.AstValidator = dialect.AstValidator
        self.AstTransform = dialect.AstTransform

    def process_source(self, source):
        validator = self.SourceValidator(self.dialect)
        transform = self.SourceTransform(self.dialect)
        source = transform.precheck_transform(source)
        validator(source)
        source = transform.postcheck_transform(source)
        return source

    def process_ast(self, ast_tree):
        validator = self.AstValidator(self.dialect)
        transform = self.AstTransform(self.dialect)
        ast_tree = transform.precheck_transform(ast_tree)
        validator(ast_tree)
        ast_tree = transform.postcheck_transform(ast_tree)
        return ast_tree


class SplitSourceProcessor(Processor):
    def __init__(self, dialect):
        super(SplitSourceProcessor, self).__init__(dialect)
        self.WholeSourceValidator = dialect.WholeSourceValidator
        self.WholeSourceTransform = dialect.WholeSourceTransform
        self.SourceSplitter = dialect.SourceSplitter
        self.AstMerger = dialect.AstMerger
        self.MergedAstValidator = dialect.MergedAstValidator
        self.MergedAstTransform = dialect.MergedAstTransform

    def process_whole_source(self, source):
        validator = self.WholeSourceValidator(self.dialect)
        transform = self.WholeSourceTransform(self.dialect)
        source = transform.precheck_transform(source)
        validator(source)
        source = transform.postcheck_transform(source)
        return source

    def split_source(self, source):
        return self.SourceSplitter()(source)

    def merge_asts(self, trees):
        return self.AstMerger()(trees)

    def process_merged_ast(self, ast_tree):
        validator = self.MergedAstValidator(self.dialect)
        transform = self.MergedAstTransform(self.dialect)
        ast_tree = transform.precheck_transform(ast_tree)
        validator(ast_tree)
        ast_tree = transform.postcheck_transform(ast_tree)
        return ast_tree



