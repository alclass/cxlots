#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

this_is_just_to_avoid_recursive_local_imports=1
from HTMLGrabber import *
del this_is_just_to_avoid_recursive_local_imports

htmlFragAsTestForComparison = '''
'''

class TestHtmlGrabber(unittest.TestCase):
  '''
  A test class for the maths2 module
  '''
  def setUp(self):
    '''
    set up data
    setUp is called before each test function execution
    '''
    self.grabber = HtmlGrabberClass()
    pass
  
  def testSquare(self):
    self.assertEqual(first, second, msg)

  def testCube(self):
    self.assertEqual(first, second, msg)


if __name__ == '__name__':
  # unittest.main(module, defaultTest, argv, testRunner, testLoader)
  unittest.main()    