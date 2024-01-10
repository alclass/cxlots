#!/usr/bin/env python3
"""

"""
#import datetime #,
from bs4 import BeautifulSoup as bF
import sys
import local_settings as ls
from models.Concursos.ConcursoSlider import ConcursoSlider
import models.Concursos.ConcursoHTML as conc
import fs.db_sql.FieldsAndTypes as fat
# import models.JogoSlider.JogoSlider
#from models.ConcursoSlider import ConcursoSlider


class ConcursoHTMLScraper(object):

  def __init__(self, html_data_filename=None):
    self.html_data_filename = html_data_filename
    if self.html_data_filename is None:
      self.html_data_filename = ls.MS_DATAFILE_ABSPATH
    self.concursoSlider = ConcursoSlider(conc.ConcursoHTML)
    self.process_flow()
    self.print_concursos()
    self.save_concursos_in_db()
    self.bs_obj = None
    self.concursos = None

  def process_flow(self):    
    self.parse_to_data_stru()
    self.convert_concursos_fieldtypes()

  def parse_to_data_stru(self):
    self.create_soup_obj()
    if self.bs_obj is not None:
      self.concursos = process_rows_across_table(self.bs_obj)

  def convert_concursos_fieldtypes(self):
    for concurso in self.concursos:
      concurso.transport_dict_into_attrs()

  def create_soup_obj(self):
    """
    Because of Portuguese accents in headers and in SIM/NÃO row values
      and the fact that the HTML is probably iso-8859-1 (Latin1) instead of UTF-8
    the unicode function raises UnicodeDecodeError
      if optional parameter errors is not set either to 'ignore' or 'replace'
      we chose 'ignore' because we only read the first character of field acumuladoSimNao,
      so it's either 'S' or 'N' coinciding with its ASCII/UTF-8 codes
    """
    html_text = open(self.html_data_filename, encoding='utf-8').read()
    self.bs_obj = bF.BeautifulSoup(html_text)

  def print_concursos(self):      
    outStr = '\n' + '='*30 + '\n'
    outStr += '============ print_concursos() ============'
    outStr += '\n' + '='*30 + '\n'
    print(outStr)
    for concurso in self.concursos:
      n_do_conc = concurso['n_do_conc']
      if n_do_conc is None:
        n_do_conc = -1
      print(n_do_conc, concurso)

  def save_concursos_in_db(self):
    print( '========== save_concursos_in_db() ============')
    total_db_concursos = self.concursoSlider.get_total_concursos()
    total_html_concursos = len(self.concursos)
    print('total_db_concursos', total_db_concursos)
    print('total_html_concursos', total_html_concursos)
    if total_html_concursos <= total_db_concursos:
      return
    concursos_to_insert = []
    for n_do_conc in range(total_db_concursos + 1, total_html_concursos + 1):
      index = n_do_conc - 1
      concurso = self.concursos[index]
      expected_n_do_conc = concurso['n_do_conc']
      print('expected_n_do_conc', expected_n_do_conc)
      if expected_n_do_conc is None:
        print('Stopping expected_n_do_conc == None.')
        sys.exit(0)
      concurso.transport_dict_into_attrs()
      concursos_to_insert.append(concurso)
    self.concursoSlider.bulk_insert(concursos_to_insert)

  def __str__(self):
    out_str = '\n' + '='*30 + '\n'
    out_str += '============ Concursos ============'
    out_str += '\n' + '='*30 + '\n'
    for concurso in self.concursos:
      out_str += str(concurso)
      out_str += '\n' + '='*30 + '\n'
    out_str += 'Total: %d' % len(self.concursos)
    return out_str


def process_columns_across_row(tr, n_of_the_line=0):
  n_of_the_line += 1
  tds = tr.fetch('td')
  column_tracker, row = 1, {}
  for td in tds:
    # this typecast is to avoid propagation of type(value)=<class 'BeautifulSoup.NavigableString'>
    value = str(td.string)
    fieldname = fat.allowedFieldNamesInOriginalOrder[column_tracker - 1]
    row[fieldname] = value
    column_tracker += 1
  # print 'row', row
  concurso = conc.convertRowListToHTMLConcursoObj(row)
  return concurso


def process_rows_across_table(bs_obj):
  # 1st level
  trs = bs_obj.fetch('tr')
  n_of_the_line, concursos = 1, []
  for tr in trs:
    # 2nd level
    concurso = process_columns_across_row(tr, n_of_the_line)
    if concurso is not None:
      concursos.append(concurso)
      n_of_the_line += 1
  return concursos


def test_grabber():
  ConcursoHTMLScraper()


def process():
  scraper = ConcursoHTMLScraper()
  scraper.process_flow()


def adhoc_test():
  test_grabber()


if __name__ == '__main__':
  process()
