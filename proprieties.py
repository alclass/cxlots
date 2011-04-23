#!/usr/bin/env python
# -*- coding: utf-8 -*-

a=1
import HistoricoUpdater as huc

def getDbFieldsFor(tipoJogo):
  dbFields={'lf':'''Concurso,nDoConc
Data Sorteio,date
Bola1,
Bola2,
Bola3,
Bola4,
Bola5,
Bola6,
Bola7,
Bola8,
Bola9,
Bola10,
Bola11,
Bola12,
Bola13,
Bola14,
Bola15,
Arrecadacao_Total,arrecadacao
Ganhadores_15_Números,ganhadores15N
Ganhadores_14_Números,ganhadores14N
Ganhadores_13_Números,ganhadores13N
Ganhadores_12_Números,ganhadores12N
Ganhadores_11_Números,ganhadores11N
Valor_Rateio_15_Números,rateio15
Valor_Rateio_14_Números,rateio14
Valor_Rateio_13_Números,
Valor_Rateio_12_Números,
Valor_Rateio_11_Números,
Acumulado_15_Números,premioAcum15
Estimativa_Preimo,premioEstimado''',
'ms':'''Concurso,nDoConc
Data Sorteio,date
1ª Dezena,
2ª Dezena,
3ª Dezena,
4ª Dezena,
5ª Dezena,
6ª Dezena,
Arrecadacao_Total,arrecadacao
Ganhadores_Sena,ganhadoresSena
Rateio_Sena,rateioSena
Ganhadores_Quina,ganhadoresQuina
Rateio_Quina,rateioQuina
Ganhadores_Quadra,ganhadoresQuadra
Rateio_Quadra,rateioQuadra
Acumulado,foiAcumulado
Valor_Acumulado,acumulado
Estimativa_Prêmio,premioEstimado
Acumulado_Natal,premioAcumNatal'''}
  dbFieldStrs = dbFields[tipoJogo]
  return getFieldNames(dbFieldStrs)

def getFieldNames(fieldsStr):
  fields = fieldsStr.split('\n')
  dbFields = []
  for line in fields:
    field = None
    if line.find(',') > -1:
      field = line.split(',')[-1]
    dbFields.append(field)
  return dbFields

def testDbFieldsClass():
  for tipoJogo in ['lf','ms']:
    print '='*40
    obj = huc.DbFields(tipoJogo)
    print 'obj.size()', obj.size()
    print 'obj.fields()', obj.fields()
    for i in range(obj.size()):
      print obj.field(i),
    print
    print '='*40

if __name__ == '__main__':
  pass
  testDbFieldsClass()
