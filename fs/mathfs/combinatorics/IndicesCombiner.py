#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/IndicesCombiner.py
  Contains the class IndicesCombiner that models a combinadic object
  (@see ref @wikipedia below)

Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
"""
import copy
import sys
import fs.mathfs.combinatorics.combinatoric_algorithms as ca  # ca.fact(n)
import fs.mathfs.combinatorics.IndicesCombiner_functions as ICf  # ICf.project_last_combinationlist


def verify_lexicographical_comb_must_be_within_first_n_last_or_raise(inbetween_comb, first_comb, last_comb):
  # notice that first_comb and last_comb are equally sized from their origins
  if len(inbetween_comb) != len(first_comb):
    errmsg = f"len(inbetween_comb)={len(inbetween_comb)} != len(first_comb)={len(first_comb)}"
    raise ValueError(errmsg)
  two_by_2 = zip(first_comb, inbetween_comb)
  bool_list = list(map(lambda tupl: tupl[0] <= tupl[1], two_by_2))
  if False in bool_list:
    error_cause = 'LESS'
    errmsg = (f'parameter comb (combination={inbetween_comb}) is'
              f' lexicographical-{error_cause} than the initial value {first_comb}')
    raise ValueError(errmsg)
  two_by_2 = zip(last_comb, inbetween_comb)
  bool_list = list(map(lambda tupl: tupl[0] >= tupl[1], two_by_2))
  if False in bool_list:
    error_cause = 'MORE'
    errmsg = (f'parameter comb (combination={inbetween_comb}) is'
              f' lexicographical-{error_cause} than the initial value {last_comb}')
    raise ValueError(errmsg)


class IndicesCombiner:
  """
  This class is explained by examples
  ===================================

  Example 1:
    indComb = IndicesCombiner(5, 3, False)
    indComb.first() results [0, 1, 2]
    indComb.get_first_given() in this case also results [0, 1, 2]
  applying indComb.next() each time:
    [0, 1, 2]   [0, 1, 3]   [0, 1, 4]   [0, 1, 5]   [0, 2, 3]
    [0, 2, 4]   [0, 2, 5]   [0, 3, 4]   [0, 3, 5]   [0, 4, 5]
    [1, 2, 3]   [1, 2, 4]  ... the last one is [3, 4, 5]
  if a new indComb.next(), after the last one, is applied, None is returned

  The behavior expected is that of a Combination
  Mathematically, the total of combinations (produced arrays) is:
    Combination(5,3) = 5! / ((5-3)!3!) =

  Example 2:
  Now the same example with overlap=True (in fact, 'True' is default)
    indComb = IndicesCombiner(5, 3, True)
    indComb.first() results [0, 0, 0]
    indComb.get_first_given() in this case also results [0, 0, 0]
  (*) get_first_given() is explained below
  aplying indComb.next() each time:
  [0, 0, 1]   [0, 0, 2]   [0, 0, 3]   [0, 0, 4]   [0, 0, 5]
  [0, 1, 1]   [0, 1, 2]   [0, 1, 3]   [0, 1, 4]   [0, 1, 5]
  [0, 2, 2] ... the last one is [5,5,5] after that, a None will be returned

  (*) get_first_given() explanation
    when iArrayIn is passed with a consistent array
    get_first_given() returns that array

  Example:
    indComb = IndicesCombiner(5, 3, True, [2,2,3])
    indComb.get_first_given() in this case results [2, 2, 3]
  [2, 2, 3] is called the "restartAt" array
  indComb.next() results [2, 2, 4]

  IMPORTANT: if indComb.first() is issued/called, the combiner is zeroed,
    so to speak, ie, it goes top to [0,0,0] or [0,1,2] depending on whether
    overlap is True or False, respectively

  Error Handling
  ==============

  1) if a "bad" restartAt array is given, a ValueError Exception will be raised

  Example 1 (for when overlap=False)
  [0,2,2] ie there is a 2 following a 2 (only possible if overlap=True)

  Example 2 (for when either overlap=True or False)
  [0,10,9] ie there is a 9 following a 10

  2) when overlap=False, if both upLimit and size are positive (*),
     upLimit must be at least size - 1

  (*) if upLimit or size enters negative, they are changed to the default,
      ie, upLimit=0 and size=1

  Eg. upLimit = 2 and size = 3 :: this will result in
      only one combination [0,1,2] (with overlap=False)
  
  If the above fails, a ValueError Exception will be raised
  Notice that this restriction does not exist for overlap=True

  Test example:

  indComb = IndicesCombiner(1, 4, True)
  [0, 0, 0, 0]  [0, 0, 0, 1]  [0, 0, 1, 1]  [0, 1, 1, 1]  [1, 1, 1, 1]

  But
    [[[ indComb = IndicesCombiner(1, 4, False) ]]] will raise a ValueError:

  Traceback (most recent call last):
    File "./combinadics.py", line 237, in <module>
      test_indices_combiner(upLimit, size)
    File "./combinadics.py", line 189, in test_indices_combiner
      indComb = IndicesCombiner(upLimit, size, False); c=0
    File "./combinadics.py", line 80, in __init__
      raise ValueError, msg
  ValueError: Inconsistent IndicesCombiner upLimit(=1) must be at least size(=4) - 1 when overlap=False
  """

  def __init__(self, n_elements=1, n_slots=1, overlap=True, ini_comb=None, fim_comb=None):
    self.n_elements = n_elements
    self.n_slots = n_slots
    self.ini_comb = ini_comb
    self.fim_comb = fim_comb
    self.curr_comb = None
    self._first_comb = None
    self._last_comb = None
    self.comb_before_first = None  # [-1] * self.n_slots
    self.overlap = bool(overlap)
    self.check_consistency_of_nelements_n_nslots()
    self.check_consistency_of_ini_comb_n_fim_comb()

  def check_consistency_of_nelements_n_nslots(self):
    """
    """
    try:
      self.n_slots = int(self.n_slots)
    except (TypeError, ValueError):
      self.n_slots = 1
    try:
      self.n_elements = int(self.n_elements)
    except (TypeError, ValueError):
      self.n_elements = 1
    if not self.overlap:
      if self.n_elements + 2 < self.n_slots:
        errmsg = ('Inconsistent IndicesCombiner upLimit(=%d) must be at least size(=%d) - 1 when overlap=False '
                  % (self.n_elements, self.n_slots))
        raise ValueError(errmsg)
    else:
      if self.n_elements < self.n_slots:
        errmsg = ('Inconsistent IndicesCombiner upLimit(=%d) must be at least size(=%d) when overlap=False '
                  % (self.n_elements, self.n_slots))
        raise ValueError(errmsg)

  def check_consistency_of_ini_comb_n_fim_comb(self):
    # init self.curr_comb based on whether it's pos after zero or the zero pos
    self.comb_before_first = [-1] * self.n_slots
    if self.ini_comb is None:
      self.ini_comb = list(self.first_comb)
      self.curr_comb = list(self.first_comb)
    else:
      verify_lexicographical_comb_must_be_within_first_n_last_or_raise(self.ini_comb, self.first_comb, self.last_comb)
      self.curr_comb = list(self.ini_comb)
    if self.fim_comb is None:
      self.fim_comb = list(self.last_comb)
    else:
      # the verification below also checks that len(self.curr_comb) is equal to self.n_slots
      verify_lexicographical_comb_must_be_within_first_n_last_or_raise(self.fim_comb, self.first_comb, self.last_comb)

  @property
  def greatest_index(self):
    """
    greatest_index was formerly called "up_limit"
    least_index is "commonly" 0, so there's not a @property for it
    """
    return self.n_elements - 1

  def check_array_consistency(self):
    """
    Checks the consistency of iArray
    Examples of inconsistent arrays:
      1) for overlap=True
        valid ==>> [0,0,0], [0,1,1], [2,2,3]
        invalid ==>> [0,1,0], [10,0,0]
      2) for overlap=False
        valid ==>> [0,1,2], [0,1,100]
        invalid ==>> [0,0,0], [2,2,3] (these two valid when overlap=True)
    """
    for i in range(self.n_slots - 1):
      raise_exception = False
      if self.overlap:
        if self.curr_comb[i] > self.curr_comb[i+1]:
          raise_exception = True
      else:
        if self.curr_comb[i] >= self.curr_comb[i]+1:
          raise_exception = True
      if raise_exception:
        if self.overlap:
          context = 'lesser'
        else:
          context = 'lesser or equal'
        errmsg = 'Inconsistent array: next elem can be %s than a previous one %s' % (context, str(self.curr_comb))
        raise ValueError(errmsg)

  def position_curr_comb_before_first(self):
    self.curr_comb = list(self.comb_before_first)

  @property
  def first_comb(self):
    if self._first_comb is None:
      if self.overlap:
        self._first_comb = [0] * self.n_slots
      else:
        self._first_comb = list(range(self.n_slots))
    return self._first_comb

  @property
  def ini_comb_given(self):
    if self.ini_comb:
      return self.ini_comb
    return self.first_comb

  @property
  def last_comb(self):
    if self._last_comb is None:
      if self.overlap:
        self._last_comb = [self.greatest_index] * self.n_slots
      else:
        cut_pos = self.greatest_index - self.n_slots + 1
        self._last_comb = list(range(cut_pos, self.greatest_index + 1))
    return self._last_comb

  @property
  def total_comb(self):
    """
    Uses the formula:
    comb_of_n_m_by_m = n! / ((n - m)! * m!)
    For example: the MS has 50063860 combinations, ie C = 60! / (54! * 6!)
    """
    if not self.overlap:
      if self.n_elements == self.n_slots:
        return 1
      n = self.n_elements
      m = self.n_slots
      num = ca.fact(n)
      den = ca.fact(n - m) * ca.fact(m)
      total_combinations = num / den
      # total_combinations should be a countable integer
      return int(total_combinations)
    else:
      # TO-DO
      return -1

  @property
  def size(self):
    return self.total_comb

  def reposition_to_first_given(self):
    """
    Returns the get_first_given/restartAt array changing current position to it
    @see also get_first_given()
    """
    if self.ini_comb:
      self.curr_comb = list(self.ini_comb)
    else:
      self.curr_comb = list(self.first_comb)
    return self.curr_comb

  def move_curr_comb_to_first(self):
    self.curr_comb = list(self.first_comb)
    return self.curr_comb

  def move_curr_comb_to_last(self):
    self.curr_comb = list(self.last_comb)
    return self.curr_comb

  def move_to_one_before_first(self):
    self.curr_comb = list(self.comb_before_first)
    return self.curr_comb

  def gen_all_combs(self):
    self.move_curr_comb_to_first()
    local_count = 0
    while self.curr_comb:
      yield self.curr_comb
      # when next() hits last_comb, curr_comb becomes None, the while-loop exit condition
      self.next()

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
    if self.curr_comb[pos] > self.greatest_index:
      errmsg = 'Index in Combiner exceeds upLimit(=%d). There is probably a bug. self.iArray[%d]=%d :: ' %(self.greatest_index, pos, self.curr_comb[pos])
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
    if self.curr_comb[pos] > self.greatest_index - back_pos:
      errmsg = 'Index in Combiner exceeds upLimit(=%d). There is probably a bug. self.iArray[%d]=%d :: ' %(self.greatest_index, pos, self.curr_comb[pos])
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
      return self.move_curr_comb_to_last()  # iArrayToDiscard = self.move_to_last_one()
    if self.overlap:
      if self.curr_comb[pos - 1] == self.greatest_index:
        return self.foward_n_positions(pos - 1)
      self.curr_comb[pos - 1] += 1
      self.correct_remaining_to_the_right_overlap_case(pos - 1)
      return self.curr_comb
    else:
      pos_ant = pos - 1
      back_pos_ant = self.n_slots - pos_ant - 1
      if self.curr_comb[pos_ant] == self.greatest_index - back_pos_ant:
        return self.foward_n_positions(pos - 1)
      self.curr_comb[pos - 1] += 1
      self.correct_remaining_to_the_right_non_overlap_case(pos - 1)
      return self.curr_comb

  def vai_um_in_place_overlap_case(self, pos):
    """
    Case of "goes one" when overlap=True
    """
    if pos == 0 and self.curr_comb[pos] == self.greatest_index:
      self.move_curr_comb_to_last()  # iArrayToDiscard = self.move_to_last_one()
      return None
    if self.curr_comb[pos] == self.greatest_index:
      return self.vai_um_in_place_overlap_case(pos - 1)
    self.curr_comb[pos] += 1
    self.correct_remaining_to_the_right_overlap_case(pos)
    return self.curr_comb

  def vai_um_in_place_non_overlap_case(self, pos):
    """
    Case of vaiUm when overlap=False
    """
    back_pos = self.n_slots - pos - 1
    if pos == 0 and self.curr_comb[pos] == self.greatest_index - back_pos:
      self.move_curr_comb_to_last()  # iArrayToDiscard = self.move_to_last_one()
      return None
    if self.curr_comb[pos] == self.greatest_index - back_pos:
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
        self.move_curr_comb_to_first()
        return None
    if self.curr_comb[pos - 1] == self.curr_comb[pos]:
      self.curr_comb[pos] = self.greatest_index
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
      self.move_curr_comb_to_first()
      return None
    if self.curr_comb[pos - 1]+1 == self.curr_comb[pos]:
      debit_to_up_limit = self.n_slots - pos - 1
      self.curr_comb[pos] = self.greatest_index - debit_to_up_limit
      return self.minus_one_non_overlap(pos - 1)
    else:
      self.curr_comb[pos] -= 1
    return self.curr_comb

  def previous(self):
    """
    Moves iArray to its previous consistent position and returns the array
    When the first one is current, None will be returned
    """
    if self.curr_comb == self.comb_before_first:
      return self.curr_comb
    if self.curr_comb == self.first_comb:
      self.curr_comb = list(self.comb_before_first)
      return self.curr_comb
    if self.curr_comb is None:  # this convention may be reviewd later one
      return self.move_curr_comb_to_last()
    pos = self.n_slots - 1
    if self.overlap:
      return copy.copy(self.minus_one_overlap(pos))
    else:
      return copy.copy(self.minus_one_non_overlap(pos))

  def next_under_overlap(self):
    # check before first element
    if self.curr_comb is not None and self.curr_comb == [-1] * self.n_slots:
      # switch it off independently of next if's result
      return self.move_curr_comb_to_first()
    if pos == -1:
      pos = self.n_slots - 1
      # if self.iArray[pos]+1 > self.greatest_index:
    if self.overlap:
      up_limit = self.greatest_index
    else:
      up_limit = self.greatest_index - (self.n_slots - pos - 1)
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
    self.curr_comb = ICf.add_one(self.curr_comb, up_limit=self.greatest_index)
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
    if self.greatest_index == 1 and self.n_slots == 2:
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
    if upto > self.total_comb:
      upto = self.total_comb
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
    if p_pos == 0 and self.curr_comb[p_pos] + 1 > self.greatest_index:
      return None
    if self.curr_comb[p_pos] + 1 > self.greatest_index:
      if self.curr_comb[p_pos - 1] + 1 > self.greatest_index:
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
    if p_pos == 0 and self.curr_comb[p_pos] + 1 > self.greatest_index - (self.n_slots - p_pos - 1):
      return None
    if self.curr_comb[p_pos] + 1 > self.greatest_index - (self.n_slots - p_pos - 1):
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
