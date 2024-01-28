#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/IndicesCombinerForCombinations.py
  Contains the class IndicesCombiner that models a combinadic object
  (@see ref @wikipedia below)

History Notice:
  In previous versions of this system, the main class IndicesCombiner had a paramater
    called overlap (either True or False) that represented one of two schemes, these two are.
      overlap True meant an ascending ordered permutation
        example: [0, 0, 0], [0, 0, 1], ..., [3, 3, 3]
      overlap False meant an ascending ordered combination
        example: [0, 1, 2], [0, 1, 3], ..., [1, 2, 3]

  Because of some differences in dealing with each case (overlap and NOT overlap)
    the class was split into two, one for the overlap case and the other for the not-overlap.

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


def verify_lexicographical_comb_must_be_within_first_n_last_or_raise(middle_comb, min_comb, max_comb):
  # notice that first_comb and last_comb are equally sized from their origins
  if len(middle_comb) != len(min_comb):
    errmsg = f"len(inbetween_comb)={len(middle_comb)} != len(first_comb)={len(min_comb)}"
    raise ValueError(errmsg)
  intbetwen_is_less = is_first_comb_lexicographacally_less_than_the_second(middle_comb, min_comb)
  if intbetwen_is_less:
    error_cause = 'LESS'
    errmsg = (f'parameter comb (combination={middle_comb}) is'
              f' lexicographical-{error_cause} than the initial value {min_comb}')
    raise ValueError(errmsg)
  intbetwen_is_greater = is_first_comb_lexicographacally_greater_than_the_second(middle_comb, max_comb)
  if intbetwen_is_greater:
    error_cause = 'MORE'
    errmsg = (f'parameter comb (combination={middle_comb}) is'
              f' lexicographical-{error_cause} than the initial value {max_comb}')
    raise ValueError(errmsg)


class IndicesCombinerForCombinations:
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

  def __init__(self, n_elements=1, n_slots=1, ini_comb=None, fim_comb=None):
    self.n_elements = n_elements
    self.n_slots = n_slots
    self.ini_comb = ini_comb
    self.fim_comb = fim_comb
    self.curr_comb = None
    self._first_comb = None
    self._last_comb = None
    self.comb_before_first = None  # [-1] * self.n_slots
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
    if self.n_elements < self.n_slots:
      errmsg = (f'Inconsistent IndicesCombiner n_elements (given value {self.n_elements})'
                f' must be greater or at least equal to n_slot={self.n_slots}')
      raise ValueError(errmsg)
    if self.n_slots < 1:
      errmsg = ("At this version, it's been decided not to allow n_slots=0 => parameters are:"
                f' (n_elements={self.n_elements}, n_slot={self.n_slots})')
      raise ValueError(errmsg)

  def check_consistency_of_ini_comb_n_fim_comb(self):
    # init self.curr_comb based on whether it's pos after zero or the zero pos
    self.comb_before_first = [-1] * self.n_slots
    if self.ini_comb is None:
      self.ini_comb = list(self.first_comb)
      self.curr_comb = list(self.first_comb)
    else:
      # the verification below also checks that len(self.curr_comb) is equal to self.n_slots
      verify_lexicographical_comb_must_be_within_first_n_last_or_raise(self.ini_comb, self.first_comb, self.last_comb)
      self.curr_comb = list(self.ini_comb)
    if self.fim_comb is None:
      self.fim_comb = list(self.last_comb)
    else:
      verify_lexicographical_comb_must_be_within_first_n_last_or_raise(self.fim_comb, self.first_comb, self.last_comb)

  @property
  def lgi_b1idx(self):
    """
      Calculates the lexicographical index of a combination.

    The lgi_b1idx is an integer that represents a combination, starting from 1 (under 1-based indices)
    and ending with the integer that represents the total combinations.

    As a simple example: suppose:
      IndicesCombiner n_elements=3 n_slots=2 size=3 first_cmbs=[[0, 1], [0, 2], [1, 2]]
        combination [0, 1] is index 1 (as index 0 if it's under 0-based indices)
        combination [0, 2] is index 2
        combination [1, 2] is index 3

    @see more info and explanation in docstring for function:
      ca.calc_lgi_from_comb_where_ints_start_at_0(cmbset, n_elements)
    """
    lgi_computed = ca.calc_lgi_from_comb_where_ints_start_at_0(self.curr_comb, self.n_elements)
    return lgi_computed

  @property
  def lgi_b0idx(self):
    return self.lgi_b1idx - 1

  @property
  def greatest_int_in_comb(self):
    """
    greatest_int_in_comb was formerly called "up_limit" (or upLimit)
    least_index is "commonly" 0, so there's not a @property for it

    Example:
      [0, 1, 2], greatest_int_in_comb=2, self.n_elements=3, self.n_slots=3,
    General Example:
      [0, 1, 2, ..., n-1], greatest_int_in_comb=n-1, self.n_elements=n, self.n_slots=n,
    """
    return self.n_elements - 1

  def is_comb_valid_in_relation_to_elements_n_slots(self, p_comb):
    if p_comb is None:
      return False
    if len(p_comb) != self.n_slots:
      return False
    if len(p_comb) == 1 and list(p_comb) != [0]:
      return False
    bool_array = [p_comb[i] < p_comb[i+1] for i in range(len(p_comb)-1)]
    if False in bool_array:
      return False
    return True

  def check_subset_asc_order_consistency(self, ini_comb, fim_comb, cut_off=10):
    """
    Checks the consistency of iArray
    Examples of inconsistent arrays of combinations:
    (in older version, it was overlap=False)
      valid ==>> [0,1,2], [0,1,100]
      invalid ==>> [0,0,0], [2,2,3] (though these two are valid in mode overlap=True, ie permutations
      invalid ==>> [2,1,0] invalid even for permutations, because order should never be descending
    """
    if ini_comb in None:
      ini_comb = list(self.first_comb)
    if fim_comb in None:
      fim_comb = list(self.last_comb)
    if not self.is_comb_valid_in_relation_to_elements_n_slots(ini_comb):
      errmsg = f"comb {ini_comb} is invalid for n_elements={self.n_elements} and n_slots={self.n_slots}"
      raise ValueError(errmsg)
    if not self.is_comb_valid_in_relation_to_elements_n_slots(fim_comb):
      errmsg = f"comb {fim_comb} is invalid for n_elements={self.n_elements} and n_slots={self.n_slots}"
      raise ValueError(errmsg)
    if not is_first_comb_lexicographacally_less_than_the_second(ini_comb, fim_comb):
      errmsg = f"ini_comb {ini_comb} is not less than fim_comb {fim_comb}"
      raise ValueError(errmsg)

  def position_curr_comb_before_first(self):
    """
    By convention, the element in "position before first" (a kind of marker)
      is [-1]*n_slots
    At the opposite side, the element in "position after last"
      is None
    """
    self.curr_comb = list(self.comb_before_first)

  @property
  def first_comb(self):
    """
    first_comb is list(range(n_slots))
    Examples:
      e1 if n_slots = 3 than first_comb is [0, 1, 2]
      e2 if n_slots = 6 than first_comb is [0, 1, 2, 3, 4, 5]
    Obs: first_comb does not depend on n_elements,
         on the other hand, last_comb below does depend on it
    """
    if self._first_comb is None:
      self._first_comb = list(range(self.n_slots))
    return self._first_comb

  @property
  def ini_comb_given(self):
    if self.ini_comb:
      return self.ini_comb
    return self.first_comb

  @property
  def last_comb(self):
    """
    last_comb is list(range(cut_pos, self.greatest_int_in_comb + 1))
      cut_pos is self.greatest_int_in_comb - self.n_slots + 1
    Examples:
      e1 n_slots = 3, n_elements=4 than greatest_int_in_comb=3 & cut_pos=1
        and last_comb is [1, 2, 3]
      e2 n_slots = 6, n_elements=60 than greatest_int_in_comb=59 & cut_pos=54
        and last_comb is [54, 55, 56, 57, 58, 59]
    """
    if self._last_comb is None:
      cut_pos = self.greatest_int_in_comb - self.n_slots + 1
      self._last_comb = list(range(cut_pos, self.greatest_int_in_comb + 1))
    return self._last_comb

  @property
  def total_cmbs(self):
    """
      Gives the total number of combinations dependent on n_elements & n_slots
    It uses the formula:
      comb_of_n_m_by_m = n! / ((n - m)! * m!)
    For example:
      the MS (Megasena cardgame) has 50063860 combinations,
      ie C = 60! / (54! * 6!) = 50063860
      (ie n_elements=60 & n_slots=6 generate a total number of combinations a bit greater than 50MM)
    """
    if self.n_slots == self.n_elements:
      return 1
    if self.n_slots == 1:
      return self.n_elements
    n = self.n_elements
    m = self.n_slots
    num = ca.fact(n)
    den = ca.fact(n - m) * ca.fact(m)
    total_combinations = num / den
    # total_combinations should be a countable integer
    return int(total_combinations)

  @property
  def size(self):
    """
    This is the same as total_cmbs (total combinations)
    The combination itself as a list has its own size, that one is given by self.n_slots
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
    It's conventioned here that curr_comb has value [-1]*n_slots before the first position.
      and, on the opposite side, has value None after the last position.
    """
    self.curr_comb = list(self.comb_before_first)
    return self.curr_comb

  def move_to_one_after_last(self):
    """
    It's conventioned that curr_comb has value None after the last position.
      and, on the opposite side, has value [-1]*n_slots before the first position.
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

  def gen_all_lgis_n_cmbs_or_those_bw_ini_fim_if_given(self):
    for _ in self.gen_all_cmbs_or_those_bw_ini_fim_if_given():
      tupl_lgi_n_cmb = self.lgi_b1idx, self.curr_comb
      yield tupl_lgi_n_cmb

  def gen_all_cmbs_or_those_bw_ini_fim_if_given(self):
    """
    This generator "yields" all combinations considering self.ini_comb and self.fim_comb
      if given at __init__()
    The generator technique (with yield <variable>) is memory-saving
      for the whole set, when kept in memory, may use of lots of if set is "big"
    The "opposite" method get_all_cmbs_or_those_bw_ini_fim_if_given()
      'consumes' this generator entirely and kepts the set in memory.
    Advice is given to prefer this generator and avoid the 'get' version if output set is "big".
    Example: the MS set has 50063860 combinations (about 50MM).
    """
    self.move_curr_comb_to_first_or_ini()
    while self.curr_comb is not None:
      yield self.curr_comb
      # when next() hits last_comb, curr_comb becomes None, which is a while-loop exit condition
      if self.fim_comb:
        # but, if fim_comb was given at __init__, that becomes a second while-loop exit condition
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
       (That corroborates to the memory-caution mentioned above if output set is big.)
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
    if self.curr_comb == self.comb_before_first:
      return self.curr_comb
    if self.curr_comb == self.first_comb:
      self.curr_comb = list(self.comb_before_first)
      return self.curr_comb
    if self.curr_comb is None:  # this convention may be reviewd later one
      return self.move_curr_comb_to_last_or_fim()
    pos = self.n_slots - 1
    if self.overlap:
      return copy.copy(self.minus_one_overlap(pos))
    else:
      return copy.copy(self.minus_one_non_overlap(pos))

  def next(self):
    """
    Moves curr_comb position to the next consistent one and returns it
    When the last one is current, a next() will move it to None that is also returned
    (thus, None becomes here a kind of convention of "after the last" or "parked after the last")
    """
    self.curr_comb = ICf.add_one(self.curr_comb, up_limit=self.greatest_int_in_comb)
    return self.curr_comb

  def __str__(self):
    """
    The object's string representation contains n_elements, n_slots, overlap &
      the first 10 (or less) combination elements.
    """
    ne = self.n_elements
    ns = self.n_slots
    sz = self.size
    first_n_combs = self.get_all_cmbs_or_those_bw_ini_fim_if_given(cut_off=10)
    out_str = f'IndicesCombiner n_elements={ne} n_slots={ns} size={sz} first_cmbs={first_n_combs}'
    return out_str


def adhoc_test():
  """
  n_elements, n_slots = 4, 3
  icc = IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots)
  print(icc)
  n_elements, n_slots = 1, 1
  icc = IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots)
  print(icc)
  n_elements, n_slots = 2, 1
  icc = IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots)
  print(icc)
  n_elements, n_slots = 3, 2
  icc = IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots)
  print(icc)

  """
  n_elements, n_slots = 3, 2
  icc = IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots)
  print(icc)
  n_elements, n_slots = 4, 3
  icc = IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots)
  print(icc)
  n_elements, n_slots = 60, 6
  icc = IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots, ini_comb=[53, 55, 56, 57, 58, 59])
  print(icc)
  c = 0
  for tupl in icc.gen_all_lgis_n_cmbs_or_those_bw_ini_fim_if_given():
    c += 1
    print(c, tupl)
    if c >= 20:
      break
  n_elements, n_slots = 5, 3
  icc = IndicesCombinerForCombinations(n_elements=n_elements, n_slots=n_slots)
  icc.move_curr_comb_to_last_or_fim()
  print(icc.curr_comb, icc.lgi_b1idx)
  icc.move_curr_comb_to_first_or_ini()
  print(icc.curr_comb, icc.lgi_b1idx)


if __name__ == '__main__':
  """
  """
  adhoc_test()
