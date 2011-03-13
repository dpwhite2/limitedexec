from ltdexec.dialect import Dialect
from ltdexec.compiler import compile

src = """\
"""

def main():
    filename = 'my_script'
    dialect = Dialect()
    script = compile(src, filename, dialect)
    result = script.run()
    assert result.exception is False


main()
