#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 summary
 
 SELECT nDoConc, til4pattern, til5pattern, til6pattern, til10pattern
FROM `lf` where nDoConc > 100

'''
import CLClasses
import funcsForSql as fSql

def summary(jogosObj):
  attrs = ['nDoConc', 'arrecadacao', 'ganhadores15N', 'rateio15', 'ganhadores14N', 'rateio14']
  sqlPart =''
  for attr in attrs:
    sqlPart += '`%s`,' %(attr)
  sqlPart = sqlPart.rstrip(',')
  ultimoNDoConc = jogosObj.size()
  sql = '''SELECT %s FROM `%s`
WHERE nDoConc > %d ''' %(sqlPart, jogosObj.sqlTable, ultimoNDoConc - 10)
  db = fSql.DB()
  rows = db.doSelect(sql)
  print '='*40
  for attr in attrs:
    '''
    if type(attr) == Decimal:
      attr = int(attr/1000)
    '''
    print attr,
  print
  print '='*40
  for row in rows:
    for col in row:
      print col,
    print


def testSumm():
  jogosObj = CLClasses.getJogosObj('lf')
  summary(jogosObj)
  
if __name__ == '__main__':
  testSumm()
