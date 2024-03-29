#!/usr/bin/env python3
"""
gen/backsimulators/backsimulator.py
  The idea of a backsimulator is to compare past results with a strategy of metrics that generate combinations.

For example, suppose one delimitates a strategy defined by metrics such as:
  - all games with such and such metric x (even_numbers, columnpatters, rowpatterns, graphshapes etc.)
  - all games with such and such historic metric y (til-frequencies, depth-repeats, maxacertos_backwards)

With such a definition, a backsimulator might go looking for past 'concursos' and compare them with the 'filter' above,
  giving statistical results as to 'how far' such combinations may get close to, if anywhere,
  as it's previously expected for the whole 'thing' to be random.

---------
Notice: for the time being (Fev 2024) no backsimulator in this system (and package) is completed or fully functional,
        ie, working is ongoing, maybe a bit slowly...
---------

# numpy, os, pickle, sys
"""
from fs.jogosfs import jogos_functions
from models.Files.ReadConcursosHistory import ConcursosHistoryMetrics  # ConcursosHistoryPickledStorage
from models.Concursos.concurso_extended import ConcursoExt


class Analyzer(object):
  
  def __init__(self, concurso):
    self.concurso = concurso
    self.n_conc  = self.concurso.n_conc
    self.jogo     = concurso.get_dezenas()
    self.jogo_in_orig_order = concurso.get_dezenas_in_orig_order()
    
  def run(self):
    scrmsg = 'Running games_before_concurso'
    print(scrmsg)
    games_before_concurso = ConcursosHistoryMetrics(read_as_id=None, upper_nDoConc=self.n_conc - 1)
    scrmsg = 'Running impares_histogram'
    print(scrmsg)
    self.impares_histogram = games_before_concurso.find_impares_histogram_for_games()
    scrmsg = 'Running impares_histogram'
    print(scrmsg)
    print 'Running sum_histogram'
    self.sum_histogram       = games_before_concurso.find_sum_histogram_for_games()
    print 'Running line_pattern_dict'
    self.line_pattern_dict   = games_before_concurso.find_line_pattern_histogram_games()
    print 'Running column_pattern_dict'
    self.column_pattern_dict = games_before_concurso.find_column_pattern_histogram_games()
    
  def report(self):
    scrmsg = 'Reporting impares_histogram'
    print(scrmsg)
    print(self.impares_histogram)
    print('Concurso After', self.concurso.n_conc, self.concurso.get_dezenas())
    n_impares = jogos_functions.get_n_impares(self.concurso.get_dezenas())
    print('n_impares', n_impares)
    print('Reporting sum_histogram')
    print(self.sum_histogram)
    print('Concurso After', self.concurso.n_conc, self.concurso.get_dezenas())
    print('Soma', sum(self.concurso.get_dezenas()))
    print('Reporting line_pattern_dict')
    print(self.line_pattern_dict)
    print( 'Concurso After', self.concurso.n_conc, self.concurso.get_dezenas())
    line_pattern = jogos_functions.get_line_pattern(self.concurso.get_dezenas())
    print('line_pattern', line_pattern)
    print('column_pattern_dict')
    print(self.column_pattern_dict)
    print('Concurso After', self.concurso.n_conc, self.concurso.get_dezenas())
    column_pattern = jogos_functions.get_column_pattern(self.concurso.get_dezenas())
    print('column_pattern', column_pattern)


def adhoc_test():
  slider = ConcursoExt()
  concurso = slider.get_last_concurso()
  analyzer = Analyzer(concurso)
  analyzer.run()
  analyzer.report()
  

if __name__ == '__main__':
  adhoc_test()
