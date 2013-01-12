#!/usr/bin/env python
# -*- coding: utf-8 -*-
# local_settings.py
'''
Created on 28/12/2012

@author: friend
'''

import __init__
__init__.setlocalpythonpath()

from models.ReadConcursosHistory import ConcursosHistoryPickledStorage
from lib.funcsForStringPatternsEtAl import convert_intlist_to_spaced_zfillstr
import random

def has_game_equal_or_more_than_n_acertos(compare_dezenas, all_jogos_as_dezenas, cant_have_n_acertos = 3):
  '''
  This function is a filter-like operator that runs compare_dezenas (a list of ints) against a history of games
    (each game is a compare_dezenas compatible)
  If, as all games loop up to be compare, more than upToAcertos coincide, False is returned rightaway
  After all games have looped up -- ie, a False not happening before -- True will be returned at the end
  '''
  for jogo in all_jogos_as_dezenas:
    n_acertos = 0
    equals = []
    for compare_dezena in compare_dezenas:
      if compare_dezena in jogo:
        n_acertos += 1
        equals.append(compare_dezena)
      if n_acertos >= cant_have_n_acertos:
        print 'n_acertos=%d >= cant_have_n_acertos=%d %s %s %s' %(n_acertos, cant_have_n_acertos, str(compare_dezenas), str(jogo), str(equals))
        return True
  return False

class LoopedTooMuchException(TypeError):
  '''
  This is an "empty" exception class
  Its purpose is to raise itself when a WHILE-LOOP takes more iterations than a certain threshold alloted to it
  '''
  pass

class TupleGetter(object):
  '''
  This class have only one "working" method, ie, get_tuple()
  get_tuple()'s purpose is to return a random integer n-tuple
  Eg.
    tupleGetter = TupleGetter()
    random_dezenas = self.tupleGetter.get_tuple()
    print random_dezenas ==>> [3, 6, 17, 32, 41, 59]
  '''
  
  def __init__(self, n_numbers=6, lowerInt=1, upperInt=60):
    self.n_numbers = n_numbers
    self.lowerInt  = lowerInt
    self.upperInt  = upperInt
    self.randint   = random.Random()
    self.MAX_LOOP_LIMIT = self.n_numbers * 2 + self.upperInt - self.lowerInt
    self.randintObj = random.Random()
  
  def get_tuple(self):
    t=[]; n_iterations = 0
    while len(t) < self.n_numbers:
      d = self.randintObj.randint(self.lowerInt, self.upperInt)
      if d not in t:
        t.append(d)
      n_iterations += 1
      if n_iterations > self.MAX_LOOP_LIMIT: # can loop up to this limit
        raise LoopedTooMuchException, 'LoopedTooMuchException' 
    return t

  # ENDS class TupleGetter(object):

class GameProducer(object):

  def __init__(self):
    self.CUTOFF_N_ACERTOS = 4
    self.fraction_to_size_reduce_generated_games = 1
    self.N_TO_PRODUCE = 120
    self.open_outfile()
    self.tupleGetter = TupleGetter()

  def process(self):
    self.prepare()
    self.read_all_past_concursos()
    self.produce()
    self.reduce_generate_size()
    self.write_all_jogos_to_file()
    self.outfile.close()

  def prepare(self):
    pass

  def open_outfile(self):
    self.filename = 'Megasena Random Games Generation.log'
    self.outfile = open(self.filename, 'w')

  def read_all_past_concursos(self):
    print 'Please wait. Reading database :: read_all_past_concursos() '
    pickled_conc_hist = ConcursosHistoryPickledStorage()
    self.all_jogos_as_dezenas = pickled_conc_hist.read_or_create()

  def produce(self):
    #print 'concurso nº', nDoConc, concurso
    print 'Starting process of random generation'
    n_done = 0; n_iterations = 0
    self.all_random_dezenas = []
    while n_done < self.N_TO_PRODUCE:
      n_iterations += 1
      if n_iterations >  self.N_TO_PRODUCE * 3 * 10 ** 9:
        raise LoopedTooMuchException, 'WHILE-LOOP Iterations exceeded self.N_TO_PRODUCE * 3 = %d' %(self.N_TO_PRODUCE * 3)
      random_dezenas = self.tupleGetter.get_tuple()
      random_dezenas.sort()
      print n_iterations, n_done+1, 'Random Game', random_dezenas
      if has_game_equal_or_more_than_n_acertos(random_dezenas, self.all_jogos_as_dezenas, cant_have_n_acertos = self.CUTOFF_N_ACERTOS):
        continue
      if self.is_random_jogo_a_repeat(random_dezenas):
        continue
      n_done += 1
      self.all_random_dezenas.append(random_dezenas[:])
      print n_done, random_dezenas
      
  def is_random_jogo_a_repeat(self, random_dezenas):
    for jogo in self.all_random_dezenas:
      if jogo == random_dezenas:
        return True
    return False
    
  def reduce_generate_size(self, fraction=None):
    if fraction == None:
      fraction = self.fraction_to_size_reduce_generated_games
    if fraction == 1:
      return
    new_size = int( len(self.all_random_dezenas) * fraction )
    while len(self.all_random_dezenas) > new_size:
      index = random.randint(0, len(self.all_random_dezenas)-1)
      print 'Deleting', index, self.all_random_dezenas[index] 
      del self.all_random_dezenas[index]

  def save(self):
    self.write_all_jogos_to_file()

  def write_all_jogos_to_file(self):
    n_done = 0
    for dezenas in self.all_random_dezenas:
      dezenas_str = convert_intlist_to_spaced_zfillstr(dezenas)
      n_done +=1
      print 'Writing', n_done, dezenas_str
      self.outfile.write(dezenas_str + '\n')

  def close_outfile(self):
    self.outfile.close()

  # ENDS class GameProducer(object):

def process():
  gameProducer = GameProducer()
  gameProducer.process()
  
if __name__ == '__main__':
  process()
