#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 14/11/2011

@author: friend
'''
import sqlite3, sys
a=1
import ClassConcursoEtc as conc
'''

megasena Metrics

  `iguaisComOAnterior`
  param: concurso, concurso[current - 1]

  `coincsComOs3Anteriores`
  param: concurso, concurso[current - 3, current - 1]

  `maxDeIguais`
  param: concurso, concurso[0, current - 1]

  `maxDeIguaisDistAo1o`
  param: concurso, concurso[0, current - 1]

  `maxDeIguaisOcorrencia`
*  param: concurso, concurso[0, current - 1]

  `iguaisMediaComPassado` 

  `rem2pattern` 
  param: concurso
  1-digit: values from 0 to 6 (0 means no even numbers / all 6 are odd, 6 all 6 are even) 
 eg suppose thisConcurso = 1,2,3,4,5,6
 the function rem2pattern(thisConcurso) should return 3, ie there are 3 (2,4,and 6) even numbers 

  `parParImparImpar`
  param: concurso
tricky one
a teen has two digits: parPar is when the two digits are even
 imparImpar is when the two digits are odd
 eg suppose 1,2,3,4,5,6
 then 02,04,and06 are parPar, there is no imparImpar in the above example, for all have the zero (even) digit


  `rem3pattern` 
  param: concurso
  1-digit: values from 0 to 6 (0 means no even numbers / all 6 are odd, 6 all 6 are even) 
 eg suppose thisConcurso = 1,2,3,4,5,6
 the function rem3pattern(thisConcurso) should return 2, ie there are 3 (3 and 6) multiple-of-3 numbers 

  `rem5pattern` 
idem as previous one changing modulo 3 to modulo 5

  `rem6pattern` 
idem as previous one changing modulo 5 to modulo 6

  `colpattern`
  param: concurso
  10-digit result: 
 eg suppose thisConcurso = 1,2,3,4,5,6
 the function colpattern(thisConcurso) should return 1111110000 

  
  `til4pattern` 
  param: concurso, concursos[0, current - 1]

Meaning of TIL<n>:

til4 divides all dezenas through its quartils. The quartil is a frequency distribution picking up each fourth of occurrences

This means that we'll separate the 25% less occurring dezenas to set 0
Then the dezenas that have occurred from 25% + 1 occurrences to 50% to set 1
Then the dezenas that have occurred from 50% + 1 occurrences to 75% to set 2
Finally the dezenas that have occurred above 75% + 1 occurrences set 3

 eg suppose thisConcurso = 10,20,30,40,50,60
and suppose also that:
10 -> quartil (set) 0
20 -> quartil (set) 3
30 -> quartil (set) 1
40 -> quartil (set) 0
50 -> quartil (set) 2
60 -> quartil (set) 1

According to such configuration, the function til4(thisConcurso) should return '031021' with til4pattern '2211'

  `til5pattern` 
idem to previous one, but instead of quartils, quintils are used, ie, occurrences are divided into 5 sets

  `til6pattern`

  `til10pattern`

  `consecEnc`,
  param: concurso
  10-digit result: 
 eg1 suppose thisConcurso = 1,2,3,4,5,6
 the function colpattern(thisConcurso) should return 5 ie there 5 numbers that are consecutives to its individual previous ones 
 
 eg2 suppose thisConcurso = 10,20,30,40,50,60
 the function colpattern(thisConcurso) should return 0 for there are no consecutives 
 
  `soma` 
  param: concurso
  It sums up all dezenas
 eg1 suppose thisConcurso = 1,2,3,4,5,6
 the function colpattern(thisConcurso) should return 1+2+3+4+5+6 ie 21


  `soma3` 
  param: concurso, concursos[-4, -1]
  It sums up all dezenas in current concurso plus three before

  `soma7`
  param: concurso, concursos[-7, -1]
  It sums up all dezenas in current concurso plus seven before

  `soma15`
idem to the previous two


  `avg`
  param: concurso
  It calculates average from the dezenas

  `std`
  param: concurso
  It calculates standard deviation from the dezenas

  `pathway`,

  `allpaths`

  `binDecReprSomaDe1s`
  param: concurso
  The binary decimal representation Soma de 1's

  `lgiDist`
  param: concurso
  The LexicoGraphical representation of concurso, ie, it's sequence number that uniquely identifies concurso with all possible combinations
  
'''

iguaisComOAnterior,coincsComOs3Anteriores,coincsComOs7Anteriores,parParImparImpar,rem2pattern,rem3pattern,rem5pattern,rem6pattern,colpattern,ocorrenciasDeCadaDezena,posAnteriorDeOcorrenciaDeCadaDezena,iguaisMediaComPassado,maxDeIguais,maxDeIguaisDistAo1oAnterior,maxDeIguaisOcorrencia,til4pattern,til5pattern,til6pattern,til10pattern,soma,soma3,soma7,soma15,avg,std,pathway,allpaths,binDecReprSomaDe1s,lgiDist=None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None

metricsDict = { \
1:('iguaisComOAnterior',iguaisComOAnterior,'Calcula quantidade de dezenas coincidentes com o jogo anterior'), \
2:('coincsComOs3Anteriores',coincsComOs3Anteriores,'Calcula quantidade de dezenas coincidentes com os 3 jogosfs anteriores'), \
3:('coincsComOs7Anteriores',coincsComOs7Anteriores,'Calcula quantidade de dezenas coincidentes com os 3 jogosfs anteriores'), \
4:('parParImparImpar',parParImparImpar,'Calcula os números de dezenas par-par (ex. 22, 04, 60, 46 etc.) e ímpar-ímpar (ex. 33, 15, 01 etc.) e junta os dois dígitos de resultado ex. 1,2,3,4,5,6 -> 30, ou 3 par-par e 0 ímpar-ímpar'), \
5:('rem2pattern',rem2pattern,'Calcula a sequência par: exemplo: 15,21,22,30,55,60 gera 001101, ou seja, 0 é ímpar e 1 é par'), \
6:('rem3pattern',rem3pattern,'Calcula a sequência modulo-3: exemplo: 15,21,22,30,56,60 gera 001021, ou seja, 0,1 e 2 são os restos da dezena dividida por 3'), \
7:('rem5pattern',rem5pattern,'Calcula a sequência modulo-5: exemplo: 15,21,22,30,56,60 gera 012010, ou seja, 0 a 4 são os restos da dezena dividida por 5'), \
8:('rem6pattern',rem6pattern,'Calcula a sequência modulo-6: exemplo: 15,21,22,30,56,60 gera ..., ou seja, 0 a 5 são os restos da dezena dividida por 5'), \
9:('colpattern',colpattern,'Calcula a ocorrência por colunas numa sequência de 10 dígitos (10 colunas), ex. concurso 1,23,42,51,57,59 gera 2010001010 (2 representa duas dezenas na coluna 1 [01 e 51], 0 diz que não houve dezenas na coluna 2, 1 diz que houve uma dezena na coluna 3 [=23] e por aí vai'), \
10:('ocorrenciasDeCadaDezena',ocorrenciasDeCadaDezena,'Calcula quantidade de vezes cada dezena do concurso caiu no em concursos anteriores'), \
11:('posAnteriorDeOcorrenciaDeCadaDezena',posAnteriorDeOcorrenciaDeCadaDezena,'Informa para cada uma das dezenas sorteadas sua posição em frequência entre todos os concursos descontando seu próprio concurso'), \
12:('iguaisMediaComPassado',iguaisMediaComPassado,'VOID'), \
13:('maxDeIguais',maxDeIguais,'VOID DEPRECATED virou ocorrenciasDeCadaDezena'), \
14:('maxDeIguaisDistAo1oAnterior',maxDeIguaisDistAo1oAnterior,'VOID a se transformar em métrica geral'), \
15:('maxDeIguaisOcorrencia',maxDeIguaisOcorrencia,'VOID'), \
16:('til4pattern',til4pattern,''), \
17:('til5pattern',til5pattern,''), \
18:('til6pattern',til6pattern,''), \
19:('til10pattern',til10pattern,''), \
20:('soma',soma,''), \
21:('soma3',soma3,''), \
22:('soma7',soma7,''), \
23:('soma15',soma15,''), \
24:('avg',avg,''), \
25:('std',std,''), \
26:('pathway',pathway,''), \
27:('allpaths',allpaths,''), \
28:('binDecReprSomaDe1s',binDecReprSomaDe1s,''), \
29:('lgiDist',lgiDist,'') }


class Metrics():
  def __init__(self, concursos):
    self.concursos = concursos
    self.concursoCurrent = concursos[-1]
    self.resultsDict = {}
  def runMetrics(self, sqlStore=True, metricsCodes=[]):
    if metricsCodes==[]:
      metricsCodes = range(0, TOTAL_OF_METRICS - 1)
    for metricsCode in metricsCodes:
      name = metricsDict[metricsCode][0]
      func = metricsDict[metricsCode][1]
      result = func(self.concursoCurrent, self.concursos)
      self.resultsDict[name] = result
    if sqlStore:
      sqlInsertForMetrics(self.resultDict)
      
def processMetrics():
  concursos = sqlLayer.sqlSelect()
  for currentPos in range(0, len(concursos)):
    concursosUntilCurrentPos = concursos[0 : currentPos + 1]
    metrics = Metrics(concursosUntilCurrentPos)
    metrics.runMetrics(sqlStore=True, metricsCodes=[])
