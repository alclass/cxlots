#!/usr/bin/env python
# -*- coding: utf-8 -*-
# local_settings.py
'''
@author: friend
'''
import sys
# numpy pickle,

import __init__
__init__.setlocalpythonpath()

#import local_settings as ls

#from maths2.tils import TilR
from maths.tils.TilProducer import TilProducer
from maths.tils.TilR import TilR
from maths.combinatorics.SetsCombiner import SetsCombiner
# from models.Files.ReadConcursosHistory import ConcursosHistoryPickledStorage
#from gen.GeradorIter import Gerador
#import fs.filters.filter_functions_dependent as filter_fd
from fs.strfs.str_patterns import trans_intlist_to_zfillstrlist

n_slots=5
tilr = TilR(n_slots)
all_generated = 0
def generate(wpattern):
  global all_generated
  pattern_list = map(int, wpattern)
  print wpattern, pattern_list
  # dozens_thru_slots = map(tilr.get_dozens_in_slot_n, xrange(n_slots))
  # print 'dozens_thru_slots', dozens_thru_slots
  combiner = SetsCombiner()
  for slot_n in xrange(n_slots):
    quantity = pattern_list[slot_n]
    if quantity == 0:
      continue 
    dozens = tilr.get_dozens_in_slot_n(slot_n)
    workSetWithQuantity = (dozens, quantity) 
    print 'Adding workSetWithQuantity', workSetWithQuantity
    combiner.addSetWithQuantities(workSetWithQuantity)
  total_combinations = combiner.get_total_combinations()
  all_generated += total_combinations
  print 'total_combinations', total_combinations
  # sys.exit(0) 
  for i, jogo in enumerate(combiner.next_combination()):
    jogo.sort()
    print all_generated, i, 'combining', trans_intlist_to_zfillstrlist(jogo)
  # sys.exit(0) 

def mount_all_combinations_with_including_tilrpatterns():
  # the excluding list was constructed with tilrpatterns occurring less than 4 times, there are 97 excluding wpatterns in a total of 180 
  excluding_tilrwpatterns = ['00006', '00060', '00600', '06000', '60000', '00015', '00051', '00105', '00150', '00501', '00510', '01005', '01050', '01500', '05001', '05010', '05100', '10005', '10050', '10500', '15000', '50001', '50010', '50100', '51000', '00024', '00042', '00204', '00240', '00402', '00420', '02004', '02040', '02400', '04002', '04020', '04200', '20004', '20040', '20400', '24000', '40002', '40020', '40200', '42000', '00114', '00141', '00411', '01014', '01041', '01401', '01410', '04011', '04101', '04110', '10014', '10104', '10140', '10401', '10410', '11004', '11040', '11400', '14001', '14010', '14100', '40011', '40101', '41001', '41010', '41100', '00033', '00303', '00330', '03003', '03030', '03300', '30003', '30030', '30300', '33000', '00132', '00213', '00321', '02031', '02103', '02301', '02310', '03012', '10203', '10302', '13002', '13020', '20310', '23001', '32100', '00222']
  n_excluding_patterns = len(excluding_tilrwpatterns)
  print 'n_excluding_patterns', n_excluding_patterns  
  n_slots=5; soma=6
  tilproducer = TilProducer(n_slots, soma)
  alltilwpatterns = tilproducer.alltilwpatterns
  n_total_patterns = len(alltilwpatterns)
  print 'n_total_patterns len(alltilwpatterns)', n_total_patterns  
  including_tilrwpatterns = []
  for wpattern in alltilwpatterns:
    if wpattern in excluding_tilrwpatterns:
      continue 
    including_tilrwpatterns.append(wpattern)
  n_including_patterns = len(including_tilrwpatterns)
  print 'n_including_patterns', n_including_patterns
  for wpattern in including_tilrwpatterns:
    generate(wpattern)
    

def process():
  '''
  '''
  mount_all_combinations_with_including_tilrpatterns()
  pass

def adhoc_test():
  '''
  '''
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
