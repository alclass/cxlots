#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
cxlots/gen/chainers/
intersection.py


The class Intersect below receives (ie, is constructed with) two iteration-capable sets.

IMPORTANT prerequisite: the two inputting sets MUST be sorted in ascending order.

An iteration-capable set is one that follows Python's iteration protocol, it's capable of generating elements in a for-loop and implements next().

Method intersect() does the processing.

The processing is not search-optimized, but it's a good work-around, for the time being, for getting equal elements in two sets.

The logic to find equals is the following:
1) pick up two elements, one from each set
2) if the two are equal, save the element (to a writing data blob file object) and continue, go back to 1 above
3) not being equal, discard the lesser and pick up another element from the set that had the lesser element, go back to 2 above
4) if, at any moment, a set expires (ie, has no further elements for comparison), terminate processing. 


Example:

Set 1      Set 2
-----      -----
1,2,3      4,5,6
4,5,6      7,8,9

The result set will be:

Result Set
-----
4,5,6

ie, both set 1 and set 2 have tuple-element 4,5,6


To the future!

Once the two sets are a priori sorted in ascending order,
  this equal-fetch functionality could be done with an optimized search algorithm, 
  such as, for example, one implementing a binary search strategy.

Just for an illustration, let's visualize an instance where a long looping may occur and no equals exist.  
  Suppose a large set whose last element is lesser than the first element of the other set.
  In that scenario, all elements of set 1 will be looped wastefully, 
  because there are no equals once the first element "abroad" is greater than any element of set 1 that looped.

An optimized algorithm would avoid such non-efficient scenarios.

'''

import numpy, pickle, sys # 

import __init__
__init__.setlocalpythonpath()

import local_settings as ls

from models.Files.ReadBlob import BlobReader 

class ProcessingIsFinished(Exception):
  pass

class Intersect(object):
  
  def __init__(self, set_iter_1, set_iter_2, intersection_blob_filename = 'test_intersection.blob'):
    self.n_intersect     = 0
    self.set_iter_1      = set_iter_1
    self.set_iter_2      = set_iter_2
    self.set_iter_result = []
    self.set1_session_index = 0
    self.set2_session_index = 0
    self.intersection_blob_filename = intersection_blob_filename
    self.prepare_intersection_blob_filepickler()
    # first move ahead
    self.move_ahead()

  def prepare_intersection_blob_filepickler(self):
    datablob_path = ls.GENERATED_DATA_DIR + self.intersection_blob_filename
    fileobj       = open(datablob_path, 'wb')
    self.pickler  = pickle.Pickler(fileobj, pickle.HIGHEST_PROTOCOL)

  def intersect(self):
    PROCESSING_IS_FINISHED = False
    while not PROCESSING_IS_FINISHED:
      try:
        self.reposition_or_save_elements()
      except ProcessingIsFinished:
        PROCESSING_IS_FINISHED = True
    self.print_summary()
        
  def reposition_or_save_elements(self):
    if self.list_1 < self.list_2:
      self.move_ahead(1)
    elif self.list_1 > self.list_2:
      self.move_ahead(2)
    else: # ie, self.list_1 == self.list_2:
      self.save_intersection()
      self.move_ahead()
        
  def move_ahead(self, which=None):
    if which == None:
      self.get_set1_next()
      self.get_set2_next()
    elif which == 1:
      self.get_set1_next()
    elif which == 2:
      self.get_set2_next()
    else:
      raise ValueError, "Either set 1 or set 2 or both should go next, none were chosen. Halting to look for the problem."
    
  def get_set1_next(self):
    try:
      self.list_1 = self.set_iter_1.next()
      if self.list_1 == None:
        raise StopIteration
      if type(self.list_1) != tuple: # type(self.list_1) == numpy.ndarray or 
        self.list_1 = tuple(self.list_1)  # so that it works directly with operators >, < and ==
      self.set1_session_index += 1
      print self.set1_session_index, 'set 1', self.list_1
    except StopIteration:
      raise ProcessingIsFinished

  def get_set2_next(self):
    try:
      self.list_2 = self.set_iter_2.next()
      if self.list_2 == None:
        raise StopIteration
      if type(self.list_2) != tuple: # type(self.list_1) == numpy.ndarray or 
        self.list_2 = tuple(self.list_2)  # so that it works directly with operators >, < and ==
      self.set2_session_index += 1
      print self.set2_session_index, 'set 2', self.list_1
    except StopIteration:
      raise ProcessingIsFinished

  def save_intersection(self):
    self.n_intersect += 1
    print self.n_intersect, 'Intersection found:', self.list_1, 'idx 1', self.set1_session_index , 'idx 2', self.set2_session_index
    nparray = numpy.array(self.list_1) 
    self.pickler.dump(nparray)
    # self.set_iter_result.append(self.list_1)

  def print_summary(self):
    print 'Set 1 size:', self.set_iter_1.n_slots()
    print 'Set 2 size:', self.set_iter_2.n_slots()
    print 'N of intersects:', self.n_intersect
    print 'intersection file', self.intersection_blob_filename

  # ENDS class Intersect(object)


def process():
  pass


def fill_in_test_sets():
  set1 = []; set2 = [] 
  a = 1,2,3,4,5,6
  set1.append(a)
  a = 2,3,4,5,6,7
  set2.append(a)
  return set1, set2

def adhoc_test():
  # 'soma-100-a-200.blob')
  # 'line_drawing-2211.blob')
  blobfile1 = 'test.blob'
  blobfile2 = '1357090777.79.blob'
  set_iter_1 = BlobReader(blobfile1).get_iterator()
  set_iter_2 = BlobReader(blobfile2).get_iterator()
  intersect_obj = Intersect(set_iter_1, set_iter_2)
  intersect_obj.intersect()

import unittest
class MyTest(unittest.TestCase):

  def test_1(self):
    pass

def look_up_cli_params_for_tests_or_processing():
  for arg in sys.argv:
    if arg.startswith('-t'):
      del sys.argv[1]
      adhoc_test()
    elif arg.startswith('-u'):
      # unittest complains if argument is available, so remove it from sys.argv
      del sys.argv[1]
      unittest.main()
    elif arg.startswith('-p'):
      pass
      # process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
