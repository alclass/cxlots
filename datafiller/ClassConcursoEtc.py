#!/usr/bin/env python
# -*- coding: utf-8 -*-


a=1
import ClassAttributeEtc as cae

class Concurso():
  def __init__(self, nDoConc):
    self.concursoDict = {}
    try:
      self.concursoDict['nDoConcurso'] = int(nDoConc)
    except ValueError, valueErrorExceptionObj:
      print valueErrorExceptionObj, 'nDoConc is not int'
      print 'Halting'
      sys.exit(0)
  def __setitem__(self, fieldname, value):
    shouldBeType = cae.getFieldType(fieldname)
    if type(value) != shouldBeType:
      raise TypeError, 'type error in __setitem__ attrName=%s and attrValue=%s ' %(fieldname, str(value))
    self.concursoDict[fieldname] = value
  def __getitem__(self, fieldname):
    if fieldname in self.concursoDict.keys():
      return self.concursoDict[fieldname]
    return None
  def __str__(self):
    outStr = 'nDoConc = %d \n' %(self.concursoDict['nDoConcurso'])
    for fieldname in self.concursoDict.keys():
      outStr += str(self.concursoDict[fieldname]) + '; '
    outStr = outStr[ : -2]
    return outStr 

def test():
  c = Concurso(1)
  c['dezena1']=25
  print c
  
if __name__ == '__main__':
  test()