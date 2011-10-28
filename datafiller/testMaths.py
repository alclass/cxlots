#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

class testMaths(unittest.TestCase):
  '''
  A test class for the maths module
  '''
  def setUp(self):
    '''
    set up data
    setUp is called before each test function execution
    '''
    pass
  
  def testSquare(self):
    self.assertEqual(first, second, msg)

  def testCube(self):
    self.assertEqual(first, second, msg)


if __name__ == '__name__':
  # unittest.main(module, defaultTest, argv, testRunner, testLoader)
  unittest.main()    