#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/hanoi_like_tower_piecemover.py
  Contains class HanoiLikeTowerPieceMover

This HanoiLike moving is not the one of the classic Hannoi-Tower.
This HanoiLike moving may be explained by an example:
  @see also docstrings below

 => Suppose an array with 3 columns (or rods or posts or towers).
 => Suppose the first column (the leftmost one) has 4 pegs;
    the other two have none.

The objective is to find all "transitions" to take all 4 pegs,
  one at a time, left to right tower by tower, to the last tower.

Thus, the transitions are:

    0 [4, 0, 0]  # all pieces begin at slot 1
    1 [3, 1, 0]  # first step, one piece is moved from slot 1 to slot 2
    2 [2, 2, 0]  # second step, another piece is moved from slot 1 to slot 2
    3 [1, 3, 0]
    4 [0, 4, 0]
    5 [0, 3, 1]  # one piece is moved from slot 2 to slot 3
    6 [0, 2, 2]  # another piece is moved from slot 2 to slot 3
    7 [0, 1, 3]
    8 [0, 0, 4]  # all pieces end up at slot 3

"""
import copy


class HanoiLikeTowerPieceMover:
  """
  First off, this class does not implement the classic "Hanoi Tower",
    it just implements a simpler rod/disk scheme that contains "equal" disks.

  This implementation does not work with more than
    one single slot (or stakepost, or rod, or slot etc.) filled in with pieces (or disks).

  The scenario here is like the following example:
  Suppose 4 pieces and 3 slots, the array [4, 0, 0] represents this.
  Now the objective is to move, piece by piece, everything
    so that at the end, the array is [0, 0, 4]

  The transitions under the algorithm in-here is:
    0 [4, 0, 0]  # all pieces begin at slot 1
    1 [3, 1, 0]  # first step, one piece is moved from slot 1 to slot 2
    2 [2, 2, 0]  # second step, another piece is moved from slot 1 to slot 2
    3 [1, 3, 0]
    4 [0, 4, 0]
    5 [0, 3, 1]  # one piece is moved from slot 2 to slot 3
    6 [0, 2, 2]  # another piece is moved from slot 2 to slot 3
    7 [0, 1, 3]
    8 [0, 0, 4]  # all pieces end up at slot 3

  @see property 'size' below for the analytical formula that counts all traversal_combinations.
  If demand grows above some expected size, a 'generation' function, with yield, may be thought about.

  Applicaton:
    the main application of this class is to help form the zero-grafted combinations
    (@see its module for further info).
  """

  def __init__(self, npieces=4, nslots=3):
    self.npieces = npieces
    self.nslots = nslots
    self.qtd_slot_array = [0]*nslots
    self.qtd_slot_array[0] = npieces
    self.from_slot = 0
    self.idx = 0
    self.traversal_combinations = [copy.copy(self.qtd_slot_array)]
    self.has_been_processed = False

  @property
  def size(self):
    """
    This is the "analytical formula" for the total number of traversal_combinations
    Notice that 'size' here does not grow exponentially. However, as commented above:
      if demand grows above some expected size,
      a 'generation' function, with yield, may be thought about.
    """
    return self.npieces * (self.nslots - 1) + 1

  @property
  def nsteps(self):
    return self.size - 1

  @property
  def all_combinations(self):
    """
    Returns self.traversal_combinations ie the list result of the HanoiLike traversal
      Obs: property allcombs below is an alias for this property
    Returns: list - the appended self.traversal_combinations

    """
    if not self.has_been_processed:
      self.process()
    return self.traversal_combinations

  @property
  def allcombs(self):
    """
    Same as property all_combinations
    Returns: list - the appended self.traversal_combinations
    """
    return self.all_combinations

  @property
  def whileloop_size_limit(self):
    """
    This is an infinite loop protection for the while-loop in method process()
    """
    return self.size * 2

  def move_piece_left_to_right_if_possible(self):
    if self.qtd_slot_array[self.from_slot] == 0:  # ie there's nothing to move rightward
      if self.from_slot < self.nslots - 2:  # slots can still go rightward
        self.from_slot += 1  # reposition one slot to the right and try again (recurse)
        return self.move_piece_left_to_right_if_possible()
      else:  # slot cannot go rightward anymore, traversal has finished
        return
    # at this point, self.qtd_slot_array[self.from_slot] > 0,
    # ie there may be something to move rightward if indices are good
    if self.from_slot + 1 < self.nslots:
      # move piece left to right
      self.qtd_slot_array[self.from_slot] -= 1
      self.qtd_slot_array[self.from_slot+1] += 1
      self.idx += 1
      self.traversal_combinations.append(copy.copy(self.qtd_slot_array))
    return  # indices got beyond size, traversal has finished

  def mount_patterns_w_hanoilike_piece_moving(self):
    """
    The upstream function has an 'yield'
      that outputs one element that is a 'gapset'
    """
    loop_iter_n = -1
    while self.qtd_slot_array[-1] < self.npieces:
      loop_iter_n += 1
      if loop_iter_n > self.whileloop_size_limit:
        errmsg = f'Exceeded whileloop_in_process_limit={self.whileloop_size_limit}'
        raise ValueError(errmsg)
        # break  # the while-loop
      for i in range(self.nslots):
        if self.qtd_slot_array[i] > 0:
          self.from_slot = i
          break  # the for-loop
      self.move_piece_left_to_right_if_possible()

  def process(self):
    """
    for idx, patt in enumerate(self.patterns):
      print(idx, patt)
    """
    self.mount_patterns_w_hanoilike_piece_moving()
    self.has_been_processed = True

  def __str__(self):
    outstr = f"""HanoiLikeTowerMover
    npieces = {self.npieces}
    nslots = {self.nslots}
    size = {self.size}
    combinations = {self.traversal_combinations}
    count = {len(self.traversal_combinations)}
    """
    return outstr


def adhoc_test():
  """
  max_digits_sum, gapsize = 1, 3
  distror = PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
  distror.process()
  print(max_digits_sum, gapsize, 'res =>:', distror.allcombs)
  """
  npieces, nslots = 4, 3
  m = HanoiLikeTowerPieceMover(npieces, nslots)
  m.process()
  print(m)
  npieces, nslots = 4, 2
  m = HanoiLikeTowerPieceMover(npieces, nslots)
  m.process()
  print(m)
  npieces, nslots = 1, 2
  m = HanoiLikeTowerPieceMover(npieces, nslots)
  m.process()
  print(m)
  npieces, nslots = 3, 2
  m = HanoiLikeTowerPieceMover(npieces, nslots)
  m.process()
  print(m)
  npieces, nslots = 3, 5
  m = HanoiLikeTowerPieceMover(npieces, nslots)
  m.process()
  print(m)
  npieces, nslots = 4, 3
  m = HanoiLikeTowerPieceMover(npieces, nslots)
  m.process()
  print(m)


if __name__ == '__main__':
  """
  list_dist_xysum_metric_thru_ms_history()
  """
  adhoc_test()
