#!/usr/bin/env python3
"""
libfunctions/jogos/test_til_functions.py
  Contains unit-tests for libfunctions/jogos/til_functions.py
"""
import unittest
import libfunctions.jogos.til_functions as tf  # .sum_digits


class Test(unittest.TestCase):

  def test_sum_digits(self):
    expected = 6  # eg 1+0+2+2+1=6
    for pattern in ['10221', '11112', '600000000', '111111', '0000000000000051']:
      self.assertEqual(tf.sum_digits(pattern), expected)
    for pattern in ['310221', '911112', '1600000000', '9111111', '30000000000000051', '0']:
      # expected is still the same above, ie 6
      self.assertNotEqual(tf.sum_digits(pattern), expected)
    for pattern in ['a10221', 'string', 1.23, ['blah', 'blah'], '-1', '+0']:
      self.assertIsNone(tf.sum_digits(pattern))
