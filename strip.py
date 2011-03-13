import sys
import os
import os.path

fileexts = frozenset(('.py',))

def strip_trailing_ws(ifilename, ofilename=None):
    ofilename = ofilename or ifilename
    f = open(ifilename, 'r')
    origlines = [line for line in f]
    f.close()
    lines = [line.rstrip() for line in origlines]
    if lines == origlines:
        print 'No changes to file: {0}'.format(ifilename)
        return
    
    f = open(ofilename, 'w')
    f.write('\n'.join(lines))
    f.close()
    
def main():
    ifilename = sys.argv[1]
    if os.path.isfile(ifilename):
        strip_trailing_ws(ifilename)
    else:
        for dirpath, dirnames, filenames in os.walk(ifilename):
            for filename in filenames:
                root, ext = os.path.splitext(filename)
                if ext in fileexts:
                    fullname = os.path.join(dirpath, filename)
                    strip_trailing_ws(fullname)
    
main()

