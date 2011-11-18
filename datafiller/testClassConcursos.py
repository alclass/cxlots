#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import datetime, sys
'''
Created on 18/11/2011

@author: friend
'''


a=1
import ClassConcursoEtc as conc

concurso = conc.Concurso()
for i in range(1,7):
  fieldname = 'dezena%d' %i
  concurso[fieldname]=i
print 'concurso', concurso
print 'concurso.getDezenas()', concurso.getDezenas()

