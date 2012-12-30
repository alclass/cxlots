#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time # os, random, sys


in_between_1_and_60 = lambda x : x >= 1 and x <= 60
zfill2 = lambda x : str(x).zfill(2)

class LineToDezenas(object):
  
  def get_dezenas_from_line(self, line, sortThem=False):
    self.line = line
    self.decide_which_splitline()
    self.check_dozens_consistency()
    if sortThem:
      self.dezenas.sort()
    return self.dezenas

  def decide_which_splitline(self):
    self.dezenas_str_list = []
    if self.line.find(' ') < 0:
      i=0; index_begins = 2*i; index_ends = 2*i+2 
      while index_ends <= len(self.line):
        self.dezenas_str_list.append(self.line[index_begins : index_ends])
        i+=1; index_begins = 2*i; index_ends = 2*i+2 
      # raise TypeError, 'Size of string for dozens, if no blanks entered, should be 12.'
    elif self.line.find(',') > - 1:
      self.dezenas_str_list = self.line.split(',')
    else:
      self.dezenas_str_list = self.line.split(' ')

  def check_dozens_consistency(self):
    #errorMsg = ''
    self.dezenas = map(int, self.dezenas_str_list)
    if len(self.dezenas) != 6:
      errorMsg = 'Number of entered dozens not equal to 6 :: %s ' %(str(self.dezenas))
      raise ValueError, errorMsg
    if False in map(in_between_1_and_60, self.dezenas):
      errorMsg = 'There is one or more dozens out of range 1 to 60 :: %s ' %(str(self.dezenas))
      raise ValueError, errorMsg
    #===========================================================================
    # except ValueError:
    #  if errorMsg == '':
    #    errorMsg = 'error with %s' %(str(self.dezenas))
    #  print 'Error:', errorMsg
    #===========================================================================
      # self.finalize()
      # sys.exit(1)


class PaidGamesInputter(object):

  def __init__(self):
    self.open_outfile()
    self.all_typed_in_dozens = []
    self.lineToDezenasObj = LineToDezenas()
    
  def open_outfile(self):
    self.filename = time.ctime() + '.log'
    self.outfile = open(self.filename, 'w')
    print 'Opening', self.filename

  def process(self):
    line = raw_input('Type Volante Numbers d1 d2 d3 d4 d5 d6 ==>> ')
    try:
      while len(line) > 0:
        self.process_line(line)
        line = raw_input('Type Volante Numbers d1 d2 d3 d4 d5 d6 ==>> ')
    except KeyboardInterrupt:
      print
    self.finalize()

  def process_line(self, line):
    try:
      self.dezenas = self.lineToDezenasObj.get_dezenas_from_line(line)
    except ValueError, exception:
      print exception
      return
    if self.are_dozens_repeated():
      print 'Dozens repeated, not writing them to output file' 
    else:
      self.write_dozens_to_outfile()
  
  def are_dozens_repeated(self):
    if self.dezenas in self.all_typed_in_dozens:
      return True
    self.all_typed_in_dozens.append(self.dezenas[:])
    return False
   
  def write_dozens_to_outfile(self):
    dezenas_str_list = map(zfill2, self.dezenas)
    dezenas_str = ' '.join(dezenas_str_list)
    print 'Writing', dezenas_str
    self.outfile.write(dezenas_str + '\n')

  def finalize(self):
    print 'Closing', self.filename
    self.outfile.close()

def process():
  inputter = PaidGamesInputter()
  inputter.process()

if __name__ == '__main__':
  process()
