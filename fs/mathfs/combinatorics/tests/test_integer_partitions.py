#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_integer_partitions.py
  Unit-tests for fs/mathfs/combinatorics/integer_partitions_n_binsearch.py

Updated on 10/02/2024
Created on 22/11/2011
@author: luizlewis
"""
import math
import unittest
import random
import fs.mathfs.combinatorics.integer_partitions_n_binsearch as ipbs


class Test(unittest.TestCase):

  def test_integer_partitions(self):
    # calculating expectedMaxNOfIterationsPlus1 in THREE STEPS
    exp_parts = [[1]]
    ret_parts = ipbs.get_integer_partitions_of(1)
    self.assertEqual(exp_parts, ret_parts)
    exp_parts = [[1, 1], [2]]
    ret_parts = ipbs.get_integer_partitions_of(2)
    self.assertEqual(exp_parts, ret_parts)
    exp_parts = [[1, 1, 1], [1, 2], [3]]
    ret_parts = ipbs.get_integer_partitions_of(3)
    self.assertEqual(exp_parts, ret_parts)
    exp_parts = [[1, 1, 1, 1], [1, 1, 2], [1, 3], [2, 2], [4]]
    ret_parts = ipbs.get_integer_partitions_of(4)
    self.assertEqual(exp_parts, ret_parts)
    exp_parts = [
      [1, 1, 1, 1, 1], [1, 1, 1, 2], [1, 1, 3], [1, 2, 2], [1, 4], [2, 3], [5]
    ]
    ret_parts = ipbs.get_integer_partitions_of(5)
    self.assertEqual(exp_parts, ret_parts)

  def test_binary_search(self):
    elem_for_binsearch, n_elements = 11, 30
    exp_idx_pos = elem_for_binsearch
    array = list(range(n_elements))
    exp_n_iter = math.floor(math.log(n_elements, 2))
    ret_idx_pos, ret_n_iter = ipbs.binarysearch_idxpos_n_niterations_f_array_n_value(array, elem_for_binsearch)
    self.assertEqual(exp_idx_pos, ret_idx_pos)
    self.assertEqual(exp_n_iter, ret_n_iter)
