

class TransformBase(object):
    def __call__(self, data, validator):
        data = self.precheck_transform(data)
        validator(data)
        return self.postcheck_transform(data)

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
