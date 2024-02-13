#!/usr/bin/env python3
"""
commands/updates/db_update_lgi_lexicographical_indices.py
  Updates the MS db-table in column 'lexicographicalindex'

"""


def transf_6number12charstr_into_dozenlist(number6char12str):
  """
  Transforms a 6-number 12-character string into an int number list
  If transformation raises TypeError or ValueError, returns empty
  Example input/output:
    input:
      number6char12str = '174915333923'
    output:
      dezenas = [17, 49, 15, 33, 39, 23]
  """
  try:
    dezenas = [int(number6char12str[i:i + 2]) for i in range(0, 11, 2)]
    return dezenas
  except (TypeError, ValueError):
    pass
  return []


def adhoctest():
  number6char12str = '174915333923'
  expected_dezenas = [17, 49, 15, 33, 39, 23]
  returned_dezenas = transf_6number12charstr_into_dozenlist(number6char12str)
  scrmsg = f"nstr={number6char12str}, expected={expected_dezenas}, returned={returned_dezenas}"
  print(scrmsg)


def process():
  pass


if __name__ == '__main__':
  adhoctest()
  process()

