#!/usr/bin/env python3
"""
commands/cards/conferidores/reg_vols_pgs_por_conc.py
  Registers 'volantes' (ie cardgames) that were made (paid) into a lotteric house (or maybe via the Internet).
  This registration is done into a database
    (which may be a SQL one or, perhaps, a simple textfile, or the two -- this definition is found here).
  The db formed here may be used for two purposes, ie:
    p1 checking results 'immediately' after its public drawing
    p2 checking comparisons with past or (when happen) later 'concursos'

in_between_1_and_60 = lambda x : x >= 1 and x <= 60
import fs.system_wide_lambdas as swlambdas
import sys  # os, random
"""
import time


class LineToDezenas(object):
  def __init__(self):
    self.line = None
    self.dezenas = []
    self.dezenas_str_list = ""

  def get_dezenas_from_line(self, line, sort_them=False):
    self.line = line
    self.decide_which_splitline()
    self.check_dozens_consistency()
    if sort_them:
      self.dezenas.sort()
    return self.dezenas

  def decide_which_splitline(self):
    """
    Decides via 3 options, ie:
    o1 either it's a 12-char string with 2-digit each dozen eg "010203040506".
    o2 or it's a comma-separated number string eg "1, 2, 3, 4, 5, 6".
    o3 or it's a space-separated number string eg "1 2 3 4 5 6"
    """
    self.dezenas_str_list = []
    if self.line.find(' ') < 0:
      i = 0
      index_begins = 2*i
      index_ends = 2*i+2
      while index_ends <= len(self.line):
        self.dezenas_str_list.append(self.line[index_begins: index_ends])
        i += 1
        index_begins = 2*i
        index_ends = 2*i+2
      # raise TypeError, 'Size of string for dozens, if no blanks entered, should be 12.'
    elif self.line.find(',') > - 1:
      self.dezenas_str_list = self.line.split(',')
    else:
      self.dezenas_str_list = self.line.split(' ')

  def check_dozens_consistency(self):
    """
    #error_msg = ''
    """
    self.dezenas = list(map(int, self.dezenas_str_list))
    if len(self.dezenas) != 6:
      errmsg = 'Number of entered dozens not equal to 6 :: %s ' % (str(self.dezenas))
      raise ValueError(errmsg)
    if False in map(lambda n: n >= 1 & n <= 60, self.dezenas):
      errmsg = 'There is one or more dozens out of range 1 to 60 :: %s ' % str(self.dezenas)
      raise ValueError(errmsg)
    # ===========================================================================
    # except ValueError:
    #  if error_msg == '':
    #    error_msg = 'error with %s' %(str(self.dezenas))
    #  print 'Error:', error_msg
    # ===========================================================================
      # self.finalize()
      # sys.exit(1)


class PaidGamesInputter(object):

  def __init__(self):
    self.open_outfile()
    self.dezenas = []
    self.all_typed_in_dozens = []
    self.lineToDezenasObj = LineToDezenas()
    self.filename = None
    self.outfile = None

  def open_outfile(self):
    self.filename = time.ctime() + '.log'
    self.outfile = open(self.filename, 'w')
    print('Opening', self.filename)

  def process(self):
    line = input('Type Volante Numbers d1 d2 d3 d4 d5 d6 ==>> ')
    try:
      while len(line) > 0:
        self.process_line(line)
        line = input('Type Volante Numbers d1 d2 d3 d4 d5 d6 ==>> ')
    except KeyboardInterrupt:
      print()
    self.finalize()

  def process_line(self, line):
    try:
      self.dezenas = self.lineToDezenasObj.get_dezenas_from_line(line)
    except ValueError as e:
      print(e)
      return
    if self.are_dozens_repeated():
      print('Dozens repeated, not writing them to output file')
    else:
      self.write_dozens_to_outfile()
  
  def are_dozens_repeated(self):
    if self.dezenas in self.all_typed_in_dozens:
      return True
    self.all_typed_in_dozens.append(self.dezenas[:])
    return False
   
  def write_dozens_to_outfile(self):
    dezenas_str_list = map(lambda s: str(s).zfill(2), self.dezenas)
    dezenas_str = ' '.join(dezenas_str_list)
    print('Writing', dezenas_str)
    self.outfile.write(dezenas_str + '\n')

  def finalize(self):
    print('Closing', self.filename)
    self.outfile.close()


def process():
  inputter = PaidGamesInputter()
  inputter.process()


def adhoc_test():
  pass


if __name__ == '__main__':
  adhoc_test()
  process()
