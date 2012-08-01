#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
'''

Idea to what should be generated and pasted to the metricsgenerator module:

metricsDict = { \ 
1:('iguaisComOAnterior',iguaisComOAnterior,'Calcula quantidade de dezenas coincidentes com o jogo anterior' \ 
2:('coincsComOs3Anteriores',coincsComOs3Anteriores,'Calcula quantidade de dezenas coincidentes com os 3 jogos anteriores' \ 
3:('coincsComOs7Anteriores',coincsComOs7Anteriores,'Calcula quantidade...
  
  
  Running this script it's seen
'''

metricsNamesStr = '''iguaisComOAnterior :: Calcula quantidade de dezenas coincidentes com o jogo anterior 
coincsComOs3Anteriores :: Calcula quantidade de dezenas coincidentes com os 3 jogos anteriores
coincsComOs7Anteriores :: Calcula quantidade de dezenas coincidentes com os 3 jogos anteriores
parParImparImpar :: Calcula os números de dezenas par-par (ex. 22, 04, 60, 46 etc.) e ímpar-ímpar (ex. 33, 15, 01 etc.) e junta os dois dígitos de resultado ex. 1,2,3,4,5,6 -> 30, ou 3 par-par e 0 ímpar-ímpar
rem2pattern :: Calcula a sequência par: exemplo: 15,21,22,30,55,60 gera 001101, ou seja, 0 é ímpar e 1 é par
rem3pattern :: Calcula a sequência modulo-3: exemplo: 15,21,22,30,56,60 gera 001021, ou seja, 0,1 e 2 são os restos da dezena dividida por 3
rem5pattern :: Calcula a sequência modulo-5: exemplo: 15,21,22,30,56,60 gera 012010, ou seja, 0 a 4 são os restos da dezena dividida por 5 
rem6pattern :: Calcula a sequência modulo-6: exemplo: 15,21,22,30,56,60 gera ..., ou seja, 0 a 5 são os restos da dezena dividida por 5 
colpattern :: Calcula a ocorrência por colunas numa sequência de 10 dígitos (10 colunas), ex. concurso 1,23,42,51,57,59 gera 2010001010 (2 representa duas dezenas na coluna 1 [01 e 51], 0 diz que não houve dezenas na coluna 2, 1 diz que houve uma dezena na coluna 3 [=23] e por aí vai 
ocorrenciasDeCadaDezena :: Calcula quantidade de vezes cada dezena do concurso caiu no em concursos anteriores  
posAnteriorDeOcorrenciaDeCadaDezena :: Informa para cada uma das dezenas sorteadas sua posição em frequência entre todos os concursos descontando seu próprio concurso  
iguaisMediaComPassado :: VOID
maxDeIguais :: VOID DEPRECATED virou ocorrenciasDeCadaDezena  
maxDeIguaisDistAo1oAnterior :: VOID a se transformar em métrica geral
maxDeIguaisOcorrencia :: VOID 
til4pattern :: 
til5pattern :: 
til6pattern :: 
til10pattern :: 
soma :: 
soma3  :: 
soma7  :: 
soma15 :: 
avg :: 
std :: 
pathway :: 
allpaths :: 
binDecReprSomaDe1s :: 
lgiDist :: '''

names = []; namesDescriptionsDict = {}
def printDict():
  lines = metricsNamesStr.split('\n')
  pySourceCode = 'metricsDict = { \\\n' ; seqNumber = 0
  for line in lines:
    name, description = line.split('::')
    name = name.strip()
    names.append(name)
    description = description.strip()
    namesDescriptionsDict[name] = description 
    seqNumber += 1
    pySourceCode += "%(seqNumber)d:('%(name)s',metr.%(name)s,'%(description)s'), \\\n" %{'seqNumber':seqNumber, 'name':name,'description':description}
  pySourceCode = pySourceCode[ : - len(', \\\n')]
  pySourceCode += '  }'
  return pySourceCode

def generateNames():
  justForTheSideEffectOfFillingNamesList = printDict()
  del justForTheSideEffectOfFillingNamesList
  sourcecode = ''
  for name in names:
    description = namesDescriptionsDict[name] 
    sourcecode += '''def %(name)s(concurso, concursos):
\t"%(description)s"    
\tpass\n\n''' %{'name':name, 'description':description}
  #sourcecode = sourcecode[:-1]
  print sourcecode

def generatePrint(printStr='dict'):
  if printStr == 'dict':
    print printDict()

def process():
  if len(sys.argv) > 1:
    param = sys.argv[1]
    if param == 'dict':
      generatePrint()
    elif param == 'names':
      generateNames()

if __name__ == '__main__':
  process()
