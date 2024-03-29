#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/lexicographical_indices.py
  Contains class LgiCombiner and other related classes and functions
"""
import random
import sys
import fs.mathfs.combinatorics.IndicesCombinerForCombinations as iCmb  # for the comb(n, m) function
SUBINDO = 2
DESCENDO = 1
counter = 0  # global


class Lexico:

  def __init__(self):
    self.counter = 0


def check_up_amount_in_array_carried(carried_array, lgi):
  size = len(carried_array); soma = 0
  for i in range(size):
    value = carried_array[i]
    pos_inv = size - i
    soma += iCmb.comb(value, pos_inv)
  if soma != lgi:
    errmsg = 'checkUpAmountInCarriedArray() ==>> soma (=%d) não igual a lgi_b1idx (=%d) %s' %(soma, lgi, str(carried_array))
    raise ValueError(errmsg)


def transform_comb_in_lgi(comb_array, n_of_elems):
  lc = LgiCombiner(n_of_elems - 1, -1, comb_array)
  return lc.get_lgi()


def transform_lgi_in_comb(n_of_elems, size, lgi):
  lc = LgiCombiner(n_of_elems - 1, size)
  return lc.move_to(lgi)


class LgiCombiner(object):
  """
  LGI = LexicoGraphical Index
        From the Combinadics Theory

  Interface:

  first() ==>> sets combination to the first one and returns it
  last() ==>> sets combination to the last one and returns it
  next(jump=1) ==>> moves to the next 'jump' combinations ahead
  previous(jump=1) ==>> moves to the previous 'jump' combinations behind
  move_to(lgi_b1idx=0) ==>> moves to the combination corresponding to the LG Index 'lgi_b1idx'
  lgi_of() ==>> returns the LG Index of the current combination
  set_comb(array=[n-1,n-2,...,2,1,0])  ==>> sets the current combination to the one passed-in
  current_in_ascending_order() ==> gets the current combination in Ascending/Crescent Order

  This class models a combinadics function, ie:

    f(lgi_b1idx,ic(n,m)) = [comb]

  where:
    lgi_b1idx is the LexicoGraphic Index
    ic(n,m) is the IndicesCombinerLgi object, n is number of elements, m is array size

  Eg ==>> f(31029, ic(60,6)) = [19,15,13,11,5,4]
  because
    c(19,6)+c(15,5)+c(13,4)+c(11,3)+c(5,2)+c(4,1) = 31029

  It can also be gotten the other way around, ie:
  fInv([19,15,13,11,5,4]) = 31029

  Operationally, the movesTo() is the first (direct) function,
    the get_lgi() is the second (inverse) function

  Steps for that example:

  obj = IndicesCombinerLgi(59,6)
  obj.movesTo(31029) results in positioning iArray to [19,15,13,11,5,4] and returning it
  obj.get_lgi() after that results in 31029

  To use get_lgi giving an array, it can be done by instantiating the object with the array, ie:
  obj = IndicesCombinerLgi(59,6,[19,15,13,11,5,4])
  Then, obj.get_lgi() will return the lgi_b1idx for that array (ie, 31029)


  This class can also be explained by examples
  ============================================

  Example 1:
  indComb = IndicesCombiner(5, 3)
  indComb.first() results [2, 1, 0]
  indComb.get_first_given() in this case also results [2, 1, 0]
  aplying indComb.next() each time:
  [2, 1, 0]   [3, 1, 0]   [3, 2, 0]   [3, 2, 1]   [4, 2, 1]
  [4, 3, 1]   [4, 3, 2]   [5, 3, 2]   [5, 4, 2]
   ... the last one is [5, 4, 3]
  if a new indComb.next() is applied, None is returned

  The behavior expected is that of a Combination
  Mathematically, the total of produced arrays is:
    Combination(5,3) = 5! / ((5-3)!3!)

  (*) get_first_given() explanation
  when iArrayIn is passed with a consistent array
  get_first_given() returns that array

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
    File "./comb.py", line 237, in <module>
      test_indices_combiner(upLimit, size)
    File "./comb.py", line 189, in test_indices_combiner
      indComb = IndicesCombiner(upLimit, size, False); c=0
    File "./comb.py", line 80, in __init__
      raise ValueError, msg
  ValueError: Inconsistent IndicesCombiner upLimit(=1) must be at least size(=4) - 1 when overlap=False
  """

  def __init__(self, up_limit=0, size=1, i_array_in=None):
    if size < 1:
      size = 1
    if up_limit < 0:
      up_limit = 0
    self.up_limit = up_limit
    # yet to be checked True
    self.still_first = False
    i_array_in = [0] if i_array_in is None else i_array_in
    if i_array_in == [0] and size > 1:
      self.i_array = range(size - 1, -1, -1)
      self.still_first = True
    else:
      self.i_array = list(i_array_in)
      if self.i_array == range(size - 1, -1, -1):
        self.still_first = True
    self.size = len(self.i_array)
    self.check_array_consistency()
    self.n_of_combines = iCmb.IndicesCombinerForCombinations(self.up_limit + 1, self.size)
    self.i_array_given = list(self.i_array)

  def check_array_consistency(self):
    """
    Checks the consistency of iArray
    Examples of inconsistent arrays:
      valid ==>> [2,1,0], [100,1,0]
      invalid ==>> [0,0,0], [3,2,2]
    """
    for i in range(self.size-1):
      if self.i_array[i] <= self.i_array[i + 1]:
        errmsg = 'Inconsistent array: next elem can not be greater or equal to a previous one %s' %(str(self.i_array))
        raise ValueError(errmsg)

  def output_i_array(self, sort_it, is_zeroless):
    i_array = list(self.i_array)  # hard-copy it
    if sort_it:
      i_array.sort()
    if is_zeroless:
      i_array = map(lambda e: e+1, i_array)
    return i_array

  def current(self, sort_it=True, is_zeroless=True):
    """
    Returns the current iArray
    Notice that iArray is modified by methods like next() and first()
    """
    return self.output_i_array(sort_it, is_zeroless)

  def get_lgi(self):
    lgi = 0
    for i in range(self.size):
      value = self.i_array[i]
      pos_inv = self.size - i
      lgi += iCmb.comb(value, pos_inv)
    return lgi

  def first(self, sort_it=True, is_zeroless=True):
    """
    Moves the iArray to the top and returns it
    Eg
    overlap=True,  size=3 :: [0,0,0]
    overlap=False, size=4 :: [0,1,2,3]
    """
    self.i_array = range(self.size - 1, -1, -1)
    return self.output_i_array(sort_it, is_zeroless)

  def first_given(self):
    """
    Returns the get_first_given or restartAt array but does not change current position
    To change it, use position_to_first_given()
    """
    return list(self.i_array_given) # output a hard-copy of it so that it (the reference) is not changed outside

  def position_to_first_given(self):
    """
    Returns the get_first_given/restartAt array changing current position to it
    @see also get_first_given()
    """
    self.i_array = list(self.i_array_given)

  def last(self, sort_it=True, is_zeroless=True):
    """
    Moves iArray position to the last one and returns it
    Eg
    size=4, upLimit=33 :: [33,32,31,30]
    """
    for i in range(self.size):
      self.i_array[i] = self.up_limit - i
    return self.output_i_array(sort_it, is_zeroless)

  def move_to(self, lgi=0, sort_it=True, is_zeroless=True):
    if lgi <= 0:
      if lgi == 0:
        return self.first()
      return None
    max_index = self.n_of_combines - 1
    # print 'max_index', max_index
    if lgi >= max_index:
      if lgi == max_index:
        return self.last()
      return None
    # initializing array_carried
    array_carried = [-1] * self.size
    for pos in range(self.size):
      array_carried[pos] = self.size - pos - 1
    # if it got here, there are at least 3 elements, hence there's a midpoint
    point_inf = self.size - 1 - 0
    point_sup = self.up_limit
    pos = 0
    self.i_array = self.approach(lgi, point_inf, point_sup, pos, array_carried)
    return self.output_i_array(sort_it, is_zeroless)

  def approach(self, lgi, point_inf, point_sup, pos, array_carried, amount=0):
    """
    global counter
    """
    if pos == self.size:
      errmsg = ("""  Well, failed to get the LG Index. 
      Reason: pos surpasses all available slots. (pos=%d, size=%d, pointInf=%d, pointSup=%d)
      """ % (pos, self.size, point_inf, point_sup))
      print(errmsg)
      sys.exit(0)
      # raise ValueError(errmsg)
    point_mid = point_inf + (point_sup - point_inf) / 2
    pos_inv = self.size - pos
    parcel = iCmb.comb(point_mid, pos_inv)
    amount_compare = amount + parcel
    parcel_sup = iCmb.comb(point_sup, pos_inv)
    amount_compare_sup = amount + parcel_sup
    parcel_inf = iCmb.comb(point_inf, pos_inv)
    amount_compare_inf = amount + parcel_inf
    # msg = 'i=%d inf=%d/%d mid=%d/%d sup=%d/%d pos=%d %s press [ENTER]' %(lgi_b1idx, pointInf, amount_compare_inf, point_mid, amount_compare, pointSup, amount_compare_sup, pos, str(arrayCarried))
    # ans=raw_input(msg)
    # counter+=1 # global
    # print counter, msg
    if amount_compare_sup < lgi:
      amount += parcel_sup
      array_carried[pos] = point_sup
      pos += 1
      # renew pointInf and pointSup
      point_inf = self.size - 1 - pos
      point_sup = point_sup - 1 # limiteSup
      return self.approach(lgi, point_inf, point_sup, pos, array_carried, amount)
    if amount_compare_sup == lgi: # ok, game over
      array_carried[pos] = point_sup
      # check for consistency
      check_up_amount_in_array_carried(array_carried, lgi)
      return array_carried
    if amount_compare > lgi:
      # the following check avoids an infinite recursion and logically complements the desired functionality
      if point_mid >= point_sup-1 and parcel_inf < lgi:
        amount += parcel_inf
        array_carried[pos] = point_inf
        pos += 1
        # renew pointInf and pointSup
        point_sup = point_inf - 1 # limiteSup
        point_inf = self.size - 1 - pos
        return self.approach(lgi, point_inf, point_sup, pos, array_carried, amount)
      point_sup = point_mid
      return self.approach(lgi, point_inf, point_sup, pos, array_carried, amount)
    elif amount_compare < lgi:
      if point_mid >= point_sup - 1:
        if amount_compare_sup < lgi:
          amount += parcel_sup
          array_carried[pos] = point_sup
          point_sup = point_sup - 1 # limiteSup
        else:
          amount += parcel
          array_carried[pos] = point_mid
          point_sup = point_mid - 1 # limiteSup
        pos += 1
        # renew pointInf and pointSup
        point_inf = self.size - 1 - pos
        return self.approach(lgi, point_inf, point_sup, pos, array_carried, amount)
      point_inf = point_mid
      # pointSup is the same
      return self.approach(lgi, point_inf, point_sup, pos, array_carried, amount)
    else:  # ie, amount_compare == lgi_b1idx ie, element has just been FOUND!
      array_carried[pos] = point_mid
      # check for consistency
      check_up_amount_in_array_carried(array_carried, lgi)
      return array_carried

  def previous2(self):
    """
    Moves iArray to its previous consistent position and returns the array
    When the first one is current, None will be returned
    """
    pos = self.size - 1
    if self.overlap:
      return self.minus_one_overlap(pos)
    else:
      return self.minus_one_nonoverlap(pos)

  def ajust_to_the_right(self, pos):
    for i in range(pos, self.size-1):
      self.i_array[i + 1] = self.i_array[i] - 1
    self.check_array_consistency()

  def subtract_one(self, pos=-1):
    if pos == -1:
      pos = self.size - 1
    least_allowed = self.size - pos - 1
    if pos == 0:
      if self.i_array[0] == least_allowed:
        return None
      self.i_array[0] -= 1
      self.ajust_to_the_right(0)
      return 1  # self.iArray
    if self.i_array[pos] == least_allowed:
      return self.subtract_one(pos - 1)
    self.i_array[pos] -= 1
    self.ajust_to_the_right(pos)
    return 1  # self.iArray

  def add_one(self, pos=-1):
    """
    This method can not be called from outside of the class
    More than that, only next() can call it, otherwise, inconsistencies may arise
    ie, the method should also have its first go with pos=-1
    """
    if pos == 0:
      if self.i_array[0] == self.up_limit:
        # print 'self.iArray', self.iArray
        self.ajust_to_the_right(0)
        return None
      self.i_array[0] += 1
      return 1  # self.iArray
    if pos == -1:
      pos = self.size - 1
    if self.i_array[pos]+1 == self.i_array[pos - 1]:
      least_allowed = self.size - pos - 1
      self.i_array[pos] = least_allowed
      return self.add_one(pos - 1)
    self.i_array[pos] += 1
    return 1  # self.iArray

  def next(self, quant=1, sort_it=True, is_zeroless=True):
    """
    Moves iArray position to the next consistent one and returns it
    When the last one is current, None will be returned
    """
    if self.still_first:
      if quant == 1:
        # control flow is supposed to pass in here only once
        self.still_first = False
        return self.first(sort_it, is_zeroless)
      elif quant > 1:
        quant -= 1
      # if quant > 1 or quant <> 1, next line will be executed
      self.still_first = False
    ret_val = None
    for i in range(quant):
      ret_val = self.add_one()
    # notice that self.iArray is never None, but (local) iArray can be None
    if not ret_val:
      return None
    return self.output_i_array(sort_it, is_zeroless)

  def __getitem__(self, item_index):
    """
    itemIndex may either be an int or a slice
    logic should be implemented
    if type(itemIndex) == type(int):
      ok, do one
    if type(itemIndex) == type(int):
      think how to solve this, the slice has 3 params (x,y,z)
      like the range() params

    print 'itemIndex', itemIndex, type(itemIndex)
    if type(itemIndex) == slice:
      print repr(slice)
    """
    return self.next()  # all defaults = 1, True, True

  def previous(self, quant=1, sort_it=True, is_zeroless=True):
    """
    Moves iArray position to the previous consistent one and returns it
    When the first one is current, None will be returned
    """
    ret_val = None
    for i in range(quant):
      ret_val = self.subtract_one()
    if not ret_val:
      return None
    return self.output_i_array(sort_it, is_zeroless)

  def __str__(self):
    """
    The string representation of the class
    """
    out_str = 'array=%s upLimit=%d' %(str(self.i_array), self.up_limit)
    return out_str


def adhoctest():
  lgi = LgiCombiner(up_limit=6, size=6)
  print('n_of_combines', lgi.n_of_combines)
  print('lgi_b1idx', lgi)


def process():
  pass


if __name__ == '__main__':
  """
  """
  adhoctest()
