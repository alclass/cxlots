#!/usr/bin/env python
"""
fs/mathfs/combinatorics/IndicesCombiner_functions.py

"""
import copy
import sys


def get_decrescent_integer_sequence_summation_of_n(n):
  """
  Explanation:
    integer sequence for n is [0, 1, 2, ..., n]
    but for the 'logical' summation, it's inverted, ie [n, n-1, n-2, ..., 2, 1, 0]
    of course, a summation is the same any way its constituents are placed, but here it's a logical positioning
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
  int_sequence_in_sum = int_sequence_in_sum
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
  int_sequence_in_sum = get_decrescent_integer_sequence_summation_of_n(max_value)
  if pos > len(int_sequence_in_sum) - 1:
    return None
  distance_at_pos = int_sequence_in_sum[pos]
  return distance_at_pos


def project_last_combinationlist(up_limit, n_slots):
  """
  Examples:
    f(up_limit=2, n_slots=3) = [0, 1, 2]
    f(up_limit=5, n_slots=3) = [3, 4, 5]
    f(up_limit=7, n_slots=2) = [6, 7]
    f(up_limit=7, n_slots=2) = [6, 7]
    f(up_limit=2, n_slots=4) => raises ValueError because it would go "below zero" [-1, 0, 1, 2] not allowed
  """
  if n_slots > up_limit + 1:
    errmsg = f'n_slots (={n_slots}) > up_limit (={up_limit}) + 1 (={up_limit+1})'
    raise ValueError(errmsg)
  last_combination_inversed = [up_limit-i for i in range(n_slots)]
  return list(reversed(last_combination_inversed))


def project_first_combinationlist(up_limit, n_slots):
  if n_slots > up_limit + 1:
    errmsg = f'n_slots (={n_slots}) > up_limit (={up_limit}) + 1 (={up_limit+1})'
    raise ValueError(errmsg)
  first_combination = list(range(n_slots))
  return first_combination


def get_min_at_pos(up_limit, n_slots, pos):
  projected_last = project_first_combinationlist(up_limit, n_slots)
  return projected_last[pos]


def get_max_at_pos(up_limit, n_slots, pos):
  projected_last = project_last_combinationlist(up_limit, n_slots)
  return projected_last[pos]


def add_one(numberlist, up_limit, pos=None):
  """
    "Adds one" to a combinatory numberlist.
    add_one() also means next()

  Example:
    ic = IndicesCombiner(4, 2) we have:
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
  if numberlist is None:
    return None
  if not isinstance(numberlist, list):
    print(f'Error not isinstance(numberlist, list) numberlist = {numberlist}')
    sys.exit(1)
  n_slots = len(numberlist)
  projected_last = project_last_combinationlist(up_limit, n_slots)
  if numberlist == projected_last:
    return None  # it means it can't add one to the last one
  if pos is None:
    pos = len(numberlist) - 1
  max_at_pos = get_max_at_pos(up_limit, n_slots, pos)
  number_at_pos = numberlist[pos]
  if number_at_pos == max_at_pos:
    if pos > 0:
      # recursive call traversing the indices leftwards
      return add_one(numberlist, up_limit, pos-1)
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


def subtract_one_inner(numberlist, up_limit, pos=None, dec_int_seq=None):
  """
  This function is a recursive? continuation of subtract_one()
  """
  # look ahead left to see if "vai um" is needed
  if pos is None:
    pos = len(numberlist) - 1
  if pos == 0:
    if numberlist[0] == 0:
      return None
    return do_minus_one_n_propagate(numberlist, up_limit, pos)
  if dec_int_seq is None:
    dec_int_seq = get_decrescent_integer_sequence_summation_of_n(len(numberlist))
  distance = dec_int_seq[pos]
  leftnumber = numberlist[pos-1]
  if leftnumber >= numberlist[pos] - distance:
    # recurse decreasing one from pos
    return subtract_one_inner(numberlist, up_limit, pos=pos-1, dec_int_seq=dec_int_seq)
  # else: ie leftnumber < number_at_pos - distance
  # do minus one
  return do_minus_one_n_propagate(numberlist, up_limit, pos)


def do_minus_one_n_propagate(numberlist, up_limit, pos):
  """
  # the right side number must be the highest in its possible place and propagate rightwards doing the same
  """
  previous_numberlist = copy.copy(numberlist)
  previous_numberlist[pos] = numberlist[pos] - 1
  n_slots = len(numberlist)
  propagate = True
  while propagate:
    if pos == n_slots - 1:  # ie, the last one available
      break
    pos += 1
    max_at_pos = get_max_at_pos(up_limit=up_limit, n_slots=n_slots, pos=pos)
    if previous_numberlist[pos] < max_at_pos:
      previous_numberlist[pos] = max_at_pos
      # propagate from here
      continue
    # stop propagation
    break
  return previous_numberlist


def subtract_one(numberlist, up_limit):
  """
    "Subtracts one" to a combinatory numberlist.
    add_one() also means previous()

  Example:
    ic = IndicesCombiner(4, 2) we have:
    combination_elements = [[0, 1], [0, 2],[0, 3],[1, 2],[1, 3],[2, 3]]  # 6 total
  In the ic object above:
    previous([2, 3]) = [1, 3]  # last one [2, 3]
    previous([1, 3]) = [1, 2]
    previous([1, 2]) = [0, 3]
    previous([0, 3]) = [0, 2]
    previous([0, 2]) = [0, 1]
    previous([0, 1]) = None
    and so on up to

  Strategy for subtract_one() (or previous())
  The combination sequence can also be seen as a summation of n-1, ie
  C(n, m) = Sum(n-1)
  In the example above, we have:
    C(n, m) => C(4, 2) = 4! / (4-2)! 2! = 6
  Also, we have:
    S(n-1) => S(4-1) = S(3) = 3 + 2 + 1 = 6
  The decreasing integers (3, 2, 1), seen in the summation, also show the 'distances within combinants', ie:
    '3' shows that there are 3 elements [0, n] (@see them above)
    '2' shows that there are 2 elements [1, n]
    '1' shows that there are 1 element [2, n]
  This 'idea' can help in the strategy for subtract_one() (or previous())
  This 'strategy algorithm' is implemented below.

  pos = len(numberlist) - 1
  min_at_pos = get_min_at_pos(up_limit, n_slots, pos)
  number_at_pos = numberlist[pos]
  if number_at_pos == min_at_pos:
    if pos > 0:
      # recursive call traversing the indices leftwards
      return subtract_one_inner(numberlist, pos-1)
    else:
      # can't subtract to it anymore, ie, it's already the first one
      return None
  # from this point on, number_at_pos > min_at_pos, then subtracting can happen
  n_elements = len(numberlist)
  allowed_distance = get_distance_from_the_summation_scheme(n_elements, pos)
  subtracted_one = number_at_pos - 1
  leftnumber = number_at_pos - allowed_distance
  if leftnumber == numberlist[pos] - allowed_distance:
    # recursive to 'inner'
    return subtract_one_inner(numberlist, pos-1)
  # descrease one and return
  next_numberlist = copy.copy(numberlist)
  next_numberlist[pos] = subtracted_one
  return next_numberlist

  """
  if numberlist is None:
    return None
  if not isinstance(numberlist, list):
    errmsg = f'Error not isinstance(numberlist, list) numberlist = {numberlist}'
    raise ValueError(errmsg)
  n_slots = len(numberlist)
  projected_first = project_first_combinationlist(up_limit, n_slots)
  if numberlist == projected_first:
    return None  # it means it can't subtract one to the first one
  return subtract_one_inner(numberlist, up_limit)


def adhoctest():
  """
  Examples:
    f(up_limit=7, n_slots=2) = [6, 7]
    f(up_limit=4, n_slots=3) = [2, 3, 4]

  """
  relist = project_last_combinationlist(2, 3)
  print(relist)
  relist = project_last_combinationlist(4, 3)
  print(relist)
  relist = project_last_combinationlist(7, 2)
  print(relist)
  numberlist = [0, 1, 2]
  nextone = add_one(numberlist, up_limit=3)
  scrmsg = f"numberlist {numberlist} plus 1 = nextone {nextone}"
  print(scrmsg)
  numberlist = project_last_combinationlist(up_limit=3, n_slots=3)
  nextone = add_one(numberlist, up_limit=3)
  scrmsg = f"numberlist {numberlist} plus 1 = nextone {nextone}"
  print(scrmsg)
  numberlist = None
  nextone = add_one(numberlist, up_limit=3)
  scrmsg = f"numberlist {numberlist} plus 1 = nextone {nextone}"
  print(scrmsg)
  uplim = 4
  numberlist = project_first_combinationlist(up_limit=uplim, n_slots=2)
  idx = 0
  scrmsg = f"first numberlist {numberlist} idx {idx}"
  print(scrmsg)
  while numberlist is not None:
    numberlist = add_one(numberlist, up_limit=uplim)
    idx += 1
    scrmsg = f"numberlist {numberlist} idx {idx}"
    print(scrmsg)


def adhoctest2():
  up_limit, n_slots = 3, 2
  lastelem = project_last_combinationlist(up_limit, n_slots)  # [2, 3]
  scrmsg = f'up_limit={up_limit} n_slots={n_slots} lastelem={lastelem}'
  print(scrmsg)
  firstelem = list(range(n_slots))
  scrmsg = f'up_limit={up_limit} n_slots={n_slots} firstelem={firstelem}'
  print(scrmsg)
  previousone = subtract_one(lastelem, up_limit=3)  # expects [1, 3] ie [2, 3] minus 1 = [1, 3]
  print('before', lastelem, 'previousone', previousone)
  before = copy.copy(previousone)
  previousone = subtract_one(previousone, up_limit=3)  # expects [1, 2] ie [1, 3] minus 1 = [1, 2]
  print('before', before, 'previousone', previousone)
  before = copy.copy(previousone)
  previousone = subtract_one(previousone, up_limit=3)  # expects [1, 2] ie [0, 3] minus 1 = [0, 2]
  print('before', before, 'previousone', previousone)
  before = copy.copy(previousone)
  previousone = subtract_one(previousone, up_limit=3)  # expects [0, 2] ie [0, 2] minus 1 = [0, 1]
  print('before', before, 'previousone', previousone)
  before = copy.copy(previousone)
  previousone = subtract_one(previousone, up_limit=3)  # expects [0, 1] ie [0, 2] minus 1 = None
  print('before', before, 'previousone', previousone)
  before = copy.copy(previousone)
  previousone = subtract_one(previousone, up_limit=3)
  print('before', before, 'previousone', previousone)


def adhoctest3():
  up_limit, n_slots, pos = 3, 2, 2
  firstelem = list(range(up_limit+1))
  scrmsg = f'up_limit={up_limit} n_slots={n_slots} firstelem={firstelem}'
  print(scrmsg)
  distance = get_distance_from_the_summation_scheme(n_elements=up_limit+1, pos=pos)
  scrmsg = f'up_limit={up_limit} n_slots={n_slots} at pos={pos} distance={distance}'
  print(scrmsg)
  up_limit, n_slots, pos = 4, 3, 0
  distance = get_distance_from_the_summation_scheme(n_elements=up_limit+1, pos=pos)
  scrmsg = f'up_limit={up_limit} n_slots={n_slots} at pos={pos} distance={distance}'
  print(scrmsg)
  alist = get_decrescent_integer_sequence_summation_of_n(up_limit)
  print(alist, 'sum', sum(alist))
  alist = get_decrescent_integer_sequence_summation_of_n(3)
  print(alist, 'sum', sum(alist))


if __name__ == '__main__':
  adhoctest2()
