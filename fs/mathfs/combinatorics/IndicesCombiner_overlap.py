#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/IndicesCombinerForCombinations.py
  Contains the class IndicesCombiner that models a combinadic object
  (@see ref @wikipedia below)

Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
import sys
"""


def vai_um_in_place_overlap_case(self, pos):
  """
  Case of "goes one" when overlap=True
  """
  if pos == 0 and self._combset[pos] == self.greatest_int_in_comb:
    self.move_curr_comb_to_last_or_fim()  # iArrayToDiscard = self.move_to_last_one()
    return None
  if self._combset[pos] == self.greatest_int_in_comb:
    return self.vai_um_in_place_overlap_case(pos - 1)
  self._combset[pos] += 1
  self.correct_remaining_to_the_right_overlap_case(pos)
  return self._combset


def vai_um_in_place_non_overlap_case(self, pos):
  """
  Case of vaiUm when overlap=False
  """
  back_pos = self.n_slots - pos - 1
  if pos == 0 and self._combset[pos] == self.greatest_int_in_comb - back_pos:
    self.move_curr_comb_to_last_or_fim()  # iArrayToDiscard = self.move_to_last_one()
    return None
  if self._combset[pos] == self.greatest_int_in_comb - back_pos:
    return self.vai_um_in_place_non_overlap_case(pos - 1)
  self._combset[pos] += 1
  self.correct_remaining_to_the_right_non_overlap_case(pos)
  return self._combset


def vai_um_in_place(self, pos):
  """
  Adds one in the i-th (pos) element
  Example:
    overlap=True,  size=3, upLimit=15
    [1,1,1].foward_n_positions(1) ==>> [1,2,2]
    overlap=False, size=4, upLimit=33
    [1,2,3,4].foward_n_positions(2) ==>> [1,2,4,5]
  """
  if self.overlap:
    return self.vai_um_in_place_overlap_case(pos)
  else:
    return self.vai_um_in_place_non_overlap_case(pos)


def minus_one_overlap(self, pos):
  """
  Inner implementation of previous() for the overlap=True case
  see @previous()
  """
  if pos == 0:
    if self._combset[0] > 0:
      self._combset[0] -= 1
      return self._combset
    else: # if self.iArray[pos] == 0:
      self.move_curr_comb_to_first_or_ini()
      return None
  if self._combset[pos - 1] == self._combset[pos]:
    self._combset[pos] = self.greatest_int_in_comb
    return self.minus_one_overlap(pos - 1)
  else:
    self._combset[pos] -= 1
    return self._combset


def next_under_overlap(self, pos):
  # check before first element
  if self._combset is not None and self._combset == [-1] * self.n_slots:
    # switch it off independently of next if's result
    return self.move_curr_comb_to_first_or_ini()
  if pos == -1:
    pos = self.n_slots - 1
    # if self.iArray[pos]+1 > self.greatest_int_in_comb:
  if self.overlap:
    up_limit = self.greatest_int_in_comb
  else:
    up_limit = self.greatest_int_in_comb - (self.n_slots - pos - 1)
  if self._combset and self._combset[pos]+1 > up_limit:
    if self.overlap:
      value = self.recurse_indices_with_overlap(pos)
    else:
      value = self.recurse_indices_without_overlap(pos)
    if value is None:
      return None
  else:
    self._combset[pos] = value
    self._combset[pos] += 1
  return copy.copy(self._combset)


def next_under_nonoverlap(self):
  self._combset = ICf.add_one(self._combset, up_limit=self.greatest_int_in_comb)
  return self._combset


def next_zeroless(self):
  """
  Example:
    if i_array (the current one) is [0, 3]
      the next_zeroless is [1, 2]  # remember that combinations should be always a growing sequence
    if i_array (the current one) is [0, 3, 5]
      the next_zeroless is also [1, 2, 3]
    if i_array (the current one) is [1, 2, 3]
      the next_zeroless is itself (also [1, 2, 3]) because there's no zero in it
    Now suppose the whole combination set is [[0,1]],
      then its next_zeroless is None, ie it's treated the same as next() or add_one()
  """
  # look up zeroes
  if self.greatest_int_in_comb == 1 and self.n_slots == 2:
    # the case in which whole combination set is [[0,1]]
    return None
  bool_array = list(map(lambda e: e == 0, self._combset))
  if True in bool_array:
    zeroless = list(range(self.n_slots))
    # position i_array to it
    self._combset = copy.copy(zeroless)
    return zeroless
  return self._combset


def get_first_elements(self, upto=10):
  if upto > self.total_cmbs:
    upto = self.total_cmbs
  other = copy.copy(self)
  i_array = other.first_comb
  for i in range(upto):
    if i_array is None:
      return
    yield i_array
    i_array = other.next()


def __str__(self):
  """
  The object's string representation contains n_elements, n_slots, overlap &
    the first 10 (or less) combination elements.
  """
  n = self.n_elements
  first_elems = list(self.get_first_elements(10))
  out_str = f'IndicesCombiner n_elements={n} overlap={self.overlap} array={first_elems}'
  return out_str

def all_sets(self):
  """
  This method, though it's still here, should be used with caution in the sense
    that it's memory-hungry, so to say.
  It while-loops all self.next()'s into an output array.
  Because output may become very big, according to the size involved the process,
    a better approach is to "yield" each "work_set" (a generator approach)
    one at a time, without buffering them into the "output array"
    This better approach is done by the following next method gen_all_sets()
  """
  array = []
  s = self.first
  work_set = list(s) # hard-copy
  while s:
    array.append(work_set)
    s = self.next()
    if s:
      work_set = list(s)
  return array

  def recurse_indices_with_overlap(self, p_pos):
    """
    This is an inner recursive help method
    For the case when overlap=True
    """
    if p_pos == 0 and self._combset[p_pos] + 1 > self.greatest_int_in_comb:
      return None
    if self._combset[p_pos] + 1 > self.greatest_int_in_comb:
      if self._combset[p_pos - 1] + 1 > self.greatest_int_in_comb:
        # self.iArray[pos]=self.iArray[pos-1]
        return self.recurse_indices_with_overlap(p_pos - 1)
      self._combset[p_pos - 1] += 1
      self._combset[p_pos] = self._combset[p_pos - 1]
      return self._combset[p_pos - 1]
    return self._combset[p_pos] + 1

  def recurse_indices_without_overlap(self, p_pos):
    """
    This is an inner recursive help method
    For the case when overlap=False
    """
    if p_pos is None:
      return None
    if p_pos == 0 and self._combset[p_pos] + 1 > self.greatest_int_in_comb - (self.n_slots - p_pos - 1):
      return None
    if self._combset[p_pos] + 1 > self.greatest_int_in_comb - (self.n_slots - p_pos - 1):
      tmp = self.recurse_indices_without_overlap(p_pos - 1)
      if tmp is None:
        return None
      self._combset[p_pos] = tmp + 1
      return self._combset[p_pos]
    self._combset[p_pos] += 1
    return self._combset[p_pos]


def adhoc_test():
  pass


if __name__ == '__main__':
  """
  """
  adhoc_test()
