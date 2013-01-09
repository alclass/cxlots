#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
'''

'''
import localpythonpath
localpythonpath.setlocalpythonpath()

from lib import jogos_functions_dependent as jogos_fd # get_line_patterns, get_column_patterns etc.
def filter_in_those_within_coincides_histogram_range(jogo, coincides_ranges, up_to_nDoConc=None, LOOKUP_DEPTH=1000):
  '''
  
  coincides_ranges is a histogram (or dict in Python parlance) that has the tuple min and max cutoff filter values for all n_coincides
  
  An example of a coincides_ranges dict is cr below:

    cr[0]=(500, 520) # means 0 repeats in LOOKUP_DEPTH games must not be lower than 500, nor higher than 520
    cr[1]=(300, 400) # means 1 repeat  in LOOKUP_DEPTH games must be within the range 300 to 400 
    cr[2]=( 80,  90) # similar explanation as above
    cr[3]=( 35,  55) # similar explanation as above 
    cr[4]=(  5,  15) # similar explanation as above
    cr[5]=(  0,   0) # similar explanation as below
    cr[6]=(  0,   0) # means that 6 repeats (ie, equality) must not happen against all LOOKUP_DEPTH games 

  n_coincides, for Megasena for example, is the tuple (0,1,2,3,4,5,6), ie, any possible number of dozens that repeat between two games.
  If n_coincides is 6, then, the two games are [[[ the same ]]].
  If n_coincides is 5, then, one game has a "quina" in the other (and vice versa!)
    eg. [ 1 2 3 4 5 6] and [ 1 2 3 4 5 7] 
  If n_coincides is 0, then, the two comparing games are fully different
    eg. [ 1 2 3 4 5 6] and [ 7 8 9 10 11 12] 
  
  The LOOKUP_DEPTH determines how many games will be considered, down from up_to_nDoConc, to make up the coincides_histogram
  This coincides_histogram is got from a "jogos function: get_coincides_histogram_against_a_lookup_depth()".

  To further visualize the coincides_histogram, let ch (with LOOKUP_DEPTH=1000) look like:

    ch[0]=518
    ch[1]=345
    ch[2]=82
    ch[3]=42
    ch[4]=13
    ch[5]=0
    ch[6]=0

  Notice also that sum(ch.values()) must equal LOOKUP_DEPTH, ie. 518+345+82+42+13+0+0=1000
  These values will be "contrasted" against coincides_ranges. Let's see a filter-in "passing" example:
   
  Let coincides_ranges be cr below:

    cr[0]=(500, 520) # seen above, 518 is within (500, 520), pass
    cr[1]=(300, 400) # seen above, 345 is within (300, 400), pass 
    cr[2]=( 80,  90) # seen above,  82 is within ( 80,  90), pass
    cr[3]=( 35,  55) # seen above,  42 is within ( 35,  55), pass
    cr[4]=(  5,  15) # seen above,  15 is within (  5,  15), pass
    cr[5]=(  0,   0) # seen above,   0 is within (  0,   0), pass
    cr[6]=(  0,   0) # seen above,   0 is within (  0,   0), pass
  
  A filter-in "not passing" example, further developing the example above, is when ch has values outside the ranges given in cr.

  '''
  coincides_histogram = jogos_fd.get_coincides_histogram_against_a_lookup_depth(jogo, up_to_nDoConc, LOOKUP_DEPTH)
  each_coincide_list = coincides_histogram.keys()
  for n_coincide in each_coincide_list:
    min_concursos_against_depth_with_n_coincides = coincides_ranges[n_coincide][0]
    max_concursos_against_depth_with_n_coincides = coincides_ranges[n_coincide][1]
    if coincides_histogram[n_coincide] < min_concursos_against_depth_with_n_coincides or coincides_histogram[n_coincide] > max_concursos_against_depth_with_n_coincides:
      return False
    return True


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
      pass
      # process()


if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
