#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_IndicesCombiner.py
  Contains unit-tests to the class IndicesCombiner
    that models a combinadic object (@see also its docstring)
"""
import unittest
import fs.mathfs.combinatorics.IndicesCombinerForCombinations as iCmb  # ic.IndicesCombiner


class TestIndicesCombiner(unittest.TestCase):

  def test_instantiate_indicescombiner(self):
    """
    Default parameters to IndicesCombiner
    ic = IndicesCombiner(greatest_int_in_comb=0, size=1, overlap=True, i_array_in=None)
    Example:
      ic = iCmb.IndicesCombiner(2, 2)
          combinations = [[0, 1], [0, 2], [1, 2]]
    """
    # t1
    expected_set = [[0, 1], [0, 2], [1, 2]]
    n_elements, n_slots = 3, 2
    ic = iCmb.IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots)
    expected_first = expected_set[0]
    self.assertEqual(expected_first, ic.first_comb)
    expected_last = expected_set[-1]
    self.assertEqual(expected_last, ic.last_comb)
    returned_set = list(ic.get_all_cmbs_or_those_bw_ini_fim_if_given())
    self.assertEqual(expected_set, returned_set)
    # t2
    expected_set = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    n_elements, n_slots = 4, 3
    ic = iCmb.IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots)
    expected_first = expected_set[0]
    self.assertEqual(expected_first, ic.first_comb)
    expected_last = expected_set[-1]
    self.assertEqual(expected_last, ic.last_comb)
    returned_set = list(ic.get_all_cmbs_or_those_bw_ini_fim_if_given())
    self.assertEqual(expected_set, returned_set)
    # t3
    expected_set = [[0, 1, 2, 3]]
    n_elements, n_slots = 4, 4
    ic = iCmb.IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots)
    expected_first = expected_set[0]
    self.assertEqual(expected_first, ic.first_comb)
    expected_last = expected_set[-1]
    self.assertEqual(expected_last, ic.last_comb)
    returned_set = list(ic.get_all_cmbs_or_those_bw_ini_fim_if_given())
    self.assertEqual(expected_set, returned_set)
    # t4
    expected_set = [
      [0, 1, 2, 3], [0, 1, 2, 4], [0, 1, 3, 4], [0, 2, 3, 4], [1, 2, 3, 4],
    ]
    n_elements, n_slots = 5, 4
    ic = iCmb.IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots)
    expected_first = expected_set[0]
    self.assertEqual(expected_first, ic.first_comb)
    expected_last = expected_set[-1]
    self.assertEqual(expected_last, ic.last_comb)
    returned_set = list(ic.get_all_cmbs_or_those_bw_ini_fim_if_given())
    self.assertEqual(expected_set, returned_set)

  def test_indicescombiner_w_ini_n_fim_combs(self):
    # t1
    expected_set = [
      [0, 1, 2, 4], [0, 1, 3, 4], [0, 2, 3, 4],
    ]
    n_elements, n_slots = 5, 4
    ini_comb, fim_comb = [0, 1, 2, 4], [0, 2, 3, 4]  # observing the set above (test1), extremes were pruned
    ic = iCmb.IndicesCombinerForCombinations(
      n_elements=n_elements, n_slots=n_slots, ini_comb=ini_comb, fim_comb=fim_comb
    )
    expected_first = expected_set[0]
    self.assertEqual(expected_first, ic.ini_comb)
    expected_last = expected_set[-1]
    self.assertEqual(expected_last, ic.fim_comb)
    returned_set = list(ic.get_all_cmbs_or_those_bw_ini_fim_if_given())
    self.assertEqual(expected_set, returned_set)
    # t2
    expected_set = [[0, 1, 2, 3]]
    n_elements, n_slots = 4, 4
    ic = iCmb.IndicesCombinerForCombinations(
      n_elements=n_elements, n_slots=n_slots, ini_comb=expected_set[0], fim_comb=expected_set[0]
    )
    expected_first = expected_set[0]
    self.assertEqual(expected_first, ic.ini_comb)
    expected_last = expected_set[-1]
    self.assertEqual(expected_last, ic.fim_comb)
    returned_set = list(ic.get_all_cmbs_or_those_bw_ini_fim_if_given())
    self.assertEqual(expected_set, returned_set)
