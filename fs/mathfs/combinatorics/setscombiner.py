#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/setscombiner.py
  Contains class SetsCombiner

This module is a bit old and needs refactoring.
Together with the refactoring, an attempt should be made to recover the idea behind the class in this module.
"""
from IndicesCombinerForCombinations import IndicesCombinerForCombinations
import combinatoric_algorithms as afc


class WorkSet(object):
  """
  The purpose of this class is to generate all combinations n by c of an n-element "workSet" combined c by c, where 0 < c <= n
  
  Each combination is "yielded" from each call to method next(). After the last combination, None is returned.
  
  The combination is done, under the hoods, by the IndicesCombiner attribute.  This happens in the line:
    combined_set = [self.workSet[i] for i in indices]
    
  Eg.

  The code fragment
  
  s = ['a','b','c']; combsize = 2
  ws = WorkSet(s, IndicesCombiner( len(s)-1, combsize, False))
  comb = ws.next()
  while comb:
    print comb
    comb = ws.next()
  
  Results in
    ['a', 'b']
    ['a', 'c']
    ['b', 'c']

  The IndicesCombiner generated the indices for s's subsets: 0,1; 0,2; and 1,2 
  """

  def __init__(self, work_set, indices_combiner):
    self.work_set = work_set
    self.total_combinations = None
    self.indices_combiner = indices_combiner
    self.do_restart = False
    self.total_combinations = None
    self.restart()

  def restart(self):
    self.do_restart = True
    
  def get_total_combinations(self):
    """
    total_combinations is a combination n by c, the same that is known by n!((n-c)!c!)
    where n is workSet's size and c is IndicesCombiner's quantity 
    """
    if self.total_combinations is not None:
      return self.total_combinations
    n = len(self.work_set)
    c = self.indices_combiner.n_slots
    self.total_combinations = afc.combine_n_c_by_c_nonfact(n, c)
    return self.total_combinations

  def next(self):
    """
    next_combination
    """
    if self.do_restart:
      indices = self.indices_combiner.first()
      self.do_restart = False
    else:
      indices = self.indices_combiner.next()
    if indices is None:
      return None
    combined_set = [self.work_set[i] for i in indices]
    return combined_set

class SetsCombiner(object):
  """
  This class works under a 2-way process:
  1) First, one or more of workSetWithQuantity tuples should be added to the object
  2) when all workSetWithQuantity tuples have been added to, calls to method next_combination() will "yield" one combination at a time, until None
  
  Eg.
  # ===========================================
  sc = SetsCombiner()
  workSetWithQuantity = ([1,2,3],2)
  sc.add_set_with_quantities(workSetWithQuantity)
  workSetWithQuantity = ([4,5],2)
  sc.add_set_with_quantities(workSetWithQuantity)
  workSetWithQuantity = ([6,7,8,9],3)
  sc.add_set_with_quantities(workSetWithQuantity)
  c=0
  for each in sc.next_combination():
    c+=1
    print c,'combination', each
  # ===========================================
  (( This piece of code results in: ))

  1 combination [1, 2, 4, 5, 6, 7, 8]
  2 combination [1, 2, 4, 5, 6, 7, 9]
  3 combination [1, 2, 4, 5, 6, 8, 9]
  4 combination [1, 2, 4, 5, 7, 8, 9]
  5 combination [1, 3, 4, 5, 6, 7, 8]
  6 combination [1, 3, 4, 5, 6, 7, 9]
  7 combination [1, 3, 4, 5, 6, 8, 9]
  8 combination [1, 3, 4, 5, 7, 8, 9]
  9 combination [2, 3, 4, 5, 6, 7, 8]
  10 combination [2, 3, 4, 5, 6, 7, 9]
  11 combination [2, 3, 4, 5, 6, 8, 9]
  12 combination [2, 3, 4, 5, 7, 8, 9]
  
  (( Individually, each workSet yields the sets below: ))
  
  workSetWithQuantity = ([1,2,3],2) yields
  [1, 2]
  [1, 3]
  [2, 3]
  ------------------------------
  workSetWithQuantity = ([4,5],2) yields
  [4, 5]
  ------------------------------
  workSetWithQuantity = ([6,7,8,9],3) yields
  [6, 7, 8]
  [6, 7, 9]
  [6, 8, 9]
  [7, 8, 9]

  The 3 cross-combined results in 12 sets (3*1*4=12)
  """
  def __init__(self):
    self.work_set_objs = []
    # after the first call to method combine(), object must not add workSets anymore
    self.lock_workSets_insertion = False
    self.LAST_INDEX = None
    self.total_combinations = None
    self.sets_to_join = None
    self.n_elements = None
    self.ongo_comb = None
    self.ongoing_ic = None
    self.horizontal_combined_set = None

  @property
  def n_slots(self):
    if self.ongo_comb is not None:
      return len(self.ongo_comb)
    return 0

  def instantiate_indices_combiner(self, work_set):
    if self.n_elements is None or self.n_slots is None:
      return None
    if self.n_elements < 1  or self.n_slots < 1:
      return None
    self.ongoing_ic = IndicesCombinerForCombinations(self.n_elements, self.n_slots)
    return self.ongoing_ic

  def is_work_set_with_quantity_valid(self, work_set_with_quantity):
    work_set = work_set_with_quantity[0]
    # work_set should not be empty, if it is, consider data invalid returning False
    if len(work_set) == 0:
      return False
    quantity = work_set_with_quantity[1]
    # quantity must be greater than 0, however, if it is less than 1, just return, no exception raising for this case
    if quantity < 1 or quantity > len(work_set):
      return False
    return True

  def add_set_with_quantities(self, work_set_with_quantity):
    if self.lock_workSets_insertion:
      errmsg = 'lock_workSets_insertion is True, ie, an inconsistent action (either static or dynamic) was issued. First all workSets are added, then the first call to combine() locks further additions.'
      raise IndexError(errmsg)
    if not self.is_work_set_with_quantity_valid(work_set_with_quantity):
      return
    work_set, quantity = work_set_with_quantity
    work_set_obj = WorkSet(work_set, self.instantiate_indices_combiner(work_set, quantity))
    self.work_set_objs.append(work_set_obj)
    
  def get_total_combinations(self):
    if self.total_combinations is None:
      return self.total_combinations
    self.total_combinations = 1
    for workSet in self.work_set_objs:
      self.total_combinations *= workSet.get_total_combinations() 
    return self.total_combinations

  def initialize_sets_to_join(self):
    self.sets_to_join = [[]] * len(self.work_set_objs)
    # self.horizontal_combined_sets = [] # to be used when it's desired to exchange the yield option for a memory-hungry solution
    # prepare first horizontal combined set!; run only once
    for i, workSetObj in enumerate(self.work_set_objs[:-1]):
      self.sets_to_join[i] = workSetObj.next()
    
  def join_sets(self):
    joint = []
    for s in self.sets_to_join:
      joint += s
    return joint

  def go_leftsideways_to_combine(self, depth):
    """
    This (somewhat light-weight) method is recursive (however notice that the "heavy-weight" combination generator is NOT recursive in this class, though it uses recursive in a child class)
    """
    self.work_set_objs[depth].restart()
    if depth < self.LAST_INDEX:
      # adjust self.sets_to_join for all slots, except the last (which already rounds in the combine() method) 
      self.sets_to_join[depth] = self.work_set_objs[depth].next()
    depth -= 1
    if depth < 0:
      # "Game Over" - processing is finished
      return False
    next_set = self.work_set_objs[depth].next()
    if next_set is not None:
      self.sets_to_join[depth] = next_set
      return True
    else:
      return self.go_leftsideways_to_combine(depth)
    
  def next_combination(self):
    """
    This method is not recursive. It has a while-loop with a "yield" (if right-most subset is formed not None) and go_leftsideways_to_combine() (when right-most subset is formed None)
    The exit from the 1-while-loop happens when go_leftsideways_to_combine() returns False, which indicates that all combinations have already been produced
    """
    self.lock_workSets_insertion = True # from here onwards, no further workSet can be added
    self.LAST_INDEX = len(self.work_set_objs) - 1
    self.initialize_sets_to_join()
    while 1:
      next_set = self.work_set_objs[self.LAST_INDEX].next()
      if next_set is not None:
        self.sets_to_join[self.LAST_INDEX] = next_set
        horizontal_combined_set = self.join_sets()
        #self.horizontal_combined_sets.append(horizontal_combined_set)
        self.horizontal_combined_set = horizontal_combined_set  
        yield horizontal_combined_set
      else:
        if self.go_leftsideways_to_combine(self.LAST_INDEX):
          continue
        else:
          break


class SetsCombinerMemoryIntensive(object):
  """
  This class has a "bridge" method called combineSets(self)
    that calls do_recursive_sets_combination(self.listOfTuple2)

  The latter function receives the listOfTuple2 that keeps the following information:
    first tuple element is a set (list) with dezenas to be combined according to the 
    second tuple element which is the quantity (or size) of each combination
    Eg
    ([12, 23, 33, 42, 57], 3) generates:
    12 23 33, 12 23 42, 12 23 57 ... up to 33 42 57
    
    The final result is the combination of all sets
    
    With this functionality, one possible of this class's
    
    Another example:  Observe the follow piece of code:

      sc = SetsCombiner()
      sc.add_set_with_quantities(([1,2,3],2))
      sc.add_set_with_quantities(([4,5,6],2))
      sc.combineSets()
      print sc.allCombinations    
  
  The print-out result is the 9-element set:
  
      [[1, 2, 4, 5], [1, 2, 4, 6], [1, 2, 5, 6], [1, 3, 4, 5], [1, 3, 4, 6], [1, 3, 5, 6], [2, 3, 4, 5], [2, 3, 4, 6], [2, 3, 5, 6]]
    
   Observations on performance:
   1) With this class, SetsCombinerMemoryIntensive, (having recursion, plus buffering all combinations)    
      gencounter 1634688 expected 1634688
      real  0m10.812s
      user  0m9.985s
      sys  0m0.380s

   2) With class SetsCombiner (above, having while (instead of recursion), plus having "yield", instead of buffering all combinations)    
      gencounter 1634688 expected 1634688
      real  0m6.866s
      user  0m6.728s
      sys  0m0.064s

  Conclusion, use preferencially SetsCombiner instead of this class (SetsCombinerMemoryIntensive)  
  """

  def __init__(self):

    self.nelements_nslots_tuplelist = [] #  # workSetsWithQuantities was formerly listOfTuple2
    self.total_combinations = None  # this is set when non-recursive computing is chosen
    self.all_combinations = []

  def get_all_combinations_recursive(self, index, being_combined=[]):
    """
    Memory-hungry !
    """
    # the trick is here is to "imagine" a 2D assignment
    # (the next loop goes vertically,
    #   the previous, horizontally)
    # print 'allCombinations', allCombinations, 'index', index 
    if index > len(self.nelements_nslots_tuplelist) - 1 :
      return []
    work_set_with_quantity = self.nelements_nslots_tuplelist[index]
    for work_set in generate_all_combinations_for_work_dict(work_set_with_quantity):
      being_combined_loop_added = being_combined + work_set
      received = self.get_all_combinations_recursive(index + 1, being_combined_loop_added)
      # the "final" return, at the end, means return None; if so, ie, if received is None, just loop onwards, if it's not None, it's a combined set to be added to all combined sets
      if received is not None:
        being_combined_loop_added += received 
        self.all_combinations.append(being_combined_loop_added[:])
    return

  def get_all_combinations(self): # Entrance to recursive method get_all_combinations_recursive()
    #return 
    self.all_combinations = []
    self.get_all_combinations_recursive(index=0, being_combined=[])
    '''c=0
    for comb in self.allCombinations:
      c+=1
      print c, 'Combination', comb''' 
    return self.all_combinations

  def calculate_total_combinations(self):
    self.total_combinations = 1
    for work_set_with_quantity in self.nelements_nslots_tuplelist:
      work_set = work_set_with_quantity[0]
      quantity = work_set_with_quantity[1]
      n_combinations_for_work_set = afc.combine_n_c_by_c_nonfact(len(work_set), quantity)
      self.total_combinations *= n_combinations_for_work_set
    return self.total_combinations 

  def get_total_combinations(self):
    """
    total_combinations is a combination n by c, the same that is known by n!((n-c)!c!)
    where n is workSet's size and c is IndicesCombiner's quantity 
    """
    if self.total_combinations is not None:
      return self.total_combinations
    self.calculate_total_combinations()
    return self.total_combinations

  def __len__(self):
    if self.all_combinations is not None:
      return len(self.all_combinations)
    if self.total_combinations is None:
      self.calculate_total_combinations()
    return self.total_combinations


class SetsCombinerWithTils(SetsCombiner):
  """
  This class inherits from SetsCombiner
  The idea here is to automatically fill in self.workSetsWithQuantities from a tilObj
  So at object instantiation every is run at once
     and after instantiation the object has its combined sets available 
  """
  def __init__(self, til_element):
    super().__init__()
    self.til_element = til_element
    self.unpack_til_obj()
    self.combineSets() # a parent class's method

  def unpack_til_obj(self):
    self.workSetsWithQuantities = self.til_element.getWorkSetsWithQuantities()

def create_work_sets_with_indices_combiner(work_set, ic_obj):
  work_sets = []
  for indices_array in ic_obj.all_sets_first_to_last(): # implement an iterator with yield in the future
    set_under_indices = [work_set[i] for i in indices_array]
    work_sets.append(set_under_indices)
  return work_sets
    
def generate_all_combinations_for_work_dict(nelements_nslots_tuple):
  n_elements = nelements_nslots_tuple[0]
  n_slots = nelements_nslots_tuple[1]
  if n_slots > len(n_elements):
    errmsg = ' generate_all_combinations_for_work_dict(workSetAndQuantity) :: n_slots=%d > len(n_elements)=%d cannot happen ' %(n_slots, len(n_elements))
    raise ValueError(errmsg)
  if n_slots == 0:
    return []
  if n_slots == 1 and len(n_elements) == 1:
    return n_elements[:]
  ic = IndicesCombinerForCombinations(len(n_elements) - 1, n_slots)
  work_sets = create_work_sets_with_indices_combiner(n_elements, ic)
  return work_sets

def do_recursive_sets_combination(work_sets_and_quantities, all_combinations=[[]]):
  if len(work_sets_and_quantities) == 0:
    return all_combinations
  work_set_and_quantity = work_sets_and_quantities.pop()
  work_sets = generate_all_combinations_for_work_dict(work_set_and_quantity)
  new_all_combinations = []
  for work_set in work_sets:
    for each_combination in all_combinations:
      #print 'summing', work_set, each_combination
      new_forming_set = work_set + each_combination
      new_forming_set.sort()
      new_all_combinations.append(new_forming_set)
  return do_recursive_sets_combination(work_sets_and_quantities, new_all_combinations)

def set_combine(work_set, pieces_size):
  ind_comb = IndicesCombinerForCombinations(len(work_set) - 1, pieces_size, False)
  print(ind_comb)
  print(ind_comb.next())
  index_all_sets = ind_comb.all_sets_first_to_last()
  real_sets = []
  for index_set in index_all_sets:
    real_set = []
    for index in index_set:
      real_set.append(work_set[index])
    real_sets.append(real_set)
  print(real_sets)
  return real_sets


def set_multiply(combine_array, cadeia=[], collected=[]):
  chunk = combine_array[0]
  if type(chunk) == type([]):
    list_elem = list(chunk)
  else:
    list_elem = [chunk]
  for elem in list_elem:
    #print elem, cadeia, collected
    if len(combine_array) == 1:
      collected.append(list(cadeia)+[elem])
    else:
      nothing = set_multiply(combine_array[1:], list(cadeia) + [elem], collected)
  return collected

def simulate_set_multiply():
  """

  """
  # ===========================================
  # sc = SetsCombiner()
  sc = SetsCombinerMemoryIntensive()
  workSetWithQuantity = ([1, 2, 3], 2)
  sc.add_set_with_quantities(workSetWithQuantity)
  workSetWithQuantity = ([4, 5], 2)
  sc.add_set_with_quantities(workSetWithQuantity)
  workSetWithQuantity = ([6, 7, 8, 9], 3)
  sc.add_set_with_quantities(workSetWithQuantity)
  for i, each in enumerate(sc.get_all_combinations()):
    seq = i + 1
    print(seq, 'combination', each)
  print('total comb',  sc.get_total_combinations())


def adhoctest1():
  simulate_set_multiply()
  
def adhoctest2():
  """

  """
  # sc = SetsCombiner()
  sc = SetsCombinerMemoryIntensive()
  workset_with_quantity = ([1,2,3], 2)
  sc.add_set_with_quantities(workset_with_quantity)
  workset_with_quantity = ([4,5,6], 2)
  sc.add_set_with_quantities(workset_with_quantity)
  for ws in sc.getAllSetsCombinationNonRecursively():
    print('ws', ws)

def ynext():
  for i in range(10):
    yield i


def adhoc_test3():
  """

  """
  combiner = SetsCombiner()
  s = ['a','b','c']
  n_elements, n_slots = 3, 2
  ws = WorkSet(s, IndicesCombinerForCombinations(n_elements, n_slots))
  comb = ws.next()
  while comb:
    print(comb)
    comb = ws.next()
  print('-'*30)
  n_elements, n_slots = 3, 2
  combiner.add_set_with_quantities((s, combsize))
  s = [4, 5]
  n_slots = 2
  ws = WorkSet(s, IndicesCombinerForCombinations(len(s) - 1, n_slots))
  comb = ws.next()
  while comb:
    print(comb)
    comb = ws.next()
  print('-'*30)
  combiner.add_set_with_quantities((s, combsize))
  s = [6,7,8,9]; combsize = 3
  ws = WorkSet(s, IndicesCombinerForCombinations(len(s) - 1, combsize, False))
  comb = ws.next()
  while comb:
    print(comb)
    comb = ws.next()
  print('-'*30)
  combiner.add_set_with_quantities((s, combsize))
  for comb in combiner.next_combination():
    print(comb)
  total_combinations = combiner.get_total_combinations()
  print('total_combinations =', total_combinations)


if __name__ == '__main__':
  """
  """
  adhoctest1()
