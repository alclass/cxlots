#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/IndicesCombinerForCombinations.py
  Contains the class IndicesCombiner that models a combinadic object
  (@see ref @wikipedia below)

Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
import sys
"""


def correct_remaining_to_the_right_overlap_case(self, pos):
  """
  Recursive method
    When vaiUm() happens, the logical consistency of iArray should be kept.
    In a way, it's similar to the adding algorithm we learn at school.
  Example:
    vaiUm(pos=1) for [0,3,3] will result [0,4,3]
  This needs the "goes one" to [0,4,4]
  """
  if pos+1 >= self.n_slots:
    return
  if self.curr_comb[pos] > self.greatest_int_in_comb:
    errmsg = 'Index in Combiner exceeds upLimit(=%d). There is probably a bug. self.iArray[%d]=%d :: ' %(self.greatest_int_in_comb, pos, self.curr_comb[pos])
    errmsg += str(self)
    raise ValueError(errmsg)
  self.curr_comb[pos + 1] = self.curr_comb[pos]
  return self.correct_remaining_to_the_right_overlap_case(pos + 1)


def correct_remaining_to_the_right_non_overlap_case(self, pos):
  """
  Recursive method
    When vaiUm() happens, the logical consistency of iArray should be kept.
    In a way, it's similar to the adding algorithm we learn at school.
  Example:
    vaiUm(pos=1) for [0,3,4] will result [0,4,4]
    This needs the "goes one" to [0,4,5]
  """
  if pos+1 >= self.n_slots:
    return
  # notice back_pos here is POSITIVE ie eg. [0,1,3,...,10] back_pos's are [10,9,...,0]
  back_pos = self.n_slots - pos - 1
  if self.curr_comb[pos] > self.greatest_int_in_comb - back_pos:
    errmsg = 'Index in Combiner exceeds upLimit(=%d). There is probably a bug. self.iArray[%d]=%d :: ' %(self.greatest_int_in_comb, pos, self.curr_comb[pos])
    errmsg += str(self)
    raise ValueError(errmsg)
  self.curr_comb[pos + 1] = self.curr_comb[pos] + 1
  return self.correct_remaining_to_the_right_non_overlap_case(pos + 1)


def foward_n_positions(self, pos=-1):  # , nOfPos=-1
  """
  Left-shifts curr_comb (formerly iArray)
  Eg
    overlap=True, size=3, upLimit=15
      [1,1,1].foward_n_positions(1) ==>> [2,2,2]
    overlap=False, size=4, upLimit=33
      [1,2,3,4].foward_n_positions(2) ==>> [1,3,4,5]
  """
  if pos == -1:
    pos = self.n_slots - 1
  if pos == 0:
    # well, it's the last one, a left-shift can't happen,
    # so it goes to the last one
    return self.move_curr_comb_to_last_or_fim()  # iArrayToDiscard = self.move_to_last_one()
  if self.overlap:
    if self.curr_comb[pos - 1] == self.greatest_int_in_comb:
      return self.foward_n_positions(pos - 1)
    self.curr_comb[pos - 1] += 1
    self.correct_remaining_to_the_right_overlap_case(pos - 1)
    return self.curr_comb
  else:
    pos_ant = pos - 1
    back_pos_ant = self.n_slots - pos_ant - 1
    if self.curr_comb[pos_ant] == self.greatest_int_in_comb - back_pos_ant:
      return self.foward_n_positions(pos - 1)
    self.curr_comb[pos - 1] += 1
    self.correct_remaining_to_the_right_non_overlap_case(pos - 1)
    return self.curr_comb


def vai_um_in_place_overlap_case(self, pos):
  """
  Case of "goes one" when overlap=True
  """
  if pos == 0 and self.curr_comb[pos] == self.greatest_int_in_comb:
    self.move_curr_comb_to_last_or_fim()  # iArrayToDiscard = self.move_to_last_one()
    return None
  if self.curr_comb[pos] == self.greatest_int_in_comb:
    return self.vai_um_in_place_overlap_case(pos - 1)
  self.curr_comb[pos] += 1
  self.correct_remaining_to_the_right_overlap_case(pos)
  return self.curr_comb


def vai_um_in_place_non_overlap_case(self, pos):
  """
  Case of vaiUm when overlap=False
  """
  back_pos = self.n_slots - pos - 1
  if pos == 0 and self.curr_comb[pos] == self.greatest_int_in_comb - back_pos:
    self.move_curr_comb_to_last_or_fim()  # iArrayToDiscard = self.move_to_last_one()
    return None
  if self.curr_comb[pos] == self.greatest_int_in_comb - back_pos:
    return self.vai_um_in_place_non_overlap_case(pos - 1)
  self.curr_comb[pos] += 1
  self.correct_remaining_to_the_right_non_overlap_case(pos)
  return self.curr_comb


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
    if self.curr_comb[0] > 0:
      self.curr_comb[0] -= 1
      return self.curr_comb
    else: # if self.iArray[pos] == 0:
      self.move_curr_comb_to_first_or_ini()
      return None
  if self.curr_comb[pos - 1] == self.curr_comb[pos]:
    self.curr_comb[pos] = self.greatest_int_in_comb
    return self.minus_one_overlap(pos - 1)
  else:
    self.curr_comb[pos] -= 1
    return self.curr_comb


def minus_one_non_overlap(self, pos):
  """
  Inner implementation of previous() for the overlap=False case
  see @previous()
  """
  if pos == 0:
    if self.curr_comb[pos] > 0:
      self.curr_comb[pos] -= 1
      return self.curr_comb
  if self.curr_comb[pos] == pos:
    self.move_curr_comb_to_first_or_ini()
    return None
  if self.curr_comb[pos - 1]+1 == self.curr_comb[pos]:
    debit_to_up_limit = self.n_slots - pos - 1
    self.curr_comb[pos] = self.greatest_int_in_comb - debit_to_up_limit
    return self.minus_one_non_overlap(pos - 1)
  else:
    self.curr_comb[pos] -= 1
  return self.curr_comb


def next_under_overlap(self):
  # check before first element
  if self.curr_comb is not None and self.curr_comb == [-1] * self.n_slots:
    # switch it off independently of next if's result
    return self.move_curr_comb_to_first_or_ini()
  if pos == -1:
    pos = self.n_slots - 1
    # if self.iArray[pos]+1 > self.greatest_int_in_comb:
  if self.overlap:
    up_limit = self.greatest_int_in_comb
  else:
    up_limit = self.greatest_int_in_comb - (self.n_slots - pos - 1)
  if self.curr_comb and self.curr_comb[pos]+1 > up_limit:
    if self.overlap:
      value = self.recurse_indices_with_overlap(pos)
    else:
      value = self.recurse_indices_without_overlap(pos)
    if value is None:
      return None
  else:
    self.curr_comb[pos] = value
    self.curr_comb[pos] += 1
  return copy.copy(self.curr_comb)


def next_under_nonoverlap(self):
  self.curr_comb = ICf.add_one(self.curr_comb, up_limit=self.greatest_int_in_comb)
  return self.curr_comb

def next(self, pos=-1):
  """
  Moves curr_comb position to the next consistent one and returns it
  When the last one is current, a None will be returned
  (thus, None becomes here a kind of convention of "after the last" or "parked after the last")
  """
  if not self.overlap:
    return self.next_under_nonoverlap()
  return self.next_under_nonoverlap()

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
  bool_array = list(map(lambda e: e == 0, self.curr_comb))
  if True in bool_array:
    zeroless = list(range(self.n_slots))
    # position i_array to it
    self.curr_comb = copy.copy(zeroless)
    return zeroless
  return self.curr_comb

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

def gen_all_sets(self):
  """
  This method, though it's still here, should be used with caution in the sense the it's memory-hungry, so to say.
  It while-loops all self.next()'s into an output array.
  Because output may become very big, according to the size involved the process,
    a better approach is to "yield" each "work_set", one at a time, without buffering them into the "output array"
    This better approach is done by the following next method gen_all_sets()
  """
  work_set = self.first
  while work_set:
    yield list(work_set)  # hard-copy
    work_set = self.next()

def recurse_indices_with_overlap(self, p_pos):
  """
  This is an inner recursive help method
  For the case when overlap=True
  """
  if p_pos == 0 and self.curr_comb[p_pos] + 1 > self.greatest_int_in_comb:
    return None
  if self.curr_comb[p_pos] + 1 > self.greatest_int_in_comb:
    if self.curr_comb[p_pos - 1] + 1 > self.greatest_int_in_comb:
      # self.iArray[pos]=self.iArray[pos-1]
      return self.recurse_indices_with_overlap(p_pos - 1)
    self.curr_comb[p_pos - 1] += 1
    self.curr_comb[p_pos] = self.curr_comb[p_pos - 1]
    return self.curr_comb[p_pos - 1]
  return self.curr_comb[p_pos] + 1

def recurse_indices_without_overlap(self, p_pos):
  """
  This is an inner recursive help method
  For the case when overlap=False
  """
  if p_pos is None:
    return None
  if p_pos == 0 and self.curr_comb[p_pos] + 1 > self.greatest_int_in_comb - (self.n_slots - p_pos - 1):
    return None
  if self.curr_comb[p_pos] + 1 > self.greatest_int_in_comb - (self.n_slots - p_pos - 1):
    tmp = self.recurse_indices_without_overlap(p_pos - 1)
    if tmp is None:
      return None
    self.curr_comb[p_pos] = tmp + 1
    return self.curr_comb[p_pos]
  self.curr_comb[p_pos] += 1
  return self.curr_comb[p_pos]


def adhoc_test():
  pass


if __name__ == '__main__':
  """
  """
  adhoc_test()
