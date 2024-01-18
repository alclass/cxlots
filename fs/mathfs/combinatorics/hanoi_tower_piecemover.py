#!/usr/bin/env python3
"""
"""
import copy

class HanoiTowerPieceMover:
  """
  This implementation does not work with more than
    one slot (or post) with pieces,
  ie, all the others after the first one must be empty.
  ie, it works with the first one charged and then
    moves all pieces, one by one, to the last one.

  Example:
  """

  def __init__(self, npieces=4, nslots=3):
    self.npieces = npieces
    self.nslots = nslots
    self.qtd_slot_array = [0]*nslots
    self.qtd_slot_array[0] = npieces
    self.from_slot = 0
    self.idx = 0
    self.patterns = [copy.copy(self.qtd_slot_array)]

  def move_piece_left_to_right_if_possible(self):
    if self.qtd_slot_array[self.from_slot] == 0:
      if self.from_slot < self.nslots - 2:
        self.from_slot += 1
        return self.move_piece_left_to_right_if_possible()
      else:
        return
    # self.qtd_slot_array[self.from_slot] > 0:
    if self.from_slot + 1 < self.nslots:
      # move piece left to right
      self.qtd_slot_array[self.from_slot] -= 1
      self.qtd_slot_array[self.from_slot+1] += 1
      self.idx += 1
      self.patterns.append(copy.copy(self.qtd_slot_array))
    return

  def mount_patterns_w_hanoi_piece_moving(self):
    """
    The upstream function has an 'yield'
      that outputs one element that is a 'gapset'
    """
    while self.qtd_slot_array[-1] < self.npieces:
      for i in range(self.nslots):
        if self.qtd_slot_array[i] > 0:
          self.from_slot = i
          break
      self.move_piece_left_to_right_if_possible()

  def process(self):
    self.mount_patterns_w_hanoi_piece_moving()
    for idx, patt in enumerate(self.patterns):
      print(idx, patt)





def adhoc_test():
  """
  max_digits_sum, gapsize = 1, 3
  distror = PartitionsHanoiTowerCombiner(max_digits_sum=max_digits_sum, gapsize=gapsize)
  distror.process()
  print(max_digits_sum, gapsize, 'res =>:', distror.allcombs)
  """
  npieces, nslots = 4, 3
  m = HanoiTowerPieceMover(npieces, nslots)
  m.process()
  npieces, nslots = 4, 2
  m = HanoiTowerPieceMover(npieces, nslots)
  m.process()
  npieces, nslots = 1, 2
  m = HanoiTowerPieceMover(npieces, nslots)
  m.process()
  npieces, nslots = 3, 2
  m = HanoiTowerPieceMover(npieces, nslots)
  m.process()
  npieces, nslots = 3, 5
  m = HanoiTowerPieceMover(npieces, nslots)
  m.process()


if __name__ == '__main__':
  """
  adhoc_test()
  """
  adhoc_test()
