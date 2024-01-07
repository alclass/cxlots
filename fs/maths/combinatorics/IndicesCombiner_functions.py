#!/usr/bin/env python
"""
fs/maths/combinatorics/IndicesCombiner_functions.py

"""
import copy


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
    next([0, 1]) = [0, 2]  # last one [0, 1]
    next([0, 2]) = [0, 3]
    next([0, 3]) = [1, 2]
    and so on up to
    next([1, 2]) = [2, 3]  # last one [2, 3]
    next([2, 3]) = None  # adding one to the last one results None
    next(None) = None  # adding one to None also results None
  """
  if numberlist is None:
    return None
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


if __name__ == '__main__':
  adhoctest()
