import sys
import os
import traceback
import gc

CHECK_REFERENCES = False

def main():
    ##gc.set_debug(gc.DEBUG_STATS)
    ##gc.set_debug(gc.DEBUG_LEAK)
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
        
    if CHECK_REFERENCES:
        print ''
        print 'gc count: {0}'.format(gc.get_count())
        print 'gc collect: {0}'.format(gc.collect())
        print 'gc count: {0}'.format(gc.get_count())
    
    ##print 'gc garbage: {0}'.format(len(gc.garbage))
    ##gc.set_debug(0)
    sys.exit(0)
        

main()
