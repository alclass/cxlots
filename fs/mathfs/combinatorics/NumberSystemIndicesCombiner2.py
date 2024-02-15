#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/NumberSystemIndicesCombiner2.py
 former fs/mathfs/combinatorics/IndicesCombinerForCombinations.py
  Contains the class IndicesCombiner that models a combinadic object as a Number System base-n
  (@see ref @wikipedia below)

Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
import sys
"""


def from_decimal_to_numbersystem_base_n(decint, base=6, acclist=None):
  """
  Transform a possitive int number into an array representation with digits forming a number in base "b"
  This is a recursive function
  """
  acclist = [] if acclist is None else acclist
  newdecint = decint // base
  remainder = decint % base
  acclist.append(remainder)
  if newdecint == 0:
    invlist = reversed(acclist)
    acclist = list(invlist)
    return acclist
  return from_decimal_to_numbersystem_base_n(newdecint, base, acclist)


def from_numbersystem_base_n_to_decimal(acclist, base=6):
  """
  Transform an array representation with digits, in base "b", into a possitive int number
  This function is not recursive as its inverse above
  """
  invlist = reversed(acclist)
  i, soma = 0, 0
  for d in invlist:
    parcel = d * base ** i
    soma += parcel
  return soma


def get_number_from_array_repr_number_system_baselessthan11(array):
  """
  Transforms a number system represented in an array into an int
    converting it into a str, then into an int

  Obs: numbers individually in array should not be greater than 9 or else a ValueError will be raised
  This function is "agnostic" of the base into which the number is base,
    because its main "client" is interested in comparing lexicographical order
      (ie, if one number is less or greater than another)

  """
  if array is None:
    return None
  bool_res = [e > 9 for e in array]
  if True in bool_res:
    errmsg = f"array {array} has at least one number greater than 9"
    raise ValueError(errmsg)
  as_str = ''.join(map(str, array))
  as_int = int(as_str)
  return as_int


def is_array1_less_or_equal_array2(array1, array2):
  """
  Because arrays represent number systems, comparison may be done by the array's number representation,
    and it can be done even if array sizes differ
  """
  n1 = get_number_from_array_repr_number_system_baselessthan11(array1)
  n2 = get_number_from_array_repr_number_system_baselessthan11(array2)
  return n1 <= n2


def is_array1_greater_or_equal_array2(array1, array2):
  """
  Because arrays represent number systems, comparison may be done by the array's number representation,
    and it can be done even if array sizes differ
  """
  n1 = get_number_from_array_repr_number_system_baselessthan11(array1)
  n2 = get_number_from_array_repr_number_system_baselessthan11(array2)
  return n1 >= n2


def is_array1_less_than_array2(array1, array2):
  """
  Because arrays represent number systems, comparison may be done by the array's number representation,
    and it can be done even if array sizes differ
  """
  n1 = get_number_from_array_repr_number_system_baselessthan11(array1)
  n2 = get_number_from_array_repr_number_system_baselessthan11(array2)
  return n1 < n2


def is_array1_greater_than_array2(array1, array2):
  """
  Because arrays represent number systems, comparison may be done by the array's number representation,
    and it can be done even if array sizes differ
  """
  n1 = get_number_from_array_repr_number_system_baselessthan11(array1)
  n2 = get_number_from_array_repr_number_system_baselessthan11(array2)
  return n1 > n2


class NumberSystemIndicesCombiner:

  def __init__(self, n_elements, n_slots):
    self.n_elements, self.n_slots = n_elements, n_slots
    self._size = None
    self.b0idx = None
    self.curr_comb = None
    self.set_first_element()

  def set_first_element(self):
    self.b0idx = 0
    self.curr_comb = list(self.first_elem)
    return True

  def set_last_element(self):
    self.b0idx = self.size - 1
    self.curr_comb = list(self.last_elem)
    return True

  def set_element_at_b0idx(self, b0idx):
    if b0idx is None:
      return self.set_last_element()
    if b0idx == 0:
      return self.set_first_element()
    if b0idx == self.size - 1:
      return self.set_last_element()
    if 1 <= b0idx <= self.size - 2:
      self.b0idx = b0idx
      arr = from_decimal_to_numbersystem_base_n(decint=self.b0idx, base=self.n_elements)
      self.curr_comb = list(arr)
      return True
    return False

  @property
  def size(self):
    """
    Counting is as follows:
      from 0 (as b0_idx) to base**exponent-1 (ie altogether size=base**exponent)
    Example for NSIC(ne_= 2, ns=2), the sets are:
      0 comb [0, 0]
      1 comb [0, 1]
      2 comb [1, 0]
      3 comb [1, 1]
    """
    if self._size is None:
      base = self.n_elements
      exponent = self.n_slots
      self._size = base ** exponent
    return self._size

  @property
  def first_elem(self):
    return [0]*self.n_slots

  @property
  def before_first(self):
    return [-1]*self.n_slots

  @property
  def last_elem(self):
    return [self.n_elements-1]*self.n_slots

  def next(self):
    if self.curr_comb == self.last_elem:
      return None
    arr = from_decimal_to_numbersystem_base_n(decint=self.b0idx + 1, base=self.n_elements)
    while len(arr) < self.n_slots:
      arr.insert(0, 0)
    if is_array1_greater_than_array2(arr, self.last_elem):
      return None
    self.b0idx += 1
    self.curr_comb = list(arr)
    return self.curr_comb

  def previous(self):
    if self.curr_comb == self.first_elem:
      return [-1]*self.n_slots
    arr = from_decimal_to_numbersystem_base_n(decint=self.b0idx - 1, base=self.n_elements)
    if is_array1_less_than_array2(arr, self.first_elem):
      return [-1]*self.n_slots
    while len(arr) < self.n_slots:
      arr.insert(0, 0)
    self.b0idx -= 1
    self.curr_comb = list(arr)
    return self.curr_comb

  def gen_desc_combs_w_intrange_from_downto(self, from_b0idx=None, downto_b0idx=0):
    from_b0idx = self.size-1 if from_b0idx is None or from_b0idx > self.size else from_b0idx
    boolres = self.set_element_at_b0idx(from_b0idx)
    if not boolres:
      return
    while self.b0idx >= downto_b0idx:
      yield self.curr_comb
      if self.previous() == self.before_first:
        break
    return

  def gen_asc_combs_w_intrange_from_to(self, from_b0idx=0, to_b0idx=None):
    boolres = self.set_element_at_b0idx(from_b0idx)
    if not boolres:
      return
    to_b0idx = self.size if to_b0idx is None or to_b0idx > self.size else to_b0idx
    while self.b0idx <= to_b0idx:
      yield self.curr_comb
      if self.next() is None:
        break
    return

  def __str__(self):
    outstr = (f"n_elements={self.n_elements}, n_slots={self.n_slots} cmb={self.curr_comb}"
              f" idx={self.b0idx} size={self.size}")
    return outstr


def adhoc_test():
  """
  decint, base = 33, 2
  acclist = from_decimal_to_numbersystem_base_n(decint=decint, base=base)
  print(decint, base, acclist)
  ret_decint = from_numbersystem_base_n_to_decimal(acclist)
  print('retint', acclist, 'ret_decint', ret_decint)

  """
  n_elements, n_slots = 4, 2
  ic = NumberSystemIndicesCombiner(n_elements=n_elements, n_slots=n_slots)
  # for _ in ic.gen_asc_combs_w_intrange_from_to():
  for _ in ic.gen_desc_combs_w_intrange_from_downto():
    print(ic.b0idx, 'comb', ic.curr_comb)
  print('ic', ic)


def adhoc_test2():
  arr = from_decimal_to_numbersystem_base_n(2, 3)
  print(arr)
  arr = from_decimal_to_numbersystem_base_n(2+1, 3)
  print(arr)


if __name__ == '__main__':
  """
  adhoc_test2()
  """
  adhoc_test2()
  adhoc_test()
