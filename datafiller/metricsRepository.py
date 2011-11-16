#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
import unittest
'''
Created on 15/11/2011
@author: friend


'''
def cleanUpRepeatsAndPutInOrder(numbers):
  if type(numbers) not in [list, tuple]:
    raise TypeError, 'numbers ust be a list or tuple as passed-in parameters to cleanUpRepeatsAndPutInOrder()'
  numbers = numbers.sort()
  index = 0
  while 1:
    number = numbers[index]
    if index >= len(numbers) - 1:
      break
    nextNumber = numbers[index + 1]
    if number == nextNumber:
      del numbers[index+1]
      continue
    index += 1
  return numbers


def iguaisComOAnterior(concurso, concursoAnterior, DO_REPEAT_CLEAN_UP=False):
  '''
  Steps:
  1st) check type conformity
  2nd) do a DO_REPEAT_CLEAN_UP if "it's asked" via passed-in param DO_REPEAT_CLEAN_UP
  3rd) count equals and return it 
  '''
  if type(concurso) not in [list, tuple]:
    raise TypeError, 'concurso and must be a list or tuple as passed-in parameters to iguaisComOAnterior()'
  if type(concursoAnterior) not in [list, tuple]:
    raise TypeError, 'concursoAnterior must be a list or tuple as passed-in parameters to iguaisComOAnterior()'
  if DO_REPEAT_CLEAN_UP:
    concurso = cleanUpRepeatsAndPutInOrder(concurso)
    concursoAnterior = cleanUpRepeatsAndPutInOrder(concursoAnterior)
  nDeIguais = 0
  for dezena in concurso:
    if dezena in concursoAnterior:
      nDeIguais += 1
  return nDeIguais

def coincsComOsNAnteriores(concurso, concursosAnteriores, nAnteriores):
  '''
  Steps:
  1st) check type conformity
  2nd) check size of concursosAnteriores that must be equal to nAnteriores
  3rd) reduce problem to its elements, ie loop through concursosAnteriores and invoke iguaisComOAnterior  
  '''
  if type(concursosAnteriores) not in [list, tuple]:
    raise TypeError, 'concursosAnteriores and must be a list or tuple as passed-in parameters to iguaisComOsNAnteriores()'
  if len(concursosAnteriores) != nAnteriores:
    raise IndexError, 'concursosAnteriores has a size = %d which is different from nAnteriores' %(len(concursosAnteriores), nAnteriores)
  for concursoAnterior in concursosAnteriores:
    iguaisComOAnterior(concurso, concursoAnterior)    

def coincsComOs3Anteriores(concurso, concursosAnteriores):
  '''
  Steps:
  1st) dispatch "problem" to coincsComOsNAnteriores setting nAnteriores to 3
  '''
  return coincsComOsNAnteriores(concurso, concursosAnteriores, nAnteriores=3) 

def coincsComOs7Anteriores(concurso, concursosAnteriores):
  '''
  Steps:
  1st) dispatch "problem" to coincsComOsNAnteriores setting nAnteriores to 7
  '''
  return coincsComOsNAnteriores(concurso, concursosAnteriores, nAnteriores=7) 

    
def parParImparImpar(concurso, concursos):
  pass

def rem2pattern(concurso, concursos):
  pass

def rem3pattern(concurso, concursos):
  pass

def rem5pattern(concurso, concursos):
  pass

def rem6pattern(concurso, concursos):
  pass

def colpattern(concurso, concursos):
  pass

def ocorrenciasDeCadaDezena(concurso, concursos):
  pass

def posAnteriorDeOcorrenciaDeCadaDezena(concurso, concursos):
  pass

def iguaisMediaComPassado(concurso, concursos):
  pass

def maxDeIguais(concurso, concursos):
  pass

def maxDeIguaisDistAo1oAnterior(concurso, concursos):
  pass

def maxDeIguaisOcorrencia(concurso, concursos):
  pass

def til4pattern(concurso, concursos):
  pass

def til5pattern(concurso, concursos):
  pass

def til6pattern(concurso, concursos):
  pass

def til10pattern(concurso, concursos):
  pass

def soma(concurso, concursos):
  pass

def soma3(concurso, concursos):
  pass

def soma7(concurso, concursos):
  pass

def soma15(concurso, concursos):
  pass

def avg(concurso, concursos):
  pass

def std(concurso, concursos):
  pass

def pathway(concurso, concursos):
  pass

def allpaths(concurso, concursos):
  pass

def binDecReprSomaDe1s(concurso, concursos):
  pass

def lgiDist(concurso, concursos):
  pass


