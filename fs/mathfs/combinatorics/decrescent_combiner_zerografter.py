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
import fs.mathfs.combinatorics.decrescent_combiner as dc  # dc.DecrescentCombiner


class Grafter:

  def __init__(self, comb, upto=6):
    self.comb = comb
    self.combs = []
    self.upto = upto
    self.graftedcombs = []
    self.cmber = None
    self.prepare_cmber()

  def prepare_cmber(self):
    """
    nslots = startint - 1
    """
    startint = self.nzeroes
    self.cmber = dc.DecrescentCombiner(startint=startint, nslots=startint-1, upto=startint)
    self.cmber.process()
    self.combs = copy.copy(self.cmber.combs)
    # "simmetrize" it (ie, 3|0 produces 0|3, 2|1 produces 1|2 etc
    print('combs', self.combs)

  @property
  def nzeroes(self):
    return self.upto - len(self.comb)

  def get_graft_combs_w_nzeroes(self):
    combs = self.cmber.partition_combs
    for comb in combs:
      print(comb)


class PartitionsHanoiTowerCombiner:
  """
  The algorithmic solution is a Hanoi Tower with each 'sum' state.

  """

  def __init__(self, max_digits_sum=3, gapsize=2):
    """
    # initial condition, initialization

    """
    self.gapsize = gapsize
    self.pos = self.gapsize - 1
    self.idx = -1
    self.gap_ranges_tuplelist = []
    self.countdict = {}
    self.grafted_combs = []
    self.allcombs = []
    self.partition_combs = []
    self.ongo_gapset = []
    self.max_digits_sum = max_digits_sum
    self.partition_digits_sum = max_digits_sum
    # self.max_digits_sum = max_digits_sum
    self.soma_diminished = self.partition_digits_sum
    self.add_first_gapset_to_partition()

  def add_first_gapset_to_partition(self):
    """
    This implementation has max_sum limited to 9
    Returns:

    """
    self.ongo_gapset = [0] * self.gapsize
    self.pos = 0
    self.soma_diminished = self.partition_digits_sum
    self.ongo_gapset[self.pos] = self.soma_diminished
    self.idx += 1
    self.partition_combs = [copy.copy(self.ongo_gapset)]
    self.soma_diminished = self.soma

  @property
  def soma(self):
    return sum(self.ongo_gapset)

  def dimish_one_n_restart_hanoi(self):
    if self.soma_diminished > 0:
      self.soma_diminished -= 1
      self.pos = 0
      self.add_first_gapset_to_partition()
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
    self.partition_combs.append(copy.copy(self.ongo_gapset))

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
    previous_digit = self.ongo_gapset[self.pos]
    self.ongo_gapset[self.pos] += 1
    if self.soma <= self.partition_digits_sum:
      return True
    if self.pos == 0:
      return False
    self.ongo_gapset[self.pos] = previous_digit
    return self.move_pieces_within_hanoitower()


  def process(self):
    for self.partition_digits_sum in range(self.max_digits_sum, 0, -1):
      self.partition_combs = []
      self.add_first_gapset_to_partition()
      self.move_pieces_within_hanoitower()
      self.allcombs += copy.copy(self.partition_combs)


class ZeroesGraftAndCountsMixer:

  def __init__(self, max_digits_sum=3, gapsize=2):
    self.zeroes_graft_combs = PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)

  def mix(self):
    pass

  def determine_graft_ranges(self, countdict):
    self.countdict = countdict
    indices = self.countdict.keys()
    sorted(indices)
    prev_idx = -1
    self.gap_ranges_tuplelist = []
    while len(indices) > 0:
      idx = indices.pop()
      if prev_idx < 0:
        prev_idx = idx
        continue
      if idx - prev_idx > 1:
        trange = (prev_idx+1, idx-1)
        self.gap_ranges_tuplelist.append(trange)

  def graft_zeroes(self, countdict):
    self.grafted_combs = []
    indices = self.countdict.keys()
    sorted(indices)
    countlist = [self.countdict[i] for i in indices]
    for comb in self.allcombs:
      patt = ''.join(comb)
      zeroes_str = '0' * nzeroes
      trange = self.gap_ranges_tuplelist[i]


def adhoc_test():
  """
  comb = [4, 2]
  print(f'calling Grafter(comb={comb}))
  grafter = Grafter(comb=comb, upto=6)
  grafter.get_graft_combs_w_nzeroes()
  """
  distror = PartitionsHanoiTowerCombiner(max_digits_sum=4, gapsize=3)
  distror.process()
  print(distror.allcombs)


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
