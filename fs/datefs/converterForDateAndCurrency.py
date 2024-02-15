#!/usr/bin/env python3
"""
commands/updates/db_update_concdates.py
  Updates the MS db-table in column 'concdates'

Created on 12/11/2011
@author: Luiz Lewis
"""
import datetime


def convertToFloatAMoneyCurrencyNotInEnglishFormat(value):
  if type(value) == unicode:
    # in fact, it's expected a number with comma as decimal place separator and dot/point as thousands separator
    value = str(value)
  if type(value) != str:
    '''
    The two cases below are useful when values are coming from the database and are not str
    '''
    if type(value) == float:
      return value
    if type(value) == int:
      return float(value)
  if value.find(',') > -1:
    if value.find('.') > -1:
      value = value.replace('.', '')
    value = value.replace(',', '.')
    return float(value)
  elif value.find('.') > -1:
    value = value.replace('.', '')
    return float(value)
  try:
    return float(value)
  except TypeError:
    pass
  return None
  
def convertToDdMmYyyyDatetimeDate(value):
  #print ' INSIDE convertToDatetimeDate(value=%s), type(value)=%s' %(value, type(value))
  if type(value) != str:
    return None
  pp = []
  for separator in ['/', '-']:
    if value.find(separator) > -1:
      pp = value.split(separator)
      break
  if len(pp) != 3 :
    return None
  dia = int(pp[0])
  mes = int(pp[1])
  ano = int(pp[2])
  dateObj = datetime.date(ano, mes, dia)
  #print ' INSIDE convertToDatetimeDate ==>> dateObj = %s' %str(dateObj)
  return dateObj

def convertYyyyMmDDToDatetimeDate(value):
  #print ' INSIDE convertToDatetimeDate(value=%s), type(value)=%s' %(value, type(value))
  if type(value) != str:
    return None
  pp = []
  for separator in ['/', '-']:
    if value.find(separator) > -1:
      pp = value.split(separator)
      break
  if len(pp) != 3 :
    return None
  dia = int(pp[2])
  mes = int(pp[1])
  ano = int(pp[0])
  dateObj = datetime.date(ano, mes, dia)
  #print ' INSIDE convertToDatetimeDate ==>> dateObj = %s' %str(dateObj)
  return dateObj


def convertToDatetimeDate(dateStr, dateStrFormat='DD-MM-YYYY'):
  if dateStrFormat == 'YYYY-MM-DD':
    return convertYyyyMmDDToDatetimeDate(dateStr)
  elif dateStrFormat == 'DD-MM-YYYY':
    return convertToDdMmYyyyDatetimeDate(dateStr)
  # it's the else below, ie, an option not covered above
  return None
