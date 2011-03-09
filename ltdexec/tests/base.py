import unittest

from ltdexec.dialect.registry import dialects


class LtdExec_TestCaseBase(unittest.TestCase):
    def setUp(self):
        self._dialectlist = set(dialects.names())
        
    def tearDown(self):
        newlist = set(dialects.names())
        for name in (newlist-self._dialectlist):
            dialects.unregister(name)
