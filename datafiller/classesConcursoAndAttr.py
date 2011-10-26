#!/usr/bin/env python
# -*- coding: utf-8 -*-

this_var_is_just_to_avoid_recursive_local_imports=1
import valueCheckers
import HTMLGrabber
del this_var_is_just_to_avoid_recursive_local_imports

class Attr(object):
  def __init__(self, name, value=None):
    self.name = name
    self.isInteger = False
    self.isCurrency = False
    self.isDate = False
    self.fillInIsCurrencyIsDateIsInteger()
    if value <> None:
      self.setAttr(value)
  def fillInIsCurrencyIsDateIsInteger(self):
    if self.name.lower().startswith('data'):
      self.isDate = True
      return
    for phrase in ['ganhadores', 'dezena']:
      if self.name.lower().startswith('dezena'):
        self.isInteger = True
        return
    for phrase in ['rateio', 'arrecadacao', 'estimativa', 'acumulado', 'valor']:
      if self.name.lower().startswith(phrase):
        attrObj.isCurrency = True
        return
    raise ValueError, "it could not determine whether it's currency, it's date or it's integer"
  def setAttr(self, value):
    if self.isInteger():
      if not valueCheckers.checkIfValueIsInteger(value):
        raise TypeError, 'type error having an integer'
    if attrObj.isCurrency():
      if valueCheckers.checkIfValueIsCurrency(value):
        raise TypeError, 'type error having a currency'
      value = valueCheckers.normalizeDate(value)
    self.value = value
  def putIntoParamListAttrValueInOrder(values):
    index = HTMLGrabber.megasenaFieldNames.index(self.name)
    if len(values) < index:
      values[index] = self.value
    else:
      raise IndexError, 'index error in putIntoParamListAttrValueInOrder(values)'
  def __str__(self):
    outStr = '(attr: %s = %s)' %(self.name, self.value)

class Concurso(object):
  def __init__(self, nDoConc):
    if valueCheckers.checkIfValueIsInteger(nDoConc):
      self.nDoConc = nDoConc
    else:
      raise ValueError, 'an integer was not given to Concurso (nDoConc)'
    self.values = []
  def addAttr(self, attrName, attrValue):
    attrObj = Attr(attrName, attrValue)
    attrObj.putIntoParamListAttrValueInOrder(self.values)
  def __str__(self):
    outStr = 'nDoConc = %d \n' %(self.nDoConc)
    for value in self.values:
      outStr += value + '; '
    outStr = outStr[ : -2]
    return outStr 
    
