

#==============================================================================#
class Source(object):
    def __init__(self, source, filename):
        self.lines = source.splitlines() or ['']
        self.filename = filename

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, lineno):
        """ One-based index into the lines of the source file.

            It is one-based because Python usually reports line numbers
            starting from one, and converting here keeps the conversion in one
            location.  Zero is not a valid index.

            Negative indexes are interpreted in the normal Python manner.
        """
        if isinstance(lineno, slice):
            start, stop = None, None
            if lineno.start > 0:
                start = lineno.start - 1
            elif lineno.start == 0:
                raise IndexError('Zero is not a valid index.  Line numbers are counted from 1.')
            if lineno.stop > 0:
                stop = lineno.stop - 1
            elif lineno.stop == 0:
                raise IndexError('Zero is not a valid index.  Line numbers are counted from 1.')
            lineno = slice(start, stop, lineno.step)
        else:
            if lineno > 0:
                lineno -= 1
            elif lineno == 0:
                raise IndexError('Zero is not a valid index.  Line numbers are counted from 1.')
        return self.lines[lineno]

    def __iter__(self):
        return self.lines.__iter__()

    def __str__(self):
        return '\n'.join(self.lines)

    def __repr__(self):
        return '<Source: filename={0}, lines={1}>'.format(self.filename, len(self.lines))

#==============================================================================#

