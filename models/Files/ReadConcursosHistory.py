#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy, os, pickle, sys

import __init__
__init__.setlocalpythonpath()

import local_settings as ls

# IMPORTANT: this module should import ConcursoHTML instead of ConcursoExt, because the latter imports this one!!! 
from models.Concursos.ConcursoHTML import ConcursoHTML
from libfunctions.jogos import jogos_functions

# ATTENTION: READ_CONCHIST constants start with 1!!!
# Reason: see method HistoryReader.set_read_as_id(), this methods needs to know the constants' range, its min and max.
READ_CONCHIST_AS_2D_ORDERED_MATRIX           = 1
READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS    = 2
# ATTENTION: When adding a new CONSTANT, update the last one below!!!
READ_CONCHIST_AS_TIMEONWARDS_NONORDERED_INTS = 3
READ_CONCHIST_LAST_ID                        = READ_CONCHIST_AS_TIMEONWARDS_NONORDERED_INTS

def read_concursos_history(do_ordered_dozens=False):
  all_histjogos_as_dezenas = []
  slider = ConcursoHTML()
  # print 'Please wait. Reading database :: read_all_past_concursos() '
  concursos = slider.get_all_concursos()
  for concurso in concursos:
    if do_ordered_dozens:
      dezenas = concurso.get_dezenas()
    else:
      dezenas = concurso.get_dezenas_in_orig_order()
    # print i, # dezenas
    if concurso.nDoConc % 250 == 0:
      pass
      # print concurso.nDoConc, 'done'
    all_histjogos_as_dezenas.append(dezenas)
  return all_histjogos_as_dezenas

def set_read_as_id(read_as_id):
  if read_as_id == None:
    # Default
    read_as_id = READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS
    return read_as_id 
  try:
    int(read_as_id)
  except ValueError:
    # Default
    read_as_id = READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS
    return read_as_id 
  if read_as_id < 1 or read_as_id > READ_CONCHIST_LAST_ID:
    # Default
    read_as_id = READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS
  return read_as_id 

def set_upper_nDoConc(last_nDoConc, upper_nDoConc = None):
  if upper_nDoConc == None:
    # Default
    return last_nDoConc 
  try:
    int(upper_nDoConc)
  except ValueError:
    # Default
    return last_nDoConc 
  if upper_nDoConc < 1 or upper_nDoConc > last_nDoConc: 
    # Default
    return last_nDoConc
  # if none of the above returned, let it be itself! 
  return upper_nDoConc 

class CantKnowWhichBlobFileToReadFrom(TypeError):
  pass

class ConcursosHistoryPickledStorage(object):

  def __init__(self, read_as_id=None, upper_nDoConc=None):
    self.set_read_as_id(read_as_id)
    self.numpy_histjogos = []
    slider               = ConcursoHTML()
    self.last_nDoConc    = slider.get_n_last_concurso()
    self.total_concursos = slider.get_total_concursos()
    self.set_upper_nDoConc(upper_nDoConc)

  def set_read_as_id(self, read_as_id=None):
    self.read_as_id = set_read_as_id(read_as_id)

  def set_upper_nDoConc(self, upper_nDoConc=None):
    self.upper_nDoConc = set_upper_nDoConc(self.last_nDoConc, upper_nDoConc)
    self.read_or_create_not_returning_list

  def get_concursos_up_to_upper_nDoConc(self):
    if len(self.numpy_histjogos) != self.total_concursos:
      raise IndexError, 'An Inconsistent Condition happened: len(self.numpy_histjogos)=%d != self.total_concursos=%d ' %(len(self.numpy_histjogos), self.total_concursos)
    return self.numpy_histjogos[:self.upper_nDoConc-1]

  def read_or_create_not_returning_list(self):
    '''
    Just to fill-in attribute self.numpy_histjogos
    '''
    if self.blob_file_exists():
      self.read_from_blob_file()
    else:
      self.create_blob_file_timeonwards_ordered_ints()

  def read_or_create(self):
    if self.blob_file_exists():
      return self.output_list_reading_from_blob_file()
    return self.output_list_creating_blob_file()
  
  def blob_file_exists(self):
    self.set_read_as_names()
    self.blobfilename = '%s%d.blob' %(self.read_as_name, self.last_nDoConc) # IMPORTANT: it's always the LAST ONE!!! Previous ones are cut down! 
    self.blobfilepath = ls.GENERATED_DATA_DIR + self.blobfilename
    if os.path.isfile(self.blobfilepath):
      return True
    else:
      return False

  def set_read_as_names(self):
    
    if self.read_as_id == READ_CONCHIST_AS_2D_ORDERED_MATRIX:
      self.read_as_name = '2D_ORDERED_MATRIX-'
    elif self.read_as_id == READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS:
      self.read_as_name = 'TIMEONWARDS_ORDERED_INTS-'
    elif self.read_as_id == READ_CONCHIST_AS_TIMEONWARDS_NONORDERED_INTS:
      self.read_as_name = 'TIMEONWARDS_NONORDERED_INTS-'

  def output_list_reading_from_blob_file(self):
    self.read_from_blob_file()
    return self.get_concursos_up_to_upper_nDoConc()

  def read_from_blob_file(self):
    # print 'Load Picking from self.blobfilepath =', self.blobfilepath
    self.numpy_histjogos = [] # pickle.load(open(self.blobfilepath, 'rb'))
    unpickle_obj = pickle.Unpickler(open(self.blobfilepath, 'rb'))
    eof_of_unpickle = False; counter = 0
    while not eof_of_unpickle:
      try:
        if counter + 1 > self.upper_nDoConc:
          break
        counter += 1
        dezenas = unpickle_obj.load()
        self.numpy_histjogos.append(dezenas)
        # print counter, dezenas
      except EOFError:
        eof_of_unpickle = True 

  def output_list_creating_blob_file(self):
    if self.read_as_id == READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS or self.read_as_id == READ_CONCHIST_AS_TIMEONWARDS_NONORDERED_INTS:
      return self.output_list_creating_blob_file_timeonwards_ordered_ints()
    elif self.read_as_id == READ_CONCHIST_AS_2D_ORDERED_MATRIX:
      return self.output_list_creating_blob_file_2d_ordered_matrix()

  def output_list_creating_blob_file_timeonwards_ordered_ints(self):
    '''
    IMPORTANT! When creating the blob file, it's always to store ALL games, but the returning list/tuple is smaller if self.upper_nDoConc < self.last_nDoConc 
    '''
    self.create_blob_file_timeonwards_ordered_ints()
    # pickle.dump(numpy_histjogos, ,)
    if self.upper_nDoConc < self.last_nDoConc:
      return self.numpy_histjogos[:self.upper_nDoConc]
    return self.numpy_histjogos

  def create_blob_file_timeonwards_ordered_ints(self):
    pickle_obj = pickle.Pickler(open(self.blobfilepath, 'wb'), pickle.HIGHEST_PROTOCOL)
    if self.read_as_id == READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS:
      do_ordered_dozens = True
    else:
      do_ordered_dozens = False
    all_histjogos_as_dezenas = read_concursos_history(do_ordered_dozens)
    self.numpy_histjogos = []
    print 'Picking to self.blobfilepath =', self.blobfilepath, ' pickle.HIGHEST_PROTOCOL =', pickle.HIGHEST_PROTOCOL, 'for', len(all_histjogos_as_dezenas), 'jogos'
    for dozens in all_histjogos_as_dezenas:
      numpy_jogo = numpy.array(dozens)
      self.numpy_histjogos.append(numpy_jogo)
      pickle_obj.dump(numpy_jogo)


  def output_list_creating_blob_file_2d_ordered_matrix(self):
    pass


class ConcursosHistoryMetrics(ConcursosHistoryPickledStorage):

  def __init__(self, read_as_id=None, upper_nDoConc=None):
    '''
    To refactor:
    1) use the Super() function
    2) after the Super(), keep up only the last line below
    '''
    self.set_read_as_id(read_as_id)
    self.last_nDoConc = find_last_nDoConc()
    self.set_upper_nDoConc(upper_nDoConc)
    self.numpy_histjogos = []
    self.read_or_create_not_returning_list()
  
  def find_impares_histogram_for_games(self):
    impares_histogram = {}
    for jogo in self.numpy_histjogos:
      n_impares = jogos_functions.get_n_impares(jogo)
      if impares_histogram.has_key(n_impares):
        impares_histogram[n_impares] += 1
      else:
        impares_histogram[n_impares] = 1
    return impares_histogram
  
  def find_sum_histogram_for_games(self):
    sum_histogram = {}
    for jogo in self.numpy_histjogos:
      soma = sum(jogo)
      if sum_histogram.has_key(soma):
        sum_histogram[soma] += 1
      else:
        sum_histogram[soma] = 1
    return sum_histogram
  
  def find_line_pattern_histogram_games(self):
    line_pattern_histogram = {}
    for jogo in self.numpy_histjogos:
      line_pattern = jogos_functions.get_line_pattern(jogo)
      if line_pattern_histogram.has_key(line_pattern):
        line_pattern_histogram[line_pattern] += 1
      else:
        line_pattern_histogram[line_pattern] = 1
    return line_pattern_histogram
  
  def find_column_pattern_histogram_games(self):
    column_pattern_histogram = {}
    for jogo in self.numpy_histjogos:
      column_pattern = jogos_functions.get_column_pattern(jogo)
      if column_pattern_histogram.has_key(column_pattern):
        column_pattern_histogram[column_pattern] += 1
      else:
        column_pattern_histogram[column_pattern] = 1
    return column_pattern_histogram


def get_contrajogos_as_dezenas_down_from(concurso, depth):
  if depth > concurso.nDoConc:
    return None
  pickled = ConcursosHistoryPickledStorage(read_as_id=None, upper_nDoConc=concurso.nDoConc)
  jogos_dezenas_list = pickled.read_or_create()
  if len(jogos_dezenas_list) > depth:
    offset = len(jogos_dezenas_list) - depth
    jogos_dezenas_list = jogos_dezenas_list[offset:]
  return jogos_dezenas_list


def adhoc_test():
  '''
  histreader = HistoryReader()  
  all_jogos = histreader.read(READ_CONCHIST_AS_2D_ORDERED_MATRIX)
  '''
  # blob = ConcursosHistoryPickledStorage(read_as_id=READ_CONCHIST_AS_TIMEONWARDS_NONORDERED_INTS)
  blob = ConcursosHistoryPickledStorage(read_as_id=READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS, upper_nDoConc=1001)
  all_jogos = blob.read_or_create()
  for i, jogo in enumerate(all_jogos):
    print i+1, jogo

import unittest
class MyTest(unittest.TestCase):

  def test_equality_of_both_blob_and_db(self):
    slider = ConcursoHTML()
    concursos_db = slider.get_all_concursos()
    pickled = ConcursosHistoryPickledStorage(read_as_id=READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS)
    pickled.read_or_create_not_returning_list()
    # repeat it, so that a blob will be read from
    pickled = ConcursosHistoryPickledStorage(read_as_id=READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS)
    concursos_blob = pickled.read_or_create()
    for i, concurso in enumerate(concursos_db):
      # get_dezenas() as a numpy array
      dezenas_db = numpy.array(concurso.get_dezenas())
      dezenas_blob = concursos_blob[i]
      self.assertEqual(dezenas_blob.all(), dezenas_db.all())  

  def test_get_contrajogos_as_dezenas_down_from(self):
    slider = ConcursoHTML()
    last_concurso = slider.get_last_concurso()
    jogos_dezenas_list = get_contrajogos_as_dezenas_down_from(last_concurso, last_concurso.nDoConc - 1)
    for i, jogo_as_dezenas in enumerate(jogos_dezenas_list):
      nDoConc = i+1
      concurso = slider.get_concurso_by_nDoConc(nDoConc)
      concurso_numpy_dezenas = numpy.array(concurso.get_dezenas())
      self.assertEqual(jogo_as_dezenas.all(), concurso_numpy_dezenas.all(), ' jogo_as_dezenas & concurso_numpy_dezenas SHOULD BE EQUAL')


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
