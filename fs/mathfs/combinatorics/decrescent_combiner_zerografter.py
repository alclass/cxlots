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
import fs.mathfs.combinatorics.decrescent_combiner as dc # dc.DecrescentCombiner
import random
import sys

class Grafter:

  def __init__(self, comb, upto=6):
    self.comb = comb
    self.upto = upto
    self.graftedcombs = []
    self.cmber = None
    self.prepare_cmber()

  def prepare_cmber(self):
    startint = self.nzeroes
    nslots = startint - 1
    self.cmber = dc.DecrescentCombiner(startint=startint, nslots=startint-1, upto=startint)
    self.cmber.process()
    self.combs = copy.copy(self.cmber.combs)
    # "simmetrize" it (ie, 3|0 produces 0|3, 2|1 produces 1|2 etc
    print('combs', self.combs)



  @property
  def nzeroes(self):
    return self.upto - len(self.comb)

  def get_graft_combs_w_nzeroes(self):
    combs = self.cmber.combs
    for comb in combs:
      print(comb)


class CombGapDistributor:
  """
  The algorithmic solution is a Hanoi Tower with each 'sum' state.

  """

  def __init__(self, max_digits_sum=3, gapsize=2):
    """
    # initial condition, initialization
    Args:
      digits_sum:
      gapsize:
    """
    self.gapsize = gapsize
    self.pos = self.gapsize - 1
    self.idx = -1
    self.combs = []
    self.ongo_gapset = []
    self.max_digits_sum = max_digits_sum
    self.soma_diminished = self.max_digits_sum
    self.add_full_gapset()

  def add_full_gapset(self):
    """
    This implementation has max_sum limited to 9
    Returns:

    """
    self.ongo_gapset = [0] * self.gapsize
    self.pos = 0
    self.ongo_gapset[self.pos] = self.soma_diminished
    self.idx += 1
    self.combs = [copy.copy(self.ongo_gapset)]
    self.soma_diminished = self.soma

  @property
  def soma(self):
    return sum(self.ongo_gapset)

  def dimish_one_n_restart_hanoi(self):
    if self.soma_diminished > 0:
      self.soma_diminished -= 1
      self.pos = 0
      self.add_full_gapset()
      return True
    return False

  def move_one_from_one_pin_to_the_next(self, pinsrc, pintrg=None):
    if self.ongo_gapset[pinsrc] == 0:
      return False
    pintrg = pinsrc+1 if pintrg is None else pintrg
    if self.ongo_gapset[pintrg] > 0 and pintrg < len(self.ongo_gapset) - 1:
      return self.move_one_from_one_pin_to_the_next(pinsrc, pintrg)
    if self.ongo_gapset[pintrg] > self.soma_diminished:
      return False
    self.ongo_gapset[pinsrc] -= 1
    self.ongo_gapset[pintrg] += 1
    return True

  def add_gapset(self):
    self.idx += 1
    self.combs.append(copy.copy(self.ongo_gapset))

  def move_pieces_within_hanoitower(self, pinpos=0):
    if pinpos < len(self.ongo_gapset) and self.ongo_gapset[pinpos] > 0:
      if pinpos < len(self.ongo_gapset) - 1:
        boolres = self.move_one_from_one_pin_to_the_next(pinpos)
        if boolres:
          self.add_gapset()
          return self.move_pieces_within_hanoitower()
      # else:
      #   return
    if self.soma_diminished > 0:
      self.soma_diminished -= 1
      return self.move_pieces_within_hanoitower(pinpos + 1)
    bootres = self.dimish_one_n_restart_hanoi()
    if bootres:
      self.pos = 0
      return self.move_pieces_within_hanoitower()
    return

  def add_one_n_move_leftward_if_possible(self):
    previous_digit = self.gapsize[self.pos]
    self.ongo_gapset[self.pos] += 1
    if self.soma <= self.max_digits_sum:
      return True
    if self.pos == 0:
      return False
    self.ongo_gapset[self.pos] = previous_digit
    return self.move_pieces_within_hanoitower()

  def process(self):
    self.move_pieces_within_hanoitower()


def adhoc_test():
  """
  comb = [4, 2]
  print(f'calling Grafter(comb={comb})')
  grafter = Grafter(comb=comb, upto=6)
  grafter.get_graft_combs_w_nzeroes()
  """
  distror = CombGapDistributor(max_digits_sum=3, gapsize=2)
  distror.process()
  print(distror.combs)


def show_evol():
  s = """CF
  C0000F
  C000F
  C00F
  C0F"""
  print(s)
  s = """CFG  0, 0
  C000FG 3, 0
  C00FG 2, 0
  C0FG 1, 0
  C00F0G 2, 1
  C00FG 2, 0
  C0F0G 1, 1
  C0F00G 1, 2
  CF000G 0, 3
  """
  print(s)



if __name__ == '__main__':
  """
  """
  adhoc_test()
