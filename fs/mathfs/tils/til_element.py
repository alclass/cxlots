#!/usr/bin/env python3
"""
fs/mathfs/tils/til_pattern_vector.py
  Contains class TilPatternVector
"""
import os, sys
folder_relpath = os.path.dirname(__file__)
folder_abspath = os.path.abspath(folder_relpath)
app_root_abspath = folder_abspath [ : -len('maths2/frequencies') ]
sys.path.insert(0, app_root_abspath)


def spread2_d_list_to1_d_list(list2_d):
  """
  what does this do?
  """
  new_set = []
  for list1D in list2_d:
    for element in list1D:
      new_set.append(element)
  return new_set


def sum_up_til_pattern(pattern):
  try:
    return sum(map(int, pattern))
  except (TypeError, ValueError):
    pass
  return None


class TilElement:
  """
  This class covers a Til Element.

  The 'til' in the name comes from the idea (or paradigm or entity or...) of quartil, percentil etc.
  The til then is a sort of instanced n-til, when n is an integer ranging from 2 to 100 (or even more than 100).
    It will be quartil (4-til) if the frequencies are in four groups,
    a sixtil (6-til) if frequencies are in six groupings,
    a tentil (10-til), if frequencies are in ten groups, a percentil (100-til) if in one hundred groupings.
  So, a 'til' is a frequency placement of a datum among others in a sample (or a population).
  For instance, in quartils:
    q1 the first quartil takes all elements (items) that belong to the first 25% most frequent;
    q2 the second quartil encompasses all elements (items) that belong to the second 25%
      (or within 25% to 50%) most frequent;
    q3 the third quartil considers all elements (items) that belong to the third 25% (or within 50% to 75%);
    q4 the fourth and last quartil engulfs the elements (items) that belong to the fourth 25% (or within 75% to 100%);

  So, the til-metric ends up being more than a metric, in fact, it's a statistic,
    ie a measure that depends on sample or population.

  A Til Element is instantiated with a pattern (eg '03021'): the numbers represent quantities or frequencies.
  From any pattern (these numbers), the two attributes n_slots (formerly length) and elemsum can be derived.
    n_slots is the pattern's string size (in the example above len('03021')=5
    and sum is the summing up of its digits (in the example above 0+3+0+2+1=6)
  
  It implements a method called get_worksets_w_quantities() which does the following:
    it gets the frequency-til-positioned dezenas and joins this set with the quantity
    expressed in the digit.
    
    Let's see this in the example above '03021':
    -- 0, the first digit, means 0 dezenas in the first quintil
    -- 3 means 3 dezenas in the second quintil which may have x dezenas altogether
    -- the pair (tuple) to form is this set of x dezenas, together with the quantity 3
    -- this tuple will be used elsewhere for combinations of this til(size=5, index=1) 3 by 3

    index 1 is because pattern[1]=3
    
    So this method is applied in a calling routine that produces these combinations
  """

  def __init__(self, pattern):
    """
    init() set the attributes pattern and its two derivatives length and sum
    """
    self.pattern = pattern
    self._elemsum = None

  @property
  def n_slots(self):
    return len(self.pattern)

  @property
  def elemsum(self):
    """
    self.sum = sum_up_til_pattern(self.pattern)
    """
    if self._elemsum is None:
      self._elemsum = sum(map(int, self.pattern))
    return self._elemsum

  def get_worksets_w_quantities(self):
    """
    This method returns a list of tuples
    -- the 2D-tuple has 1) a list of dezenas & 2) quantity
    -- -- the dezenas are picked up via method tilObj.getTilSets()
          given the til index (eg 0123 are indices for the four quartils)
    -- -- the quantity is the digit in the pattern itself
         eg 03021 says
            3 dezenas in quintil 2, 2 dezenas in quintil 4 & 1 dezena in quintil 5
    """
    work_sets_with_quantities = []
    tilObj = TilMaker(self.length)
    for i in range(len(self.pattern)):
      quantity = int(self.pattern[i])
      if quantity > 0:
        dezenas = tilObj.getTilSets()[i]
        work_set_with_quantity = (dezenas, quantity)
        work_sets_with_quantities.append(work_set_with_quantity)
    return work_sets_with_quantities

def test_til_element():
  til_element = TilElement('03021')
  work_sets_with_quantities = til_element.get_worksets_w_quantities()
  for ws in work_sets_with_quantities:
    print(ws[0], 'size', len(ws[0]), 'ncomb', ws[1])  # work_sets_with_quantities
  #test_til_element()
  

def adhoctest():
  test_til_element()


if __name__ == '__main__':
  adhoctest()
