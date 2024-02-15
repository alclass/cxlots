#!/usr/bin/env python3
"""
fs/datefs/date_functions.py

"""
import datetime
week_days_dict = {'mon':0, 'tue':1, 'wed':2, 'thu':3, 'fri':4, 'sat':5, 'sun':6}


def get_weekday_dif(week_day2, week_day1):
  """
  dif = wd2 - wd1
  """
  if type(week_day2) != int and type(week_day2) == str:
    try:
      week_day2 = week_days_dict[week_day2]
    except KeyError:
      return None
  if type(week_day1) != int and type(week_day1) == str:
    try:
      week_day1 = week_days_dict[week_day1]
    except KeyError:
      return None
  if week_day2 == week_day1:
    return 0
  dif = week_day2 - week_day1
  if dif < 0:
    ajustedDif = 6 + dif + 1
    return ajustedDif
  return dif


def transform_bar_ddmmyyyy_date_into_datetime(date_to_translate):
  if len(date_to_translate) != 10:
    return None
  if date_to_translate[2] != '/':
    return None
  if date_to_translate[5] != '/':
    return None
  pp = date_to_translate.split('/')
  year = int(pp[2])
  month = int(pp[1])
  day = int(pp[0])
  date = datetime.date(year, month, day)
  return date


def get_date_from_string(line):
  if line.endswith('\n'):
    line = line.rstrip('\n')
  date_portion = line
  time_portion = None
  if line.find(' ') > -1:
    pp = line.split(' ')
    date_portion = pp[0]
    time_portion = pp[1]
  pp = date_portion.split('-')
  year  = int(pp[0])
  month = int(pp[1])
  day   = int(pp[2])
  if not time_portion:
    dateTime = datetime.datetime(year, month, day, 0, 0, 0, 0)
    return dateTime
  pos = time_portion.find('.')
  msec = 0
  if pos > -1:
    msec = int(time_portion[pos+1:])
    time_portion = time_portion[:pos]
  pp = time_portion.split(':')
  hour   = int(pp[0])
  minute = int(pp[1])
  second = int(pp[2])
  dateTime = datetime.datetime(year, month, day, hour, minute, second, msec)
  return dateTime


if __name__ == '__main__':
  pass
