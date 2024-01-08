#!/usr/bin/env python
"""
fs/maths/combinatorics/IndicesCombiner.py
  Contains the class IndicesCombiner that models a combinadic object (@see ref @wikipedia below)

Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
"""
import copy
import sys
import fs.maths.combinatorics.combinatoric_algorithms as ca  # ca.fact(n)
import fs.maths.combinatorics.IndicesCombiner_functions as icf  # icf.project_last_combinationlist


class IndicesCombiner(object):
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

  def __init__(self, n_elements=0, n_slots=1, overlap=True, i_array_in=None):
    i_array_in = [0] if i_array_in is None else i_array_in
    self.parked_at_first_element = None
    self.i_array_given = None
    if n_slots < 1:
      n_slots = 1
    if n_elements < 0:
      n_elements = 0
    self.n_elements = n_elements
    if overlap not in [True, False]:
      overlap = True
    if not overlap:
      if n_elements + 2 < n_slots:
        errmsg = 'Inconsistent IndicesCombiner upLimit(=%d) must be at least size(=%d) - 1 when overlap=False ' %(up_limit, n_slots)
        raise ValueError(errmsg)
    self.overlap = overlap
    if i_array_in == [0] and n_slots > 1:
      if overlap:
        self.i_array = [0] * n_slots
      else:
        self.i_array = list(range(n_slots))
    else:
      self.i_array = list(i_array_in)
    self.n_slots = len(self.i_array)
    self.check_array_consistency()
    self.determined_from_constructor_whether_position_is_before_first()

  @property
  def up_limit(self):
    return self.n_elements - 1

  def determined_from_constructor_whether_position_is_before_first(self):
    self.i_array_given = list(self.i_array)
    if self.i_array_given == self.make_first():
      self.park_before_first()

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
        if self.i_array[i + 1] < self.i_array[i]:
          raise_exception = True
      else:
        if self.i_array[i + 1] <= self.i_array[i]:
          raise_exception = True
      if raise_exception:
        if self.overlap:
          context = 'lesser'
        else:
          context = 'lesser or equal'
        errmsg = 'Inconsistent array: next elem can be %s than a previous one %s' %(context, str(self.i_array))
        raise ValueError(errmsg)

  def make_before_first(self):
    """
    No matter overlap kind, the "before first" is an array of minus one
    Example:
      if size=3, before_first is:
        [-1, -1, -1]
    """
    before_first_i_array = [-1] * self.n_slots
    return before_first_i_array

  def restart_positioning_before_first(self):
    self.i_array = self.make_before_first()

  def make_first(self):
    if self.overlap:
      first_i_array = [0] * self.n_slots
    else:
      first_i_array = list(range(self.n_slots))
    return first_i_array
  
  @property
  def total_comb(self):
    """
    Uses the formula:
    comb_of_n_m_by_m = n! / ((n - m)! * m!)
    """
    n = self.n_elements
    m = self.n_slots
    num = ca.fact(n)
    den = ca.fact(n - m) * ca.fact(m)
    total_combinations = num / den
    # total_combinations should be a countable integer
    return int(total_combinations)

  @property
  def first(self):
    """
    Moves the iArray to the top and returns it
    Eg
    overlap=True,  size=3 :: [0,0,0]
    overlap=False, size=4 :: [0,1,2,3]
    """
    self.i_array = self.make_first()
    return copy.copy(self.i_array)

  @property
  def top(self):
    """
    The same as self. first
    """
    return self.first

  @property
  def bottom(self):
    """
    The same as self. last
    """
    return self.last

  @property
  def first_zeroless(self):
    first_all_elements_plus_one = list(map(lambda e: e + 1, self.first))
    return first_all_elements_plus_one
    
  def get_first_given(self):
    """
    Returns the get_first_given or restartAt array but does not change current position
    To change it, use reposition_to_first_given()
    """
    return copy.copy(self.i_array_given)

  def reposition_to_first_given(self):
    """
    Returns the get_first_given/restartAt array changing current position to it
    @see also get_first_given()
    """
    self.i_array = list(self.i_array_given)

  def park_before_first(self):
    """
    Move to first element and set flag self.parked_at_first_element to True 
    """
    self.i_array = [-1] * self.n_slots

  @property
  def last(self):
    """
    @see self.move_to_last_one()
    """
    last_i_array = [0]*self.n_slots
    if self.overlap:
      last_i_array = [self.up_limit] * self.n_slots
      return last_i_array
    else:
      for i in list(range(self.n_slots)):
        back_pos = self.n_slots - i - 1
        last_i_array[i] = self.up_limit - back_pos
      return last_i_array

  def tell_first_i_array(self):
    first_i_array = [0]*self.n_slots
    if self.overlap:
      # first_i_array = [0] * self.size
      return first_i_array
    else:
      first_i_array = len(range(self.n_slots))
      return first_i_array

  def move_to_one_before_last(self):
    self.move_to_last_one()
    self.previous()
  
  def move_to_position_by_i_array(self, i_array_in):
    if i_array_in is None or len(i_array_in) != self.n_slots:
      errmsg = f"i_array_in is None or it's been given having an incorrect size {self.n_slots} | {str(i_array_in)}"
      raise ValueError(errmsg)
    if i_array_in != list(map(int, i_array_in)):
      errmsg = 'parameter iArray_in was passed in containing non-integers'
      raise ValueError(errmsg)
    self.parked_at_first_element = False
    last_i_array = self.last()
    # if it's greater than last, move it to last
    if True in map(lambda e: e > last_i_array, i_array_in):
      self.move_to_last_one()
      return
    first_i_array = self.tell_first_i_array()
    # if it's less than first, move it to first
    if True in map(lambda e: e > first_i_array, i_array_in):
      self.first()
      return
    self.i_array = i_array_in
  
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
    if self.i_array[pos] > self.up_limit:
      errmsg = 'Index in Combiner exceeds upLimit(=%d). There is probably a bug. self.iArray[%d]=%d :: ' %(self.up_limit, pos, self.i_array[pos])
      errmsg += str(self)
      raise ValueError(errmsg)
    self.i_array[pos + 1] = self.i_array[pos]
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
    if self.i_array[pos] > self.up_limit - back_pos:
      errmsg = 'Index in Combiner exceeds upLimit(=%d). There is probably a bug. self.iArray[%d]=%d :: ' %(self.up_limit, pos, self.i_array[pos])
      errmsg += str(self)
      raise ValueError(errmsg)
    self.i_array[pos+1] = self.i_array[pos] + 1
    return self.correct_remaining_to_the_right_non_overlap_case(pos + 1)

  def shift_left(self, pos=-1): # , nOfPos=-1
    '''
    Left-shifts the iArray
    Eg
    overlap=True,  size=3, upLimit=15
    [1,1,1].shift_left(1) ==>> [2,2,2]
    overlap=False, size=4, upLimit=33
    [1,2,3,4].shift_left(2) ==>> [1,3,4,5]
    '''
    if pos == -1:
      pos = self.n_slots - 1
    if pos == 0:
      # well, it's the last one, a left-shift can't happen,
      # so it goes to the last one
      self.move_to_last_one() #iArrayToDiscard = self.move_to_last_one()
      return None
    if self.overlap:
      if self.i_array[pos - 1] == self.up_limit:
        return self.shift_left(pos - 1)
      self.i_array[pos - 1] += 1
      self.correct_remaining_to_the_right_overlap_case(pos - 1)
      return self.i_array
    else:
      pos_ant = pos - 1
      back_pos_ant = self.n_slots - pos_ant - 1
      if self.i_array[pos_ant] == self.up_limit - back_pos_ant:
        return self.shift_left(pos - 1)
      self.i_array[pos - 1] += 1
      self.correct_remaining_to_the_right_non_overlap_case(pos - 1)
      return self.i_array

  def vai_um_in_place_overlap_case(self, pos):
    """
    Case of "goes one" when overlap=True
    """
    if pos == 0 and self.i_array[pos] == self.up_limit:
      self.move_to_last_one() # iArrayToDiscard = self.move_to_last_one()
      return None
    if self.i_array[pos] == self.up_limit:
      return self.vai_um_in_place_overlap_case(pos - 1)
    self.i_array[pos] += 1
    self.correct_remaining_to_the_right_overlap_case(pos)
    return self.i_array

  def vai_um_in_place_non_overlap_case(self, pos):
    """
    Case of vaiUm when overlap=False
    """
    back_pos = self.n_slots - pos - 1
    if pos == 0 and self.i_array[pos] == self.up_limit - back_pos:
      self.move_to_last_one()  # iArrayToDiscard = self.move_to_last_one()
      return None
    if self.i_array[pos] == self.up_limit - back_pos:
      return self.vai_um_in_place_non_overlap_case(pos - 1)
    self.i_array[pos] += 1
    self.correct_remaining_to_the_right_non_overlap_case(pos)
    return self.i_array

  def vai_um_in_place(self, pos):
    """
    Adds one in the i-th (pos) element
    Example:
      overlap=True,  size=3, upLimit=15
      [1,1,1].shift_left(1) ==>> [1,2,2]
      overlap=False, size=4, upLimit=33
      [1,2,3,4].shift_left(2) ==>> [1,2,4,5]
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
      if self.i_array[0] > 0:
        self.i_array[0] -= 1
        return self.i_array
      else: # if self.iArray[pos] == 0:
        self.first()
        return None
    if self.i_array[pos - 1] == self.i_array[pos]:
      self.i_array[pos] = self.up_limit
      return self.minus_one_overlap(pos - 1)
    else:
      self.i_array[pos] -= 1
      return self.i_array

  def minus_one_non_overlap(self, pos):
    """
    Inner implementation of previous() for the overlap=False case
    see @previous()
    """
    if pos == 0:
      if self.i_array[pos] > 0:
        self.i_array[pos] -= 1
        return self.i_array
    if self.i_array[pos] == pos:
      self.first()
      return None
    if self.i_array[pos - 1]+1 == self.i_array[pos]:
      debit_to_up_limit = self.n_slots - pos - 1
      self.i_array[pos] = self.up_limit - debit_to_up_limit
      return self.minus_one_non_overlap(pos - 1)
    else:
      self.i_array[pos] -= 1
    return self.i_array

  def previous(self):
    """
    Moves iArray to its previous consistent position and returns the array
    When the first one is current, None will be returned
    """
    if self.i_array == self.make_before_first():
      return self.i_array
    if self.i_array == self.make_first():
      self.i_array = self.make_before_first()
      return self.i_array
    if self.i_array is None:
      return self.move_to_last_one()
    pos = self.n_slots - 1
    if self.overlap:
      return copy.copy(self.minus_one_overlap(pos))
    else:
      return copy.copy(self.minus_one_non_overlap(pos))

  def next(self, pos=-1):
    """
    Moves iArray position to the next consistent one and returns it
    When the last one is current, a None will be returned
    """
    if not self.overlap:
      self.i_array = icf.add_one(self.i_array, up_limit=self.up_limit)
      return self.i_array
    # check before first element
    if self.i_array is not None and self.i_array == [-1] * self.n_slots:
      # switch it off independently of next if's result
      self.i_array = self.make_first()
      return copy.copy(self.i_array)
    if pos == -1:
      pos = self.n_slots - 1
      # if self.iArray[pos]+1 > self.up_limit:
    if self.overlap:
      up_limit = self.up_limit
    else:
      up_limit = self.up_limit - (self.n_slots - pos - 1)

    if self.i_array and self.i_array[pos]+1 > up_limit:
      def recurse_indices_with_overlap(p_pos):
        """
        This is an inner recursive help method
        For the case when overlap=True
        """
        if p_pos == 0 and self.i_array[p_pos]+1 > self.up_limit:
          return None
        if self.i_array[p_pos]+1 > self.up_limit:
          if self.i_array[p_pos - 1]+1 > self.up_limit:
            # self.iArray[pos]=self.iArray[pos-1]
            return recurse_indices_with_overlap(p_pos - 1)
          self.i_array[p_pos - 1] += 1
          self.i_array[p_pos] = self.i_array[p_pos - 1]
          return self.i_array[p_pos - 1]
        return self.i_array[p_pos]+1

      def recurse_indices_without_overlap(p_pos):
        """
        This is an inner recursive help method
        For the case when overlap=False
        """
        if p_pos is None:
          return None
        if p_pos == 0 and self.i_array[p_pos]+1 > self.up_limit - (self.n_slots - p_pos - 1):
          return None
        if self.i_array[p_pos]+1 > self.up_limit - (self.n_slots - p_pos - 1):
          tmp = recurse_indices_without_overlap(p_pos - 1)
          if tmp is None:
            return None
          self.i_array[p_pos] = tmp + 1
          return self.i_array[p_pos]
        self.i_array[p_pos] += 1
        return self.i_array[p_pos]

      if self.overlap:
        value = recurse_indices_with_overlap(pos)
      else:
        value = recurse_indices_without_overlap(pos)
      if value is None:
        return None
      self.i_array[pos] = value
    else:
      self.i_array[pos] += 1
    return copy.copy(self.i_array)

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
    if self.up_limit == 1 and self.n_slots == 2:
      # the case in which whole combination set is [[0,1]]
      return None
    bool_array = list(map(lambda e: e == 0, self.i_array))
    if True in bool_array:
      zeroless = list(range(self.n_slots))
      # position i_array to it
      self.i_array = copy.copy(zeroless)
      return zeroless
    return self.i_array

  def get_first_elements(self, upto=10):
    if upto > self.total_comb:
      upto = self.total_comb
    other = copy.copy(self)
    i_array = other.move_to_first()
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

  
def adhoctest_indicescombiner(up_limit, size):
  # signature IndsControl(upLimit=1, size=-1, overlap=True, iArrayIn=[])
  ind_comb = IndicesCombiner(up_limit, size, True); c=0
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, True)' % (up_limit, size)
  print(scrmsg)
  s = ind_comb.get_first_given()
  set_with_ol = []
  while s:
    c+=1
    print(c, s)
    set_with_ol.append(list(s))
    s = ind_comb.next()
  set_without_ol = []
  ind_comb = IndicesCombiner(up_limit, size, False); c=0
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, False)' % (up_limit, size)
  print(scrmsg)
  s = ind_comb.get_first_given()
  while s:
    c += 1
    print(c, s)
    set_without_ol.append(list(s))
    s = ind_comb.next()
  c=0
  not_there = 0
  for wol in set_with_ol:
    c+=1
    print(c, wol)
    if wol in set_without_ol:
      print(wol)
    else:
      not_there += 1
      print(not_there)

def pick_up_params():
  params = []
  up_limit = 5
  size = 3
  for i in range(1, len(sys.argv)):
    params.append(sys.argv[i].lower())
  print('params', params)
  if '-uplimit' in params:
    index = params.index('-uplimit')
    print('index -uplimit', index)
    if index + 1 < len(params):
      try:
        up_limit = int(params[index + 1])
      except ValueError:
        pass
  if '-size' in params:
    index = params.index('-size')
    if index + 1 < len(params):
      try:
        size = int(params[index + 1])
      except ValueError:
        pass
  return up_limit, size

def adhoctest_shiftleft(up_limit, size):
  ind_comb = IndicesCombiner(up_limit, size, True, [2, 4, 5]); c=0
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, %s)' % (up_limit, size, ind_comb.overlap)
  print(scrmsg)
  print(ind_comb)
  print('adhoctest_shift_left()', ind_comb.shift_left())
  for i in range(7):
    next_i = ind_comb.next()
  print('next_i 7', next_i)
  print('adhoctest_shift_left()', ind_comb.shift_left())
  ind_comb = IndicesCombiner(7, -1, True, [0,6,6,7,7])
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, %s)' % (up_limit, size, ind_comb.overlap)
  print(scrmsg)
  print(ind_comb)
  pos = 1
  vai_um = ind_comb.vai_um_in_place(pos)
  scrmsg = f'test pos={pos} vai_um={vai_um}'
  print(scrmsg)
  pos = 2
  shifleft = ind_comb.shift_left(pos)
  scrmsg = f'adhoctest pos={pos} shift_left {shifleft}'
  print(scrmsg)
  pos = 1
  vai_um = ind_comb.vai_um_in_place(pos)
  scrmsg = f'adhoctest pos={pos} shift_left {shifleft}'
  print(scrmsg)
  vai_um = ind_comb.vai_um_in_place(pos)
  scrmsg = f'adhoctest pos={pos} shift_left {shifleft}'
  print(scrmsg)
  vai_um = ind_comb.vai_um_in_place(pos)
  scrmsg = f'adhoctest pos={pos} shift_left {shifleft}'
  print(scrmsg)
  print('current', ind_comb.current())
  print('next_i', ind_comb.next())
  

def adhoctest_previous(up_limit, size):
  ic = IndicesCombiner(up_limit, size, True, [0, 2, 12])
  print('ic', ic)
  print('ic.next()', ic.next())
  print('ic', ic)
  print('ic.previous()', ic.previous())
  for i in range(36):
    print('ic.previous()', ic.previous())


def adhoc_test():
  """
  sc = SetsCombiner()
  worksetWithQuantity = ([1,2,3], 2)
  sc.addSetWithQuantities(worksetWithQuantity)
  worksetWithQuantity = ([4,5,6], 2)
  sc.addSetWithQuantities(worksetWithQuantity)
  for ws in sc.getAllSetsCombinationNonRecursively():
    print 'ws', ws
  """
  ic = IndicesCombiner(4, 2, False); c=0
  for ws in ic.gen_all_sets():
    c += 1
    print(c, ws)


def ynext():
  for i in range(10):
    yield i


def test_yield():
  for i in ynext():
    print(i)


def adhoc_test2():
  test_yield()


if __name__ == '__main__':
  pass
