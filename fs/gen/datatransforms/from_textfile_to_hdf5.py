#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys # , os, pickle, 
import numpy
import tables

import __init__
__init__.setlocalpythonpath()

import local_settings as ls


# Define a user record to characterize some kind of particles
class SixDozensHDF5(tables.IsDescription):
  
  d1 = tables.UInt8Col()  # unsigned byte
  d2 = tables.UInt8Col()  # unsigned byte
  d3 = tables.UInt8Col() # unsigned byte
  d4 = tables.UInt8Col() # unsigned byte
  d5 = tables.UInt8Col() # unsigned byte
  d6 = tables.UInt8Col() # unsigned byte

# The name of our HDF5 filename

filename = ls.GENERATED_DATA_DIR + 'Filtragem-TilR-excluding-97-patterns_2013-01-11.h5'

print "Creating file:", filename
# Open a file in "w"rite mode
h5file = tables.openFile(filename, mode = "w", title = "Megasena Combs Subset")

print
print   '-**-**-**-**-**- group and table creation  -**-**-**-**-**-**-**-'

# Create a new group under "/" (root)
group = h5file.createGroup("/", 'g1', 'Group 1')
print "Group '/g1' created"

# Create one table on it
datatable = h5file.createTable(group, 'filteredsubset', SixDozensHDF5, "Readout example")
print "Table '/g1/filteredsubset' created"

# Print the file
print h5file
print
print repr(h5file)


def read_textfile():
  jogo_struct = datatable.row
  textfilename = ls.GENERATED_DATA_DIR + 'all_combinations_against_excluding_tilrpatterns.dat'
  fileobj = open(textfilename, 'r')
  line = fileobj.readline(); counter=0
  while line:
    counter+=1
    line = line.rstrip('\n')
    if line.startswith('n_passed'):
      line = fileobj.readline()
      continue
    dezenas_as_str = line.split(' ')
    for i in xrange(6):
      try:
        dozen = int(dezenas_as_str[i])
        jogo_struct['d%d'%(i+1)] = dozen
      except ValueError:
        pass
    jogo_struct.append()
    last_line = line
    if counter % 1000000 == 0:
      print 'Flushing', counter, line
      datatable.flush()
    line = fileobj.readline()
  print counter, last_line
  h5file.close()

read_textfile()

def process():
  pass
  # read_textfile()

def adhoc_test():
  pass

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
      process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
