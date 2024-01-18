#!/usr/bin/env python3
"""

"""
import fs.mathfs.combinatorics.decrescent_combiner_zerografter as zg  # zg.PartitionsHanoiTowerCombiner
import unittest


class Test1(unittest.TestCase):

  def test_1(self):
    """
    # tests the zero grafting combinations
    """
    # t1
    max_digits_sum, gapsize = 3, 2
    expected_zeroesgraft_combs = [
      [3, 0], [2, 1], [1, 2], [0, 3],
      [2, 0], [1, 1], [0, 2],
      [1, 0], [0, 1]
    ]
    ptc = zg.PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
    ptc.process()
    returned_zeroesgraft_combs = ptc.allcombs
    self.assertEqual(expected_zeroesgraft_combs, returned_zeroesgraft_combs)
    # t1
    max_digits_sum, gapsize = 4, 3
    expected_zeroesgraft_combs = [
      [4, 0, 0], [3, 1, 0], [2, 1, 1], [1, 1, 2], [0, 1, 3], [0, 0, 4],
      [3, 0, 0], [2, 1, 0], [1, 1, 1], [0, 1, 2], [0, 0, 3],
      [2, 0, 0], [1, 1, 0], [0, 1, 1], [0, 0, 2],
      [1, 0, 0], [0, 1, 0], [0, 0, 1]
    ]
    ptc = zg.PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
    ptc.process()
    returned_zeroesgraft_combs = ptc.allcombs
    self.assertEqual(expected_zeroesgraft_combs, returned_zeroesgraft_combs)


expected_zeroesgraft_combs = [
  [3, 0, 0, 0], [2, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 1], [0, 0, 1, 2], [2, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]
]
