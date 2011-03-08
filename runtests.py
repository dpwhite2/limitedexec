import sys
import unittest

loader = unittest.defaultTestLoader

start_dir = 'ltdexec.tests'
top_level_dir = '.'

suite = loader.discover(start_dir, top_level_dir=top_level_dir)

runner = unittest.TextTestRunner()
runner.run(suite)
