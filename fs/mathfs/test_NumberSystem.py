#!/usr/bin/env python3
"""
fs/mathfs/test_NumberSystem.py
  Contains unit-tests for fs/mathfs/NumberSystem.py
"""
import unittest
import fs.mathfs.NumberSystem as nS  #


class Test1(unittest.TestCase):

  def test_convert_positive_dec_int_to_base(self):
    """
    assert returned == expected
    returned = f(210, 5)  # returns '1320' (which 210 written on base 5)
    expected = '1320'
    assert returned == expected
    returned = f(210, 6)  # returns '550'
    expected = '550'
    assert returned == expected
    returned = f(0, 6)  # returns '0'
    expected = '0'
    assert returned == expected
    returned = f(1, 6)  # returns '1'
    expected = '1'
    assert returned == expected
    returned = f(6, 6)  # returns '10'
    expected = '10'
    assert returned == expected
    returned = f(7, 6)  # returns '11'
    expected = '11'
    assert returned == expected
    """
    n, base, strdigits = 10, 10, ''
    f = nS.convert_positive_dec_int_to_base
    returned = f(1024, 2)  # returns '10000000000' (which is 1024 written on base 2)
    expected = '10000000000'
    self.assertEqual(expected, returned)
