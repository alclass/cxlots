#!/usr/bin/env python
"""
fs/maths/combinatorics/IndicesCombiner.py
  Contains the class IndicesCombiner that models a combinadic object (@see ref @wikipedia below)

Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
"""
import unittest
import fs.maths.combinatorics.IndicesCombiner as iCmb  # ic.IndicesCombiner


class TestIndicesCombiner(unittest.TestCase):

  def test_instantiate_indicescombiner(self):
    """
    Default parameters to IndicesCombiner
    ic = IndicesCombiner(up_limit=0, size=1, overlap=True, i_array_in=None)
    Example:
      ic = iCmb.IndicesCombiner(2, 2, False)
    [0, 1]   [0, 2]   [1, 2]
    """
    ic = iCmb.IndicesCombiner(2, 2, False)



