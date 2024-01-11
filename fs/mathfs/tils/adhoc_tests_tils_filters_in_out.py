#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
import sys

import __init__
__init__.setlocalpythonpath()

from models.Concursos.concurso_extended import ConcursoExt
from maths.tils.TilFreqSlotSeparator import TilFreqSlotSeparator
#from maths2.tils.TilPatternsProducer import TilProducer
from maths.tils.ConcursoTil import ConcursoTil
from maths.tils.TilR import TilR


def adhoc_test1():
  slider = ConcursoExt()
  for nDoConc in range(1401, slider.get_n_last_concurso() + 1):
    concurso = slider.get_concurso_by_nDoConc(nDoConc)
    line = '%d ' %nDoConc
    concursotil = ConcursoTil(concurso)
    for n_slots in [2, 3, 4, 5, 6, 10, 12]: 
      concursotil.reset_n_slots(n_slots)
      line += 'tslot%d%s ' %(n_slots, concursotil.get_tilpattern_interlaced_with_n_dozens_per_til()) #wpattern
    print line  

def adhoc_test2():
  slider = ConcursoExt()
  for nDoConc in range(1401, slider.get_n_last_concurso() + 1):
    concurso = slider.get_concurso_by_nDoConc(nDoConc)
    concursotil = ConcursoTil(concurso)
    concursotilr = TilR(n_slots = 5, concurso=concurso)

    nDoConc_anterior = nDoConc - 1
    print concurso.n_conc, concurso.date, concurso.get_dezenas(), concurso.get_dezenas_in_orig_order()
    print 'histfreq for conc', nDoConc_anterior, concursotil.get_histfreq_obj().get_histfreq_tuplelike_at(nDoConc_anterior)
    #print concursotil.get_dezenas_and_their_frequencies_for_concurso()
    for n_slots in [5, 6, 10]: 
      concursotil.reset_n_slots(n_slots)
      print 'dezenas, frequencies, tils:', concursotil.get_dezenas_their_frequencies_and_til_for_concurso()
      print 'concursotil', concursotil, 'wpatt', concursotil.wpattern 
      print 'BorderTupleOfTilSets', concursotil.getBorderTupleOfTilSets()
      tilfreqslotter = TilFreqSlotSeparator(n_slots)
      print tilfreqslotter.show_tilhistogram_table()
      print '-'*50      
    print '=*'*27

def adhoc_test3():
  slider = ConcursoExt()
  last_concurso = slider.get_last_concurso()
  concursotil = ConcursoTil(last_concurso)
  print 'concursotil', concursotil, 'wpatt', concursotil.wpattern 
  # tilproducer = TilProducer(5, 6)
  tilfreqslotter = TilFreqSlotSeparator(5)
  # print tilproducer.alltilwpatterns 
  # patterns_as_intlist = tilproducer.get_alltilpatterns_as_intlist()
  # tilsets = tilfreqslotter.getTilSets()
  n_dozens_per_tilslot = tilfreqslotter.get_quantities_of_dozens_per_tilslot()
  print 'dezenas per tilslot:', n_dozens_per_tilslot 
  # tilhistogram = tilfreqslotter.get_tilhistogram()
  #print 'tilhistogram:', tilhistogram 
  # filtered_patterns_as_intlist, patterns_filtered_out = filter_out(patterns_as_intlist, tilhistogram)
  # print 'filtered_patterns_as_intlist', filtered_patterns_as_intlist, len(filtered_patterns_as_intlist)
  # print 'filtered out patterns', patterns_filtered_out, len(patterns_filtered_out)
  tilfreqslotter.show_slot_elements()
  print tilfreqslotter.show_tilhistogram_table()      

def adhoc_test4():
  tilfreqslotter = TilFreqSlotSeparator(5)
  tilfreqslotter.show_slot_elements()
  print tilfreqslotter.show_tilhistogram_table()      
  print '='*40
  tilfreqslotter = TilFreqSlotSeparator(6)
  tilfreqslotter.show_slot_elements()
  print tilfreqslotter.show_tilhistogram_table()      
  print '='*40
  tilfreqslotter = TilFreqSlotSeparator(10)
  tilfreqslotter.show_slot_elements()
  print tilfreqslotter.show_tilhistogram_table()      
  print '='*40
  tilfreqslotter = TilFreqSlotSeparator(12)
  tilfreqslotter.show_slot_elements()
  print tilfreqslotter.show_tilhistogram_table()      
  print '='*40
  tilfreqslotter = TilFreqSlotSeparator(32)
  tilfreqslotter.show_slot_elements()
  print tilfreqslotter.show_tilhistogram_table()    


def process():
  pass

def adhoc_test():
  NO_FUNCTION_CALLED = False
  try:
    n_test = int(sys.argv[2])
    adhocfuncname = 'adhoc_test%d()' %n_test 
    exec(adhocfuncname)
  except ValueError:
    NO_FUNCTION_CALLED = True
  except IndexError:
    NO_FUNCTION_CALLED = True
  if NO_FUNCTION_CALLED:
    # default
    adhoc_test1()


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
      # process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
