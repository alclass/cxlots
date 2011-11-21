#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import os # datetime, sys

def sumDigits(pattern):
  '''
  This function sums a sequence of numbers in a string or an iterator from which int(element) is possible
  From the context of cxlots, its function is to sum up the digits in a pattern string
  Eg
  '10221' will sum as follows: 1+0+2+2+1=6
  '''
  if pattern == None:
    return None
  # in the future, refactor this part to test for an iterator, instead of str, list or tuple
  if type(pattern) not in [str, list, tuple]:
    return None
  soma = 0
  for c in pattern:
    try:
      soma += int(c)
    except ValueError:
      return None
  return soma

import unittest
class Test(unittest.TestCase):
  def test_sumDigits(self):
    expected = 6 # eg 1+0+2+2+1=6
    for pattern in ['10221', '11112', '600000000', '111111','0000000000000051']:
      self.assertEqual(sumDigits(pattern), expected)
    for pattern in ['310221', '911112', '1600000000', '9111111','30000000000000051', '0']:
      # expected is still the same above, ie 6
      self.assertNotEqual(sumDigits(pattern), expected)
    for pattern in ['a10221', 'string', 1.23, ['blah','blah'],'-1','+0']:
      self.assertIsNone(sumDigits(pattern))

if __name__ == '__main__':
  unittest.main()
