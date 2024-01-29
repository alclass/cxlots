#!/usr/bin/env python
"""
fs/mathfs/combinatorics/IndicesCombiner_functions.py

"""
import copy
import sys
import fs.mathfs.combinatorics.combinatoric_algorithms as ca  # ca.fact(n)


def get_decrescent_integer_sequence_for_later_summation_of_n(n):
  """
  Explanation:
    integer sequence for n is [0, 1, 2, ..., n]
    but for the 'logical' summation, it's inverted, ie [n, n-1, n-2, ..., 2, 1, 0]
    of course, a summation is the same no matter how its constituents are placed,
      but here there's a logical positioning
  Example:
    f(0) = [0]
    f(1) = [1, 0]
    f(2) = [2, 1, 0]
    f(3) = [3, 2, 1, 0]
    f('blah') = None
    f(-2) = None
  """
  try:
    n = int(n)
  except (TypeError, ValueError):
    return None
  if n < 0:
    return None
  int_sequence_in_sum = [e for e in range(n, -1, -1)]
  return int_sequence_in_sum


def get_distance_from_the_summation_scheme(n_elements, pos):
  """
  This function uses the 'idea' behind the integers composing the summation that is alternative to total_combinations.
  This function helps find the "vai um" for subtract_one() (or previous())

  Rationale Explanation
  =====================

  The combination sequence total can also be seen as a summation of n-1, ie:
    C(n, m) = Sum(n-1)
  In the example for IC(n_elements=4, n_slots=3), we have:
    C(n, m) => C(4, 2) = 4! / (4-2)! 2! = 6
  Also, we have:
    S(n-1) => S(4-1) = S(3) = 3 + 2 + 1 = 6
  The decreasing integers (3, 2, 1), seen in the summation, also show the 'distances within combinants', ie:
    '3' shows that there are 3 elements [0, n] (@see them either in docstring for add_one() or subtract_one())
    '2' shows that there are 2 elements [1, n]
    '1' shows that there are 1 element [2, n]
  This 'idea' can help in the strategy for subtract_one() (or previous())
  decrescent_integer_sequence = [3, 2, 1, 0]  # the ending zero is more theoretical than practical
  """
  max_value = n_elements - 1  # min_value = 0
  int_sequence_in_sum = get_decrescent_integer_sequence_for_later_summation_of_n(max_value)
  if pos > len(int_sequence_in_sum) - 1:
    return None
  distance_at_pos = int_sequence_in_sum[pos]
  return distance_at_pos


def add_one(numberlist, n_elements, lastcomb=None, pos=None):
  """
    "Adds one" to a combinatory numberlist.
    add_one() also means next()

  Example:
    ic = IndicesCombiner(n_elements=4, n_slots=2) we have:
    combination_elements = [[0, 1], [0, 2],[0, 3],[1, 2],[1, 3],[2, 3]]  # 6 total
  In the ic object above:
    next([0, 1]) = [0, 2]  # first one [0, 1]
    next([0, 2]) = [0, 3]
    next([0, 3]) = [1, 2]
    and so on up to
    next([1, 3]) = [2, 3]  # last one [2, 3]
    next([2, 3]) = None  # adding one to the last one results None
    next(None) = None  # adding one to None also results None
  """
  # up_limit = n_elements - 1
  if numberlist is None:
    return None
  if not isinstance(numberlist, list):
    print(f'Error not isinstance(numberlist, list) numberlist = {numberlist}')
    sys.exit(1)
  n_slots = len(numberlist)
  elem_min, elem_max = n_elements - n_slots, n_elements - 1
  lastcomb = lastcomb if lastcomb is not None else [i for i in range(elem_min, elem_max+1)]
  if numberlist == lastcomb:
    return None  # it means it can't add one to the last one
  if pos is None:
    pos = len(numberlist) - 1
  max_at_pos = lastcomb[pos]
  number_at_pos = numberlist[pos]
  if number_at_pos == max_at_pos:
    if pos > 0:
      # recursive call traversing the indices leftwards
      return add_one(numberlist, n_elements, lastcomb, pos-1)
    else:
      # can't add to it anymore, ie, it's already the last one
      return None
  # from this point, number_at_pos < max_at_pos, then adding can happen
  added_one = number_at_pos + 1
  next_numberlist = copy.copy(numberlist)
  next_numberlist[pos] = added_one
  if pos == n_slots - 1:
    return next_numberlist
  for ipos in range(pos+1, n_slots):
    # when an adding happens not at the last pos, an integer sequence follows for the pos being added rightwards
    # example: 1[2]67 becomes 1[3]45 the integer sequence is 3, 4, 5 because 3 happened when "2 was added by one"
    # the [] above are just to emphasize which number was added one
    next_numberlist[ipos] = next_numberlist[ipos-1] + 1
  return next_numberlist


def project_first_combinationlist(n_elements, n_slots):
  if n_slots > n_elements:
    greatest_int_in_comb = n_elements - 1
    errmsg = f'n_slots (={n_slots}) > greatest_int_in_comb (={greatest_int_in_comb}) + 1 (={n_elements})'
    raise ValueError(errmsg)
  first_combination = list(range(n_slots))
  return first_combination


def project_last_combinationlist(n_elements, n_slots):
  """
  Examples:
    f(greatest_int_in_comb=2, n_slots=3) = [0, 1, 2]
    f(greatest_int_in_comb=5, n_slots=3) = [3, 4, 5]
    f(greatest_int_in_comb=7, n_slots=2) = [6, 7]
    f(greatest_int_in_comb=7, n_slots=2) = [6, 7]
    f(greatest_int_in_comb=2, n_slots=4) => raises ValueError because it would go "below zero" [-1, 0, 1, 2] not allowed
  """
  if n_slots > n_elements:
    greatest_int_in_comb = n_elements - 1
    errmsg = (f'n_slots (={n_slots}) > greatest_int_in_comb (={greatest_int_in_comb})'
              f' + 1 (n_elements={n_elements})')
    raise ValueError(errmsg)
  elem_min, elem_max = n_elements - n_slots, n_elements - 1
  last_combination = [i for i in range(elem_min, elem_max+1)]
  return last_combination


class CombinationAdderSubtracter:

  def __init__(self, n_elements, n_slots, curr_comb=None):
    self.n_elements, self.n_slots = n_elements, n_slots
    self._first_comb = None
    self.before_first_comb = None
    self._last_comb = None
    self.after_last_comb = None
    self._elems_min_at_pos = None
    self._elems_max_at_pos = None
    self.add_sub_calls = 0
    self.curr_comb = curr_comb if curr_comb is not None else list(self.first_comb)

  @property
  def first_comb(self):
    """
    """
    if self._first_comb is None:
      self._first_comb = project_first_combinationlist(self.n_elements, self.n_slots)
      self.before_first_comb = [-1] * self.n_slots
    return self._first_comb

  @property
  def last_comb(self):
    """
    """
    if self._last_comb is None:
      self._last_comb = project_last_combinationlist(self.n_elements, self.n_slots)
    return self._last_comb

  def get_min_elem_at_pos(self, pos):
    return self.first_comb[pos]

  def get_max_elem_at_pos(self, pos):
    return self.last_comb[pos]

  def is_currcomb_before_first(self):
    if self.curr_comb == self.before_first_comb:
      return True
    return False

  def is_currcomb_after_last(self):
    if self.curr_comb is None:
      return True
    return False

  def add_one(self):
    if self.curr_comb is None:
      return self.after_last_comb
    if self.curr_comb == self.before_first_comb:
      self.curr_comb = list(self.first_comb)
      return self.curr_comb
    self.add_sub_calls += 1
    self.curr_comb = add_one(self.curr_comb, n_elements=self.n_elements, lastcomb=self.last_comb)
    return self.curr_comb

  def subtract_one(self):
    if self.curr_comb is None:
      self.curr_comb = list(self.last_comb)
      return self.curr_comb
    if self.curr_comb == self.before_first_comb:
      return self.before_first_comb
    self.add_sub_calls += 1
    self.curr_comb = subtract_one(numberlist=self.curr_comb, n_elements=self.n_elements)
    if self.curr_comb is None:
      self.curr_comb = list(self.before_first_comb)
    return self.curr_comb

  def __str__(self):
    outstr = f"""AdderSubtracter currcomb={self.curr_comb} | nelements={self.n_elements} | nslots={self.n_slots}
    firstcomb={self.first_comb} | lastcomb={self.last_comb} | add_sub_calls={self.add_sub_calls}"""
    return outstr


def set_rightward_digits_after_pos_to_their_max(pos, numberlist, n_elements):
  """
  This is an adjustment function for the subtract_one() need for a "vai um" kind of propagating adjustment

  Example:
    Suppose a subtract_one() happens to [1, 2, 3] where n_elements=5
    The minimal (or first) set (where n_elements=5 & n_slots=3) is [0, 1, 2],
      so the first "1" can decrease to "0", resulting in [0, 2, 3]
    but [1, 2, 3] minus_1 is in fact [0, 3, 4],
      so [0, 2, 3] needs to propagate a "correction-like vai-um" to its ending [2, 3]
    That correction is to move [2, 3] to their maximum positional values,
      ie [3, 4], because the maximum (or last) set is [2, 3, 4]

  This function does this "vai um" propagation that the example above mentions.
  """
  if pos > len(numberlist) - 1:
    return numberlist  # or None, yet to decide
  n_slots = len(numberlist)
  elem_min, elem_max = n_elements - n_slots, n_elements - 1
  # max_values_array is the same as lastcomb
  max_values_array = [i for i in range(elem_min, elem_max + 1)]
  for i in range(pos+1, n_slots):
    # this is where the propagation mentioned in the example above happens
    numberlist[i] = max_values_array[i]
  return numberlist


def subtract_one(numberlist, n_elements, pos=None):
  n_slots = len(numberlist)
  firstcomb = [i for i in range(n_slots)]
  if numberlist == firstcomb:
    return None
  pos = n_slots - 1 if pos is None else pos
  if pos < 0:
    return None
  right_side_val = numberlist[pos]
  leftpos = pos - 1
  if leftpos < 0:
    if right_side_val > 0:
      # pos here is 0 because leftpos < 0
      numberlist[pos] = right_side_val - 1
      # at this point, a propagating "vai um" must happen
      if numberlist[pos] == firstcomb[pos]:
        # propagation vai-um-like
        numberlist = set_rightward_digits_after_pos_to_their_max(pos, numberlist, n_elements)
      return numberlist
    return None
  left_side_val = numberlist[leftpos]
  if right_side_val - 1 > left_side_val:
    # done
    numberlist[pos] = right_side_val - 1
    if numberlist[pos] == firstcomb[pos]:
      # propagation vai-um-like
      numberlist = set_rightward_digits_after_pos_to_their_max(pos, numberlist, n_elements)
    return numberlist
  return subtract_one(numberlist, n_elements=n_elements, pos=pos-1)


def adhoctest():
  """
  Examples:
    f(greatest_int_in_comb=7, n_slots=2) = [6, 7]
    f(greatest_int_in_comb=4, n_slots=3) = [2, 3, 4]

  """
  n_elements, n_slots = 4, 3
  relist = project_last_combinationlist(n_elements, n_slots)
  print(relist)
  n_elements, n_slots = 7, 2
  relist = project_last_combinationlist(n_elements, n_slots)
  print(relist)
  numberlist = [0, 1, 2]
  nextone = add_one(numberlist, n_elements)
  scrmsg = f"numberlist {numberlist} plus 1 = nextone {nextone}"
  print(scrmsg)
  n_elements, n_slots = 4, 3
  numberlist = project_last_combinationlist(n_elements, n_slots)
  nextone = add_one(numberlist, n_elements)
  scrmsg = f"numberlist {numberlist} plus 1 = nextone {nextone}"
  print(scrmsg)
  numberlist = None
  nextone = add_one(numberlist, n_elements)
  scrmsg = f"numberlist {numberlist} plus 1 = nextone {nextone}"
  print(scrmsg)
  n_elements, n_slots = 5, 2
  numberlist = project_first_combinationlist(n_elements, n_slots)
  idx = 0
  scrmsg = f"first numberlist {numberlist} idx {idx}"
  print(scrmsg)
  while numberlist is not None:
    numberlist = add_one(numberlist, n_elements)
    idx += 1
    scrmsg = f"numberlist {numberlist} idx {idx}"
    print(scrmsg)


def adhoctest2():
  up_limit, n_slots = 3, 2
  lastelem = project_last_combinationlist(up_limit, n_slots)  # [2, 3]
  scrmsg = f'greatest_int_in_comb={up_limit} n_slots={n_slots} lastelem={lastelem}'
  print(scrmsg)
  firstelem = list(range(n_slots))
  scrmsg = f'greatest_int_in_comb={up_limit} n_slots={n_slots} firstelem={firstelem}'
  print(scrmsg)
  up_limit = 3
  previousone = subtract_one(lastelem, n_elements=up_limit+1)  # expects [1, 3] ie [2, 3] minus 1 = [1, 3]
  print('before', lastelem, 'previousone', previousone)
  before = copy.copy(previousone)
  previousone = subtract_one(previousone, n_elements=up_limit+1)  # expects [1, 2] ie [1, 3] minus 1 = [1, 2]
  print('before', before, 'previousone', previousone)
  before = copy.copy(previousone)
  previousone = subtract_one(previousone, n_elements=up_limit+1)  # expects [1, 2] ie [0, 3] minus 1 = [0, 2]
  print('before', before, 'previousone', previousone)
  before = copy.copy(previousone)
  previousone = subtract_one(previousone, n_elements=up_limit+1)  # expects [0, 2] ie [0, 2] minus 1 = [0, 1]
  print('before', before, 'previousone', previousone)
  before = copy.copy(previousone)
  previousone = subtract_one(previousone, n_elements=up_limit+1)  # expects [0, 1] ie [0, 2] minus 1 = None
  print('before', before, 'previousone', previousone)
  before = copy.copy(previousone)
  previousone = subtract_one(previousone, n_elements=up_limit+1)
  print('before', before, 'previousone', previousone)


def adhoctest3():
  up_limit, n_slots, pos = 3, 2, 2
  firstelem = list(range(up_limit+1))
  scrmsg = f'greatest_int_in_comb={up_limit} n_slots={n_slots} firstelem={firstelem}'
  print(scrmsg)
  distance = get_distance_from_the_summation_scheme(n_elements=up_limit+1, pos=pos)
  scrmsg = f'greatest_int_in_comb={up_limit} n_slots={n_slots} at pos={pos} distance={distance}'
  print(scrmsg)
  up_limit, n_slots, pos = 4, 3, 0
  distance = get_distance_from_the_summation_scheme(n_elements=up_limit+1, pos=pos)
  scrmsg = f'greatest_int_in_comb={up_limit} n_slots={n_slots} at pos={pos} distance={distance}'
  print(scrmsg)
  alist = get_decrescent_integer_sequence_for_later_summation_of_n(up_limit)
  print(alist, 'sum', sum(alist))
  alist = get_decrescent_integer_sequence_for_later_summation_of_n(3)
  print(alist, 'sum', sum(alist))


def adhoctest4():
  n_elements, n_slots = 4, 3
  comber = CombinationAdderSubtracter(n_elements=n_elements, n_slots=n_slots)
  print(comber)
  print('while', '='*20)
  while comber.add_one():
    print('after add one', comber)
    # comber.add_one()
  counter = 0
  print('='*40)
  print('='*40)
  while not comber.is_currcomb_before_first():
    comber.subtract_one()
    print('counter', counter, 'after subtract one', comber)
    counter += 1
    if counter > 10:
      break


def adhoctest5():
  """
  n_elements, n_slots = 4, 3
  comber = CombinationAdderSubtracter(n_elements=n_elements, n_slots=n_slots)
  comber.curr_comb = [0, 2, 3]
  print('BEFORE subtract one', comber)
  comber.subtract_one()
  print('AFTER subtract one', comber)
  subcomb = subtract_one(comb, n_elements=n_elements, lastcomb=lastcomb)
  print(comb, 'minus 1', subcomb)
  comb = list(subcomb)
  subcomb = subtract_one(comb, n_elements=n_elements, lastcomb=lastcomb)
  print(comb, 'minus 1', subcomb)
  comb = list(subcomb)
  """
  n_elements, comb = 5, [2, 3, 4]
  previouscomb = list(comb)
  idx = 0
  while 1:
    comb = subtract_one(comb, n_elements=n_elements)
    if comb is None:
      break
    print(idx, previouscomb, 'minus 1', comb)
    previouscomb = list(comb)
    idx += 1
  # =========================
  print(idx, previouscomb, 'minus 1', comb)
  print('='*40)
  comb = [0, 2, 3]
  previouscomb = list(comb)
  comb = subtract_one(comb, n_elements=n_elements)
  print(idx, previouscomb, 'minus 1', comb)


def adhoctest6():
  n_elements, n_slots = 20, 5
  # pair(greatest_int_in_comb=19, n_slots=5) above generates 15504 combinations
  # (notice that, if still greater this number, it may slow down processing depending on CPU availability etc.)
  idx = 0
  nlist = project_last_combinationlist(n_elements=n_elements, n_slots=n_slots)
  print(idx, 'first', nlist)
  all_returned_combs = [nlist]
  idx = 0
  while nlist is not None:
    returned_added_one = subtract_one(nlist, n_elements=n_elements)
    idx += 1
    print(idx, 'returned_added_one', returned_added_one)
    if returned_added_one is None:
      break
    all_returned_combs.append(returned_added_one)
    nlist = list(returned_added_one)
  print('size all_returned_combs', len(all_returned_combs))
  ncombs = ca.combine_n_c_by_c_nonfact(20, 5)
  print('ncombs', ncombs)
  nlist = project_last_combinationlist(n_elements=4, n_slots=2)
  print(nlist)


if __name__ == '__main__':
  """
  adhoctest2()
  """
  adhoctest6()
