#!/usr/bin/env python
# -*- coding: utf-8 -*-
# local_settings.py
'''
@author: friend
'''
import numpy, sys
# pickle,

import __init__
__init__.setlocalpythonpath()

import local_settings as ls

from maths.tils import TilR
# from models.Files.ReadConcursosHistory import ConcursosHistoryPickledStorage
from generators.GeradorIter import Gerador
import fs.gen.filters.filters.filter_functions_dependent as filter_fd
from fs.strfs.str_patterns import trans_intlist_to_zfillstrlist

def generate_all_combinations_against_excluding_tilrpatterns():
  # the excluding list was constructed with tilrpatterns occurring less than 4 times, there are 97 excluding wpatterns in a total of 180 
  excluding_tilrwpatterns = ['00006', '00060', '00600', '06000', '60000', '00015', '00051', '00105', '00150', '00501', '00510', '01005', '01050', '01500', '05001', '05010', '05100', '10005', '10050', '10500', '15000', '50001', '50010', '50100', '51000', '00024', '00042', '00204', '00240', '00402', '00420', '02004', '02040', '02400', '04002', '04020', '04200', '20004', '20040', '20400', '24000', '40002', '40020', '40200', '42000', '00114', '00141', '00411', '01014', '01041', '01401', '01410', '04011', '04101', '04110', '10014', '10104', '10140', '10401', '10410', '11004', '11040', '11400', '14001', '14010', '14100', '40011', '40101', '41001', '41010', '41100', '00033', '00303', '00330', '03003', '03030', '03300', '30003', '30030', '30300', '33000', '00132', '00213', '00321', '02031', '02103', '02301', '02310', '03012', '10203', '10302', '13002', '13020', '20310', '23001', '32100', '00222']
  n_slots=5; soma=6
  tilstats_reused_for_excluding_wpatterns = TilR.TilStats(n_slots, soma)
  for wpattern in excluding_tilrwpatterns:
    tilstats_reused_for_excluding_wpatterns.add_pattern_as_str(wpattern)
  #slider = ConcursoExt()
  #n_last_concurso = slider.get_n_last_concurso()
  filename = ls.GENERATED_DATA_DIR + 'all_combinations_against_excluding_tilrpatterns.blob'
  fileobj = open(filename, 'w')
  #pickler = pickle.Pickler(fileobj, pickle.HIGHEST_PROTOCOL)
  gerador = Gerador()
  n_passed = 0 
  print 'Processing', len(gerador), 'games, please wait.'
  for jogo_as_dezenas in gerador:
    bool_result = filter_fd.filter_in_those_not_having_tilrwpatterns(jogo_as_dezenas, tilstats_reused_for_excluding_wpatterns, history_nDoConc_range=None)
    if bool_result:
      np_dezenas = numpy.array(jogo_as_dezenas)
      # pickler.dump(np_dezenas)
      dezenas_zfill2 = trans_intlist_to_zfillstrlist(np_dezenas)
      output_line = dezenas_zfill2 + '\n'
      fileobj.write(output_line)
      n_passed += 1 
    all_index = gerador.iterator.session_index
    diff = all_index - n_passed
    print bool_result, dezenas_zfill2, 'n_passed=%d, all_index=%d, diff=%d' %(n_passed, all_index, diff)
  output_line = 'n_passed=%d, all_index=%d, diff=%d' %(n_passed, all_index, diff)
  print output_line 
  fileobj.write(output_line)
  fileobj.close()


def process():
  '''
  '''
  generate_all_combinations_against_excluding_tilrpatterns()
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
