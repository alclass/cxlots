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
import fs.mathfs.combinatorics.hanoi_like_tower_piecemover as pm  # .HanoiTowerPieceMover

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
    # self.countdict = {}
    # self.grafted_combs = []
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

    self.soma_diminished is adjusted before getting here
    """
    self.ongo_gapset = [0] * self.gapsize
    self.ongo_gapset[0] = self.soma_diminished
    self.idx += 1
    self.partition_combs = [copy.copy(self.ongo_gapset)]

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

  def move_one_from_one_pin_to_the_next(self, pos):
    """
    This function is not itself recursive, but it's called by
      move_pieces_within_hanoitower() which is itself recursive.
    This function, at each call, moves one quantity from a left position
      to a rightone.
    Examples:
        [4, 0], [3, 1], [2, 2], [1, 3], [0, 4]
        Each move will happen by one singular call here.
        The sequence above represents 4 pieces being moved from the leftmost
          pin to the rightmost one in the manner of a Hanoi Tower.
        Its set is like a Hanoi Tower itself. 4 pieces moves one by one to its target.
    """
    # source index cannot be outside array
    if pos > len(self.ongo_gapset) - 1:
      # stop recursion
      return False
    # if its value is 0, there is nothing to move rightward
    if self.ongo_gapset[pos] == 0:
      # move position rightward and recheck if there's still something to move
      return False
    # if pintrg is not given, it's the subsequent of pinscr
    nextpos = pos + 1
    # target index cannot be outside array
    if nextpos > len(self.ongo_gapset) - 1:
      # stop recursion
      return False
    # if target slot has already received something before, move on rightward
    if self.ongo_gapset[nextpos] > 0 and nextpos < len(self.ongo_gapset) - 1:
      if self.ongo_gapset[pos] == 0:
        return False
      return True
    # target slot cannot be greater than the limiting value (soma_diminished)
    nextslot = self.ongo_gapset[nextpos]
    if nextslot > self.soma_diminished:
      # stop recursion
      return False
    # it seems alright for moving one quantity left to right
    self.ongo_gapset[pos] -= 1
    self.ongo_gapset[nextpos] += 1
    # quantities motion happened, return True from here
    # move_pieces_within_hanoitower() will get back to it as returns falls to it
    self.pos = pos
    return True

  def add_gapset(self):
    self.idx += 1
    self.partition_combs.append(copy.copy(self.ongo_gapset))

  def move_pieces_within_hanoitower(self, pos=None):
    """
    if self.pos > len(self.ongo_gapset) - 1:
      return
    """
    pos = 0 if pos is None else pos
    if pos > len(self.ongo_gapset) -1:
      return
    if self.ongo_gapset[pos] == 0:
      if pos < len(self.ongo_gapset) - 1:
        return self.move_pieces_within_hanoitower(pos+1)
      else:
        bootres = self.dimish_one_n_restart_hanoi()
        if bootres:
          # recurse have sum diminished by one
          return self.move_pieces_within_hanoitower()
        else:
          return
    boolres = self.move_one_from_one_pin_to_the_next(pos)
    if boolres:
      self.add_gapset()
    return self.move_pieces_within_hanoitower(pos+1)
    # value at pos is == 0, ie nothing to move rightward
    # sum has been diminished to 0, traversal process has ended

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
      npieces = self.partition_digits_sum
      mover = pm.HanoiLikeTowerPieceMover(npieces=npieces, nslots=self.gapsize)
      mover.process()
      # self.move_pieces_within_hanoitower()
      self.allcombs += copy.copy(mover.traversal_combinations)


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


def adhoc_test():
  """
  comb = [4, 2]
  print(f'calling Grafter(comb={comb}))
  grafter = Grafter(comb=comb, upto=6)
  grafter.get_graft_combs_w_nzeroes()
  """
  max_digits_sum, gapsize = 3, 2
  distror = PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
  distror.process()
  print(max_digits_sum, gapsize, 'res =>:', distror.allcombs)
  max_digits_sum, gapsize = 2, 1
  distror = PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
  distror.process()
  print(max_digits_sum, gapsize, 'res =>:', distror.allcombs)
  max_digits_sum, gapsize = 4, 1
  distror = PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
  distror.process()
  print(max_digits_sum, gapsize, 'res =>:', distror.allcombs)
  max_digits_sum, gapsize = 4, 2
  distror = PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
  distror.process()
  print(max_digits_sum, gapsize, 'res =>:', distror.allcombs)
  max_digits_sum, gapsize = 1, 2
  distror = PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
  distror.process()
  print(max_digits_sum, gapsize, 'res =>:', distror.allcombs)
  max_digits_sum, gapsize = 4, 3
  distror = PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
  distror.process()
  print(max_digits_sum, gapsize, 'res =>:', distror.allcombs)


def adhoc_test2():
  """
  max_digits_sum, gapsize = 1, 3
  distror = PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
  distror.process()
  print(max_digits_sum, gapsize, 'res =>:', distror.allcombs)
  """
  max_digits_sum, gapsize = 3, 4
  distror = PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
  distror.process()
  print(max_digits_sum, gapsize, 'res =>:', distror.allcombs)


if __name__ == '__main__':
  """
  list_dist_xysum_metric_thru_ms_history()
  """
  adhoc_test2()
