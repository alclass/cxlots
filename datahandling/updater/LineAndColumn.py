#!/usr/bin/env python
#-*-coding:utf8-*-

#justAllocateSomeMemoryBeforeImporting = 1
  
class LineAndColumn(object):
  # singleton
  _instance = None
  patternsLinhaFoundDict = None
  patternsColunaFoundDict = None
  patternsLinhaNeverOccurred = None
  maxPatternLinhaRepeat = None
  maxPatternColunaRepeat = None
  
  def __new__(self, *args, **kargs):
    if self._instance is None: 
      self._instance = object.__new__(self, *args, **kargs)
    return self._instance
  
  def initLinColPatternObj(self):
    tri = getLinColPatternObj()
    self.patternsLinhaFoundDict, self.patternsColunaFoundDict, self.patternsLinhaNeverOccurred = tri[0],tri[1],tri[2]
    
    if self.patternsLinhaFoundDict == None:
      raise ValueError, 'patternsLinhaFoundDict continues to be None after have called init to it, ValueError raised.'
    patterns = self.patternsLinhaFoundDict.keys()
    patterns.sort()
    self.maxPatternLinhaRepeat = 0
    for pattern in patterns:
      if self.patternsLinhaFoundDict[pattern] > self.maxPatternLinhaRepeat:
        self.maxPatternLinhaRepeat = self.patternsLinhaFoundDict[pattern]
    
    if self.patternsColunaFoundDict == None:
      raise ValueError, 'patternsLinhaFoundDict continues to be None after have called init to it, ValueError raised.'
    patterns = self.patternsColunaFoundDict.keys()
    patterns.sort()
    self.maxPatternColunaRepeat = 0
    for pattern in patterns:
      if self.patternsColunaFoundDict[pattern] > self.maxPatternColunaRepeat:
        self.maxPatternColunaRepeat = self.patternsColunaFoundDict[pattern]
    
    if self.patternsLinhaNeverOccurred == None:
      raise ValueError, 'patternsLinhaFoundDict continues to be None after have called init to it.'
  
  def getPatternsLinhaFoundDict(self):
    if self.patternsLinhaFoundDict == None:
      self.initLinColPatternObj()
    return self.patternsLinhaFoundDict
    
  def getPatternsColunaFoundDict(self):
    if self.patternsColunaFoundDict == None:
      self.initLinColPatternObj()
    return self.patternsColunaFoundDict
  
  def getPatternsLinhaNeverOccurred(self):
    if self.patternsLinhaNeverOccurred == None:
      self.initLinColPatternObj()
    return self.patternsLinhaNeverOccurred
  
  def getMaxPatternLinhaRepeat(self):
    if self.maxPatternLinhaRepeat == None:
      self.initLinColPatternObj()
    return self.maxPatternLinhaRepeat
  
  def getMaxPatternColunaRepeat(self):
    if self.maxPatternColunaRepeat == None:
      self.initLinColPatternObj()
    return self.maxPatternColunaRepeat
    
  def __str__(self):
    outStr =  'This is the LinColPatternObj class singleton instance:\n'
    if self.patternsLinhaFoundDict == None:
      self.initLinColPatternObj()
      if self.patternsLinhaFoundDict == None:
        msg = 'A member of the LinColPatternObj instance (patternsLinhaFoundDict) continues to be None after have called init to it, ValueError raised.'
        raise ValueError, msg
    outStr += 'size of patternsLinhaFoundDict: %d\n' %(len(self.patternsLinhaFoundDict))
    outStr += 'size of patternsColunaFoundDict: %d\n' %(len(self.patternsColunaFoundDict))
    outStr += 'size of patternsLinhaNeverOccurred: %d\n' %(len(self.patternsLinhaNeverOccurred))
    return outStr
