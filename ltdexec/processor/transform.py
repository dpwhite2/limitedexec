"""
ltdexec.processor.transform
===========================

Transform classes modify the raw source code or the abstract syntax tree before
it has been compiled.

"""

class TransformBase(object):
    def __init__(self, dialect):
        self.dialect = dialect

    def precheck_transform(self, data):
        return data

    def postcheck_transform(self, data):
        return data


class SourceTransform(TransformBase):
    pass

class AstTransform(TransformBase):
    # TODO: replace imports with custom import function
    pass

class MergedAstTransform(TransformBase):
    pass