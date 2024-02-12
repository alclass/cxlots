#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_NumberSystemIndicesCombiner2.py
  Unit-tests for fs/mathfs/combinatorics/NumberSystemIndicesCombiner2.py

Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
import sys
"""
import unittest
import fs.mathfs.combinatorics.NumberSystemIndicesCombiner2 as nsic  # nsic.NumberSystemIndicesCombiner


class TestCase1(unittest.TestCase):

  def test_1(self):
    # the first expected combination list is in descending order,
    # on ahead, this list is reversed for testing it in the ascending order
    expect_nscomb_arr = [
       [3, 3], [3, 2], [3, 1], [3, 0],
       [2, 3], [2, 2], [2, 1], [2, 0],
       [1, 3], [1, 2], [1, 1], [1, 0],
       [0, 3], [0, 2], [0, 1], [0, 0],
    ]
    n_elements, n_slots = 4, 2
    ic = nsic.NumberSystemIndicesCombiner(n_elements=n_elements, n_slots=n_slots)
    resulted_nscomb_arr = []
    for _ in ic.gen_desc_combs_w_intrange_from_downto():
      resulted_nscomb_arr.append(list(ic.curr_comb))
    # t1 equality of desc expect_nscomb_arr with resulted_nscomb_arr
    self.assertEqual(expect_nscomb_arr, resulted_nscomb_arr)
    # t2 equality of sizes
    self.assertEqual(len(expect_nscomb_arr), ic.size)
    expect_nscomb_arr = list(reversed(expect_nscomb_arr))
    resulted_nscomb_arr = []
    for _ in ic.gen_asc_combs_w_intrange_from_to():
      resulted_nscomb_arr.append(list(ic.curr_comb))
    # t3 equality of asc expect_nscomb_arr with resulted_nscomb_arr
    self.assertEqual(expect_nscomb_arr, resulted_nscomb_arr)
