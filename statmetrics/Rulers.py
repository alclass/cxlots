#!/usr/bin/env python
# -*- coding: utf-8 -*-


a=1
import funcs
import Checker
Ruler = Checker.Checker

'''
CTRL_CONSECS    :: RulerConsecs(Ruler)
CTRL_RADII      :: RulerRadii(Ruler)
CTRL_REMAINDERS :: RulerRemainders(Ruler)
CTRL_REPEATS    :: RulerRepeat(Ruler)
CTRL_SOMA_N     :: RulerSomaN(Ruler)
CTRL_TILS       :: RulerTil(Ruler)
'''

class RulerSomaN(Ruler):
  '''
  soma, soma2 a somaN
  Depends on Chooser class.
    Parameters are "estimated" from heuristics
    that take into account both soma's probability 
    as well as probability derived from direction vector
  '''

  def __init__(self, jogosObj):
    Ruler.__init__(self, jogosObj)
    middlename   = 'rulersoman'
    self.logFile = funcs.mountLogFile(middlename, self.jogosObj)


    #self.limits = [(0,1),(1,4),(4,7),(0,5),(1,4)]
    # self.limits = (25,31) # Coincs3Anteriores
    self.limits = (540,610)

  def low(self):
    return self.limits[0]
  
  def high(self):
    return self.limits[1]

  def somaN(self, soma3):
    if soma3 < self.limitsSoma3[0]:
      return False
    if soma3 > self.limitsSoma3[1]:
      return False
    return True


class RulerTil(Ruler):

  def __init__(self, jogosObj):
    Ruler.__init__(self, jogosObj)
    self.limits = [(0,1),(1,4),(4,7),(0,5),(1,4)]
    self.til5obj = tilc.Til(self.jogosObj, 5)
    middlename   = 'rulertil'
    self.logFile = funcs.mountLogFile(middlename, self.jogosObj)

  def low(self, pos):
    return self.limits[pos][0]
  
  def high(self, pos):
    return self.limits[pos][1]

  def forbiddenRegions(self):
    regions = None
    return regions


class RulerConsecs():
  '''
  consecs patterns
  Depends on Chooser class.
    Parameters are "estimated" from heuristics
    that take into account probability for next consec
  '''
  
  def __init__(self, jogosObj):
    Ruler.__init__(self, jogosObj)
    self.limits = [(0,1),(1,4),(4,7),(0,5),(1,4)]
    self.til5obj = tilc.Til(self.jogosObj, 5)
    middlename   = 'rulerconsecs'
    self.logFile = funcs.mountLogFile(middlename, self.jogosObj)

    nOfCombs = 3268760; total = 0
    cDict = {'b97531': 3960, 'c9642': 495, '8421': 138600, 'a642': 13860, 'b8531': 7920, '8531': 69300, '754321': 9240, 'c9754321': 990, 'dcba987654321': 110, 'b85321': 7920, '975321': 13860, 'a54321': 2310, '4': 330, '6321': 13860, 'c96421': 990, '7531': 9240, '931': 13860, 'b852': 3960, 'db97531': 110, 'b8521': 3960, 'c975321': 990, '54321': 110, 'b8654321': 7920, '94321': 13860, 'a86421': 9240, 'b864321': 7920, 'a75321': 27720, 'b8642': 3960, '51': 9240, '52': 3960, '63': 4620, '531': 990, 'b74321': 3960, 'db987654321': 110, '7321': 46200, 'dba987654321': 110, '964321': 55440, 'c96321': 495, '9754321': 13860, '7654321': 1320, '4321': 11, 'c97531': 990, 'a63': 9240, 'db975321': 110, 'ca987654321': 990, '854321': 34650, 'ca8642': 495, '9631': 55440, 'b854321': 3960, '83': 69300, '8654321': 13860, '81': 2310, '8321': 34650, '84': 11550, '84321': 46200, '74321': 27720, '831': 138600, '85321': 69300, '82': 34650, 'a8642': 4620, '521': 3960, '7': 1320, '421': 110, '864321': 13860, '963': 9240, '75321': 9240, 'db97654321': 110, 'cba987654321': 495, '9521': 83160, 'a864321': 9240, 'c987654321': 495, 'c9631': 990, '9642': 27720, 'b7321': 1320, 'c963': 165, '841': 138600, '821': 13860, 'a621': 9240, 'a742': 13860, 'edcba987654321': 11, '642': 1980, 'b987654321': 3960, 'b7654321': 1320, '73': 46200, 'a64321': 27720, 'ba987654321': 1320, 'b7421': 7920, '621': 27720, '741': 27720, 'a7421': 27720, 'b7531': 3960, '9531': 83160, '61': 34650, '62': 41580, '6421': 3960, 'c97654321': 990, '9321': 2772, '5321': 990, 'b741': 3960, '731': 138600, 'b742': 3960, '852': 34650, '86421': 13860, 'a51': 9240, 'b75321': 3960, 'a52': 13860, '6': 4620, 'b975321': 3960, 'a987654321': 2310, '631': 27720, 'a8654321': 9240, 'db9754321': 110, 'a7531': 27720, 'a87654321': 9240, '842': 69300, 'a62': 13860, '93': 9240, 'a7654321': 13860, '94': 13860, 'c9654321': 495, '96421': 55440, 'a631': 55440, 'a754321': 27720, '95321': 83160, 'b731': 3960, 'a6321': 27720, '721': 46200, '954321': 27720, '87654321': 2310, '9654321': 27720, '742': 27720, 'ca86421': 990, 'a6421': 27720, 'a741': 13860, 'b86421': 7920, '96321': 27720, '64321': 3960, 'b97654321': 3960, '8521': 34650, 'c964321': 990, '951': 27720, 'ca87654321': 990, '952': 83160, '42': 55, 'ca8654321': 990, '41': 495, '5': 2772, '9421': 55440, 'ca864321': 990, 'b9754321': 3960, 'b73': 1320, '7421': 55440, '987654321': 2772, 'a654321': 9240, 'b87654321': 3960, '97654321': 13860, 'a5': 462, '72': 92400, '71': 27720, 'a5321': 9240, 'a521': 13860, 'b754321': 3960, 'a531': 9240, '942': 27720, 'a74321': 13860, '941': 83160, '654321': 495, '97531': 13860, '8642': 6930}
    consecValues = cDict.values()
    total = sum(consecValues)
    assert(nOfCombs == total)
    return cDict


class RulerRepeat(object):

  def __init__(self, jogosObj):
    Ruler.__init__(self, jogosObj)
    middlename   = 'rulerrepeats'
    self.logFile = funcs.mountLogFile(middlename, self.jogosObj)

if __name__ == '__main__':
  # testRepeat()
  pass