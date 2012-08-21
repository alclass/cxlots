#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
calc_excludable_by_tils_01.py
'''
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()

from models.Concurso import ConcursoBase
from maths.tils.TilFreqSlotSeparator import TilFreqSlotSeparator
#from maths.tils.TilPatternsProducer import TilProducer
from maths.tils.ConcursoTil import ConcursoTil

indicate_greater_than = lambda pattern_slot, max_quant : pattern_slot > max_quant  # filtro passa-alta 

def filter_out(patterns_as_intlist, tilhistogram):
  '''
  tilhistogram is a "cut" filter, ie, if tilhistogram is [
  dezenas per tilslot: [7, 18, 20, 14, 1]
  '''
  filtered_patterns_as_intlist = []; patterns_filtered_out = []
  for pattern in patterns_as_intlist:
    if True in map(indicate_greater_than, pattern, tilhistogram):
      patterns_filtered_out.append(pattern)
    else:
      filtered_patterns_as_intlist.append(pattern)
  return filtered_patterns_as_intlist, patterns_filtered_out 


def adhoc_test():
  concursoBase = ConcursoBase()
  last_concurso = concursoBase.get_last_concurso()
  for nDoConc in range(1201, last_concurso.nDoConc + 1):
    concurso = concursoBase.get_concurso_by_nDoConc(nDoConc)
    line = '%d ' %nDoConc
    concursotil = ConcursoTil(concurso)
    for n_slots in [2, 3, 4, 5, 6, 10, 12]: 
      concursotil.reset_n_slots(n_slots)
      line += 'tslot%d%s ' %(n_slots, concursotil.get_tilpattern_interlaced_with_n_dozens_per_til()) #wpattern
    print line  

def adhoc_test1():
  concursoBase = ConcursoBase()
  last_concurso = concursoBase.get_last_concurso()
  for nDoConc in range(1001, last_concurso.nDoConc + 1):
    concurso = concursoBase.get_concurso_by_nDoConc(nDoConc)
    concursotil = ConcursoTil(concurso)
    anterior = nDoConc - 1
    print 'histfreq for conc', anterior, concursotil.get_histfreq_obj().get_histfreq_tuplelike_at(anterior)
    #print concursotil.get_dezenas_and_their_frequencies_for_concurso()
    for n_slots in [5, 6, 10]: 
      concursotil.reset_n_slots(n_slots)
      print 'dezenas, frequencies, tils:', concursotil.get_dezenas_their_frequencies_and_til_for_concurso()
      print 'concursotil', concursotil, 'wpatt', concursotil.wpattern 
      print 'BorderTupleOfTilSets', concursotil.getBorderTupleOfTilSets()
      tilfreqslotter = TilFreqSlotSeparator(n_slots)
      print tilfreqslotter.show_tilhistogram_table()
      print '-'*50      
   
def adhoc_test2():
  concursoBase = ConcursoBase()
  concurso = concursoBase.get_last_concurso()
  concursotil = ConcursoTil(concurso)
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

def adhoc_test3():
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

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
