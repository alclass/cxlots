#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime


weekDaysDict = {'mon':0,'tue':1,'wed':2,'thu':3,'fri':4,'sat':5,'sun':6}
def getWeekdayDif(weekDay2, weekDay1):
  '''
  dif = wd2 - wd1
  '''
  if type(weekDay2) <> int and type(weekDay2) == str:
    try:
      weekDay2 = weekDaysDict[weekDay2]
    except KeyError:
      return None
  if type(weekDay1) <> int and type(weekDay1) == str:
    try:
      weekDay1 = weekDaysDict[weekDay1]
    except KeyError:
      return None
  if weekDay2 == weekDay1:
    return 0
  dif = weekDay2 - weekDay1
  if dif < 0:
    ajustedDif = 6 + dif + 1
    return ajustedDif
  return dif

def transformBarDDMMYYYYDateIntoDatetime(dateToTranslate):
  if len(dateToTranslate) <> 10:
    return None
  if dateToTranslate[2] <> '/':
    return None
  if dateToTranslate[5] <> '/':
    return None
  pp = dateToTranslate.split('/')
  year  = int(pp[2])
  month = int(pp[1])
  day   = int(pp[0])
  date = datetime.date(year, month, day)
  return date

def getDateFromString(line):
  if line.endswith('\n'):
    line = line.rstrip('\n')
  datePortion = line
  timePortion = None
  if line.find(' ') > -1:
    pp = line.split(' ')
    datePortion = pp[0]
    timePortion = pp[1]
  pp = datePortion.split('-')
  year  = int(pp[0])
  month = int(pp[1])
  day   = int(pp[2])
  if not timePortion:
    dateTime = datetime.datetime(year, month, day, 0, 0, 0, 0)
    return dateTime
  pos = timePortion.find('.')
  msec = 0
  if pos > -1:
    msec = int(timePortion[pos+1:])
    timePortion = timePortion[:pos]
  pp = timePortion.split(':')
  hour   = int(pp[0])
  minute = int(pp[1])
  second = int(pp[2])
  dateTime = datetime.datetime(year, month, day, hour, minute, second, msec)
  return dateTime


if __name__ == '__main__':
  pass
