import ast

from ltdexec.dialect.base import Dialect
from ltdexec.processor.transform import TransformImportsAst
from ltdexec import exceptions

from .base import LtdExec_TestCaseBase

#==============================================================================#
class TransformImportsAst_TestCase(LtdExec_TestCaseBase):
    def test_import(self):
        src = 'import mymodule'
        expect_src = '_LX_import_module("mymodule")'
        tree = ast.parse(src)
        tree = TransformImportsAst().visit(tree)
        expect_tree = ast.parse(expect_src)
        self.assertEquals(ast.dump(expect_tree), ast.dump(tree))

    def test_import_asname(self):
        src = 'import mymodule as thatmodule'
        expect_src = '_LX_import_module("mymodule", asname="thatmodule")'
        tree = ast.parse(src)
        tree = TransformImportsAst().visit(tree)
        expect_tree = ast.parse(expect_src)
        self.assertEquals(ast.dump(expect_tree), ast.dump(tree))

    def test_import_dotted(self):
        src = 'import package.mymodule'
        expect_src = '_LX_import_module("package.mymodule")'
        tree = ast.parse(src)
        tree = TransformImportsAst().visit(tree)
        expect_tree = ast.parse(expect_src)
        self.assertEquals(ast.dump(expect_tree), ast.dump(tree))

    def test_import_multi(self):
        src = 'import mod1, mod2 as x, mod3'
        expect_src = '_LX_import_module("mod1")\n_LX_import_module("mod2", asname="x")\n_LX_import_module("mod3")'
        tree = ast.parse(src)
        tree = TransformImportsAst().visit(tree)
        expect_tree = ast.parse(expect_src)
        self.assertEquals(ast.dump(expect_tree), ast.dump(tree))

    def test_import_from(self):
        src = 'from mymodule import name'
        expect_src = '_LX_import_module("mymodule", froms=[("name",None)])'
        tree = ast.parse(src)
        tree = TransformImportsAst().visit(tree)
        expect_tree = ast.parse(expect_src)
        self.assertEquals(ast.dump(expect_tree), ast.dump(tree))

    def test_import_from_asname(self):
        src = 'from mymodule import name as alias'
        expect_src = '_LX_import_module("mymodule", froms=[("name","alias")])'
        tree = ast.parse(src)
        tree = TransformImportsAst().visit(tree)
        expect_tree = ast.parse(expect_src)
        self.assertEquals(ast.dump(expect_tree), ast.dump(tree))

    def test_import_from_multi(self):
        src = 'from mymodule import name1, name2 as x, name3'
        expect_src = '_LX_import_module("mymodule", froms=[("name1",None),("name2","x"),("name3",None),])'
        tree = ast.parse(src)
        tree = TransformImportsAst().visit(tree)
        expect_tree = ast.parse(expect_src)
        self.assertEquals(ast.dump(expect_tree), ast.dump(tree))
