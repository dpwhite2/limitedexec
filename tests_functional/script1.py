from ltdexec.dialect import Dialect
from ltdexec.compiler import compile

class MyDialect(Dialect):
    allow_statement_import = True

src = """\
import math

nums = [1.,4.,9.,16.,25.]
roots = [0 for i in xrange(len(nums))]

def calc_root(i):
    roots[i] = math.sqrt(nums[i])

def calc_roots():
    for i in xrange(len(nums)):
        calc_root(i)

calc_roots()

"""

def main():
    filename = 'my_script'
    dialect = MyDialect()
    script = compile(src, filename, dialect)
    result = script.run()
    assert result.exception is False
    roots = result.globals['roots']
    assert roots == [1., 2., 3., 4., 5.,],  roots


main()
