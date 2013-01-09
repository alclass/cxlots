#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle, sys # numpy, os

import __init__
__init__.setlocalpythonpath()

import local_settings as ls

class BlobReaderIterator(object):

  def __init__(self, unpickler):
    self.unpickler = unpickler
    self.current = -1  # Not to be None here, because None is EOF, -1, though not used, is BOF
    self.session_counter = -1
    self.n_elements = 0

  def __len__(self):
    return self.n_elements

  def size(self):
    return len(self)

  def next(self):
    if self.current == None:
      raise StopIteration
    try:
      self.current = self.unpickler.load()
      self.session_counter += 1
      # print self.session_counter, self.current
      return self.current 
    except EOFError:
      self.current = None
      raise StopIteration    
  
class BlobReader(object):

  def __init__(self, datablob_filename):
    self.datablob_filename = datablob_filename
    self.set_unpickler()
    self.iterator  = BlobReaderIterator(self.unpickler)
    
  def get_iterator(self):
    return self.iterator

  def set_unpickler(self):
    datablob_path  = ls.GENERATED_DATA_DIR + self.datablob_filename
    fileobj        = open(datablob_path, 'rb')
    self.unpickler = pickle.Unpickler(fileobj)

  def __iter__(self):
    return self.iterator
  
  def __len__(self):
    return -1

  def size(self):
    return len(self)
  
  # here ENDS class Gerador(object):


def process():  
  '''
  '''
  blob_name     = raw_input("Type blob's name ? ")
  blob_filename = blob_name + '.blob'
  blob_path     = ls.GENERATED_DATA_DIR + blob_filename
  unpickle_obj  = pickle.Unpickler(open(blob_path, 'rb'))
  eof_of_unpickle = False; counter = 0
  while not eof_of_unpickle:
    try:
      obj = unpickle_obj.load()
      counter += 1
      print counter, obj
    except EOFError:
      eof_of_unpickle = True    


def adhoc_test():
  # blobfilename = 'test.blob' # '1357090777.79.blob'
  blobfilename = '1357090777.79.blob'
  blobreader = BlobReader(blobfilename)
  for intlist in blobreader:
    index = blobreader.iterator.session_counter 
    print index, intlist

import unittest
class MyTest(unittest.TestCase):

  def test_1(self):
    pass

def look_up_cli_params_for_tests_or_processing():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()
    elif arg.startswith('-u'):
      # unittest complains if argument is available, so remove it from sys.argv
      del sys.argv[1]
      unittest.main()
    elif arg.startswith('-p'):
      pass
      process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
