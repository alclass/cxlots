#!/usr/bin/env python3
"""
algorithmsForPermutationEtAl.py


Main functions here:

-- permute(arrayN)
-- geraSumComponents(soma, parcel=-1, acc=[])
   Generates Integer Partitions
   (look for further explanation on the comments at the beginning of the function below)
-- getTilPatternsFor(patternSize=10, patternSoma=6)
   Uses geraSumComponents(patternSoma) then it stuffs zeroes
   and filters out larger strings than patternSize

"""
# import numpy, time, sys
import unittest
import fs.mathfs.combinatorics.combinatoric_algorithms as ca  # .permute2_d


class TestComb(unittest.TestCase):

  def test_permute(self):
    # t1
    alist = [1, 2]
    expected_permutation = [[1, 2], [2, 1]]
    returned_permutation = ca.permute(alist)
    self.assertEqual(expected_permutation, returned_permutation)
    expected_size = 2  # ie 2! is 2
    returned_size = ca.permute_n(len(alist))
    self.assertEqual(expected_size, returned_size)
    # t2
    alist = list(range(3))
    expected_permutation = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
    returned_permutation = ca.permute(alist)
    self.assertEqual(expected_permutation, returned_permutation)
    expected_size = 6   # ie 3! is 3*2 = 6
    returned_size = ca.permute_n(len(alist))
    self.assertEqual(expected_size, returned_size)

  def test_permute_via_indices(self):
    # t1
    alist = ['a', 'b', 'c']
    expected_permutation = [
      ['a', 'b', 'c'], ['a', 'c', 'b'], ['b', 'a', 'c'], ['b', 'c', 'a'], ['c', 'a', 'b'], ['c', 'b', 'a']
    ]
    returned_permutation = ca.get_genpermute_via_indices(alist)
    self.assertEqual(expected_permutation, returned_permutation)
    expected_size = 6   # ie 3! is 3*2 = 6
    returned_size = ca.permute_n(len(alist))
    self.assertEqual(expected_size, returned_size)
    # t2
    alist = 'abc'
    expected_permutation = [
      'abc', 'acb', 'bac', 'bca', 'cab', 'cba'
    ]
    returned_permutation = ca.get_genpermutations_o_str(alist)
    self.assertEqual(expected_permutation, returned_permutation)

  def test_generate_integer_partitions(self):
    """
    geraSumComponents(soma, parcel=-1, acc=[]) is an [[[ Integer Partitions generator ]]]
    The name geraSumComponents() was given here
      before I came across the established term Integer Partitions
      from the technical literature;

    Eg geraSumComponents(soma=4) results in:
      [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]]
    """
    soma = 4
    returned_partitions = ca.mount_all_integer_partitions_for(soma=soma)
    expected_partitions = [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]]
    self.assertEqual(expected_partitions, expected_partitions)
    soma = 5
    returned_partitions = ca.mount_all_integer_partitions_for(soma=soma)
    expected_partitions = [[5], [4, 1], [3, 2], [3, 1, 1],  [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]]
    self.assertEqual(expected_partitions, expected_partitions)
