import unittest

from ltdexec.source import Source

from .base import LtdExec_TestCaseBase


#==============================================================================#
class Source_TestCase(LtdExec_TestCaseBase):
    def test_empty(self):
        text = ''
        filename = 'FILE'
        source = Source(text, filename)
        self.assertEquals(1, len(source))
        self.assertEquals('<Source: filename=FILE, lines=1>', repr(source))
        self.assertEquals('', source[1])
        self.assertEquals([''], source[1:])
        self.assertEquals([''], source[:])
        with self.assertRaises(IndexError) as cm:
            source[0]
        self.assertEquals('', str(source))
        self.assertEquals('', '$'.join(line for line in source))

    def test_one_line(self):
        text = 'x = 5'
        filename = 'FILE'
        source = Source(text, filename)
        self.assertEquals(1, len(source))
        self.assertEquals('<Source: filename=FILE, lines=1>', repr(source))
        self.assertEquals('x = 5', source[1])
        self.assertEquals(['x = 5'], source[1:])
        self.assertEquals(['x = 5'], source[:])
        with self.assertRaises(IndexError) as cm:
            source[0]
        self.assertEquals('x = 5', str(source))
        self.assertEquals('x = 5', '$'.join(line for line in source))

    def test_two_lines(self):
        text = 'x = 5\ny = 7'
        filename = 'FILE'
        source = Source(text, filename)
        self.assertEquals(2, len(source))
        self.assertEquals('<Source: filename=FILE, lines=2>', repr(source))
        self.assertEquals('x = 5', source[1])
        self.assertEquals('y = 7', source[2])
        self.assertEquals('y = 7', source[-1])
        self.assertEquals(['x = 5','y = 7'], source[1:])
        self.assertEquals(['x = 5'], source[1:2])
        self.assertEquals(['x = 5','y = 7'], source[:])
        with self.assertRaises(IndexError) as cm:
            source[0]
        with self.assertRaises(IndexError) as cm:
            source[0:]
        with self.assertRaises(IndexError) as cm:
            source[:0]
        self.assertEquals('x = 5\ny = 7', str(source))
        self.assertEquals('x = 5$y = 7', '$'.join(line for line in source))
        
