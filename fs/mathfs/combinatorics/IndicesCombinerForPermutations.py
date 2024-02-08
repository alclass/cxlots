#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/IndicesCombinerForPermutations.py
  Contains the class IndicesCombinerForPermutations

History Notice:

  In previous versions of this system, the main class IndicesCombiner had a paramater
    called overlap (either True or False) that represented one of two schemes,
    these two are:
      o1 overlap True meant an ascending ordered permutation
        example: [0, 0, 0], [0, 0, 1], ..., [3, 3, 3]
      o2 overlap False meant an ascending ordered combination
        example: [0, 1, 2], [0, 1, 3], ..., [1, 2, 3]

  Because of some differences in dealing with each case (overlap and NOT overlap)
    the class was split into two, one for the overlap case (IndicesCombinerForPermutations)
    and the other for the not-overlap (IndicesCombinerForCombinations).

As a side notice, the 'technique' of the lexicographic index, at the time of this writing,
   is known only for the combination case (ie, the non-overlap case mentioned here).
In time, we hope to find out a 'technique' for the lexicographic index for the overlap case

@see also as a reference: http://en.wikipedia.org/wiki/Combinadic
"""
import copy
import fs.mathfs.combinatorics.combinatoric_algorithms as ca  # ca.fact(n)
import fs.mathfs.combinatorics.IndicesCombiner_functions as ICf  # ICf.project_last_combinationlist


def is_first_comb_lexicographacally_less_than_the_second(first_comb, second_comb):
  two_by_2 = zip(first_comb, second_comb)
  bool_list = list(map(lambda tupl: tupl[0] < tupl[1], two_by_2))
  if True in bool_list:
    return True
  return False


def is_first_comb_lexicographacally_greater_than_the_second(first_comb, second_comb):
  two_by_2 = zip(first_comb, second_comb)
  bool_list = list(map(lambda tupl: tupl[0] > tupl[1], two_by_2))
  if True in bool_list:
    return True
  return False


def verify_lexicographical_comb_must_be_within_first_n_last_or_raise(inbetween_comb, ini_comb, fim_comb):
  # notice that first_comb and last_comb are equally sized from their origins
  if len(inbetween_comb) != len(ini_comb):
    errmsg = f"len(inbetween_comb)={len(inbetween_comb)} != len(first_comb)={len(ini_comb)}"
    raise ValueError(errmsg)
  intbetwen_is_less = is_first_comb_lexicographacally_less_than_the_second(inbetween_comb, ini_comb)
  if intbetwen_is_less:
    error_cause = 'LESS'
    errmsg = (f'parameter comb (combination={inbetween_comb}) is'
              f' lexicographical-{error_cause} than the initial value {ini_comb}')
    raise ValueError(errmsg)
  intbetwen_is_greater = is_first_comb_lexicographacally_greater_than_the_second(fim_comb, inbetween_comb)
  if intbetwen_is_greater:
    error_cause = 'MORE'
    errmsg = (f'parameter comb (combination={inbetween_comb}) is'
              f' lexicographical-{error_cause} than the initial value {fim_comb}')
    raise ValueError(errmsg)


class IndicesCombinerForPermutations:
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

  When ini_comb and fim_comb are given:

  Example:
    indComb = IndicesCombiner(5, 3, True, [2,2,3])

  In this example, [2, 2, 3] represents ini_comb.
  Remind that the first comb under an overlap scheme with 3 slots is [0, 0, 1]
    and if n_elements = 4 (or upLimit = 3), the last comb is [3, 3, 3]
    (beginning = [0, 0, 0] , ending = [3, 3, 3])
  But now, with an ini_comb given, the whole combination set is shortened to
    (beginning = [2, 2, 3] , ending = [3, 3, 3])
  When [2, 2, 3] is called the "restartAt" array
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

  This parameter combination (n_elements with n_slots) may be confusing at first, but notice that:

    overlap=False
      implements a combination scheme (lexicographically ascending in order).
        here, n_elements (or upLimit-1) must be not less than n_slots
        its minimal form is [0, 1, 2, ..., n-1] where n is both n_slots and n_elements
      here, n_elements may be greater than or equal to n_slots, never less than it.

    overlap=True
      does not implement a combination scheme, but an ascending ordered permutation.
      So, for instance, [0, 0, 0, 1] is possible,
        case in which n_elements (=2) is less than n_slots (=4)
      here, n_elements may indeed be less than n_slots, but, at its lower limits,
        if n_elements = 1, n_slots can only be 1 or the scheme becomes "indefinite",
        ie, if elements = [0], n_slots should be 1.

  At the time of this writing (Jan 2024: this module is refactored from its beginnings in 2011!),
    we still don't know if there is or isn't a lexicographical index-generator
      analytical function for the ascending ordered permutation (overlap=True) proposed here.

  At this moment, it's known that lexicographical indices can be analytically (ie, with a function)
    produced from the combinations themselves. The function is placed in the 'lexicographical_indices'
    module.  But, again, that is available only for overlap=False, ie, for the combination scheme.

  TO-DO: maybe, to solve this "mismatch", this class might be split into two,
         one for each overlap kind.
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
  def greatest_int_in_comb(self):
    """
    greatest_int_in_comb was formerly called "up_limit"
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
        self._last_comb = [self.greatest_int_in_comb] * self.n_slots
      else:
        cut_pos = self.greatest_int_in_comb - self.n_slots + 1
        self._last_comb = list(range(cut_pos, self.greatest_int_in_comb + 1))
    return self._last_comb

  @property
  def total_cmbs(self):
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
    """
    This is the same as total_cmbs (total combinations)
    The combination itself has its own size, that one is given by self.n_slots
    Also: len(self.curr_comb) is equal to self.n_slots
    """
    return self.total_cmbs

  def restore_curr_comb_to_its_inipos_given_or_first(self):
    """
    Returns the get_first_given/restartAt array changing current position to it
    @see also get_first_given()
    """
    if self.ini_comb:
      self.curr_comb = list(self.ini_comb)
    else:
      self.curr_comb = list(self.first_comb)
    return self.curr_comb

  def move_curr_comb_to_first_or_ini(self):
    if self.ini_comb:
      self.curr_comb = list(self.ini_comb)
    else:
      self.curr_comb = list(self.first_comb)
    return self.curr_comb

  def move_curr_comb_to_last_or_fim(self):
    if self.fim_comb:
      self.curr_comb = list(self.fim_comb)
    else:
      self.curr_comb = list(self.last_comb)
    return self.curr_comb

  def move_to_one_before_first(self):
    """
    It's conventioned that curr_comb has value [-1]*n_slots before the first position.
      and, on the opposite side, None after the last position.
    """
    self.curr_comb = list(self.comb_before_first)
    return self.curr_comb

  def move_to_one_after_last(self):
    """
    It's conventioned that curr_comb has value None after the last position.
      and, on the opposite side, [-1]*n_slots before the first position.
    """
    self.curr_comb = None
    return self.curr_comb

  def is_curr_comb_lexicographacally_less_than_given_ini_comb(self):
    first_comb = self.curr_comb
    second_comb = self.fim_comb
    return is_first_comb_lexicographacally_less_than_the_second(first_comb, second_comb)

  def is_curr_comb_lexicographacally_greater_than_given_fim_comb(self):
    first_comb = self.curr_comb
    second_comb = self.fim_comb
    return is_first_comb_lexicographacally_greater_than_the_second(first_comb, second_comb)

  def gen_all_cmbs_or_those_bw_ini_fim_if_given(self):
    """
    This generator "yields" all combinations not considering self.ini_comb or self.fim_comb
    For this other functionality (limits between ini & fim) @see above
      method gen_combs_between_given_ini_n_fim()
    """
    self.move_curr_comb_to_first_or_ini()
    while self.curr_comb:
      yield self.curr_comb
      # when next() hits last_comb, curr_comb becomes None, the while-loop exit condition
      if self.fim_comb:
        # but, if fim_comb was given at __init__, that becomes the while-loop exit condition
        if self.is_curr_comb_lexicographacally_greater_than_given_fim_comb():
          break
      self.next()

  def get_all_cmbs_or_those_bw_ini_fim_if_given(self, cut_off=1000):
    """
    This method, though it's still here, should be used with caution in the sense
      that it may be, in larger cases, memory-hungry, so to say.

    IMPORTANT:
      i1 there is a cut_off parameter that should also be used with caution;
      i2 its default is 1000 (at the time of writing), if None, that means no "cut-off";
      i3 one way out of this memory problem is to use the "gen" method version directly,
        ie gen_all_cmbs_or_those_bw_ini_fim_if_given(),
        which "yields" every element avoiding keeping a "huge set" (if that is the case) in memory;

    This method reuses its "generator" version (@see above)
       keeping everything into an output array.
       (That corroborates to the memory-caution mentioned above.)
    """
    output_combs = []
    counter = 0
    for _ in self.gen_all_cmbs_or_those_bw_ini_fim_if_given():
      counter += 1
      # remind that cut_off is a sort of protection valve to avoid a memory crash if set is big enough for that
      # if it's passed in as None, no cut-off will be present and the output may be huge in large sets
      if cut_off and counter > cut_off:
        break
      output_combs.append(self.curr_comb)
    return output_combs

  def previous(self):
    """
    Moves iArray to its previous consistent position and returns the array
    When the first one is current, None will be returned
    """
    pass

  def next_under_overlap(self):
    pass

  def next_under_nonoverlap(self):
    self.curr_comb = next_in_overlap(self.curr_comb)
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


def correct_right_side(alist, pos):
  pass


def next_in_overlap(alist, n_elements, pos=None):
  """
  n_elements=4 | n_slots=2
  00 01 02 03 11 12 13 22 23 33 : total=10
  Notice that the combination here follows the rule
    xy where x <= y, ie combinations such as 10 and 21 are not this rule-compliant
  Curiosity: the overlap-mode is the composed of the "combinations"
    plus "xx" where the two digits are repeated (00 11 22 33)

  """
  n_slots = len(alist)
  pos = n_slots - 1 if pos is None else pos
  upperlimit = n_elements - 1
  # min_vals = [0] * n_slots
  max_vals = [upperlimit] * n_slots
  max_val_at_pos = max_vals[pos]
  if alist == max_vals:
    return None
  val_at_pos = alist[pos]
  if val_at_pos < max_val_at_pos:
    val_at_pos += 1
    alist[pos] = val_at_pos
    correct_right_side(alist, pos)
    return alist
  # vai um if possible
  pos -= 1
  return next_in_overlap(alist, n_elements, pos)


def gen_overlap_combs(n_elements, n_slots):
  first = '0'*len(n_slots)
  curr = list(first)
  while curr is not None:
    print(curr)
    curr = next_in_overlap(curr)
    yield curr
  return None


def adhoctest2():
  exp_overlap_combs = ['00', '01', '02', '03', '11', '12', '13', '22', '23', '33']


def adhoctest():
  exp_overlap_combs = ['00', '01', '02', '03', '11', '12', '13', '22', '23', '33']
  alist, n_elements = [0, 1], 4
  for i in range(20):
    previous = list(alist)
    alist = next_in_overlap(alist, n_elements, pos=None)
    print(previous, alist)


if __name__ == '__main__':
  """
  """
  adhoctest()
