#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/decrescent_combiner.py
  Contains class DecrescentCombiner

This class may be explained by an example:
  DecrescentCombiner object
      upto=6 nslots=6 startint=3
    [[3, 3], [3, 2, 1], [3, 1, 1, 1], [2, 2, 2], [2, 2, 1, 1], [2, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]

The purpose is to form integer sets whose members added up to 'upto'. In the example, upto=6,
  ie, each the elements of each set sums up to 6.
The second detail is that the elements into sets are organized decrescently.


"""
# import numpy, time, sys
import copy
import random
import sys


class DecrescentCombiner:
  def __init__(self, startint=3, nslots=5, upto=6):
    self.startint, self.nslots, self.upto = startint, nslots, upto
    self.combs = []
    self.ongoingcomb = [self.startint]

  @property
  def soma(self):
    return sum(self.ongoingcomb)

  def move_to_leftplace_n_diminish_1(self):
    if len(self.ongoingcomb) < 1:
      return False
    self.ongoingcomb.pop()  # last digit was stripped out
    if len(self.ongoingcomb) < 1:
      return False
    leftdigit = self.ongoingcomb[-1]
    if leftdigit < 2:
      return self.move_to_leftplace_n_diminish_1()
    leftdigit -= 1
    self.ongoingcomb[-1] = leftdigit
    return True

  def diminish_1_on_last_pos_n_leftpropagate_if_needed(self):
    ondigit = self.ongoingcomb[-1]
    if ondigit < 2:
      return self.move_to_leftplace_n_diminish_1()
    ondigit -= 1
    self.ongoingcomb[-1] = ondigit
    return True

  def recurs_combine_n_make_sumsets(self):
    if self.soma >= self.upto:
      if self.soma == self.upto:
        self.combs.append(copy.copy(self.ongoingcomb))
      boolret = self.diminish_1_on_last_pos_n_leftpropagate_if_needed()
      if not boolret:
        return
      return self.recurs_combine_n_make_sumsets()
    # self.soma < self.upto:
    # duplicate digit and recurse if not at limit size
    if len(self.ongoingcomb) < self.nslots:
      ondigit = self.ongoingcomb[-1]
      self.ongoingcomb.append(ondigit)
      return self.recurs_combine_n_make_sumsets()
    boolret = self.diminish_1_on_last_pos_n_leftpropagate_if_needed()
    if not boolret:
      return
    return self.recurs_combine_n_make_sumsets()

  def process(self):
    return self.recurs_combine_n_make_sumsets()

  def __str__(self):
    outstr = f"""DecrescentCombiner object
    upto={self.upto} nslots={self.nslots} startint={self.startint}
    {self.combs}
    """
    return outstr


class ZeroGrafterCombiner():

  def __init__(self, pos_count_dict, expand_to=6):
    self.pos_count_dict, self.expand_to = pos_count_dict, expand_to
    self.combs = []
    self.ongoingcomb = [self.startint]




def adhoc_test():
  """
  n_combs = combine_n_c_by_c(20, 5)
  print('ca.combine_n_c_by_c(70, 7)', n_combs)
  Returns:
  guide = 3
  results = get_combine_sumsets(guide, upto=6)
  print('guideint', guide, 'results', results)
  results = get_combine_sumsets2(leftmost=guide, upto=6, slots=3)
  print('guide', guide, 'results', results)
  """
  cmber = DecrescentCombiner(startint=3, nslots=6, upto=6)
  cmber.recurs_combine_n_make_sumsets()
  print(cmber)
  cmber = DecrescentCombiner(startint=7, nslots=4, upto=6)
  cmber.recurs_combine_n_make_sumsets()
  print(cmber)
  cmber = DecrescentCombiner(startint=12, nslots=3, upto=4)
  cmber.recurs_combine_n_make_sumsets()
  print(cmber)


if __name__ == '__main__':
  """
  """
  adhoc_test()
