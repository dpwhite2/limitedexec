import sys
import os
import traceback

def main():
    if len(sys.argv) <= 1:
        print 'usage: python _runtest.py TESTSCRIPT'
        sys.exit(1)
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            src = f.read()
        co = compile(src, filename, mode='exec')
        globals = locals = {}
        eval(co, globals, locals)
    except SystemExit:
        raise
    except:
        print ''
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
        

main()
