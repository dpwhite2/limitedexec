
class Processor(object):
    def __init__(self, dialect):
        self.SourceValidator = dialect.source_validator_class()
        self.SourceTransform = dialect.source_transform_class()
        self.AstValidator = dialect.ast_validator_class()
        self.AstTransform = dialect.ast_transform_class()

    def process_source(self, source):
        validator = self.SourceValidator()
        transform = self.SourceTransform()
        return transform(source, validator)

    def process_ast(self, ast_tree):
        validator = self.AstValidator()
        transform = self.AstTransform()
        return transform(ast_tree, validator)


class MultiProcessor(Processor):
    def __init__(self, dialect):
        super(MultiProcessor, self).__init__(dialect)
        self.WholeSourceValidator = dialect.whole_source_validator_class()
        self.WholeSourceTransform = dialect.whole_source_transform_class()
        self.SourceSplitter = dialect.source_splitter_class()
        self.AstMerger = dialect.ast_merger_class()
        self.MergedAstValidator = dialect.merged_ast_validator_class()
        self.MergedAstTransform = dialect.merged_ast_transform_class()

    def process_whole_source(self, source):
        validator = self.WholeSourceValidator()
        transform = self.WholeSourceTransform()
        return transform(source, validator)

    def split_source(self, source):
        splitter = self.SourceSplitter()
        return splitter(source)

    def merge_asts(self, trees):
        merger = self.AstMerger()
        return merger(trees)

    def process_merged_ast(self, ast_tree):
        validator = self.MergedAstValidator()
        transform = self.MergedAstTransform()
        return transform(ast_tree, validator)






