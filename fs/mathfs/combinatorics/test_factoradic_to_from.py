#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_factoradic_to_from.py
  Unit-tests for fs/mathfs/combinatorics/factoradic_to_from.py

"""
import unittest
import math


class TestForFactoradicsEtAl(unittest.TestCase):

  def test_1(self):
    """
    979,999(decimal) = 2623031010(factoradic)
    """
    quoc = 979999 // math.factorial(9)
    expected_quoc = 2
    self.assertEqual(expected_quoc, quoc)
    remainder = 979999 % math.factorial(9)
    expected_remainder = 254239
    self.assertEqual(expected_remainder, remainder)

  def test_2(self):
    pass
