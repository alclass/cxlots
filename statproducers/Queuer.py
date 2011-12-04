#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime, sys, time
import sqlite3

a=1
import Checker as chkr
import CLClasses
import funcs
#import funcsForSql as fSql
import lambdas
import LgiCombiner as lc
import Runner
import Stat
import Stream
import Til as tilc
from cardprint import pprint

# first inStream: LgiCombiner
'''
plannedStreamsDict stores streamIns and streamOuts information
key 1 means the first streamIn and streamOut in the runner
key 2 (or higher) means, if that is the case, the tuple-streams will be used if more than 2 (or higher) filters/checkers are used
'''

plannedStreamsDict = { \
  1:(Stream.STREAM_LGICOMB, Stream.STREAM_BINFILE) , \
  2:(Stream.STREAM_BINFILE, Stream.STREAM_BINFILE) }


def getPlannedStreams(n):
  numbers = plannedStreamsDict.keys()
  numbers.sort()
  if n not in numbers:
    n = numbers[-1]  # ie, take the last one
  return plannedStreamsDict[n]

plannedFiltersList = [ \
  chkr.CHKR_SOMA_N      , \
  chkr.CHKR_REMAINDERS  , \
  chkr.CHKR_REPEATS     , \
  chkr.CHKR_CONSECS     , \
  chkr.CHKR_RADII       , \
  chkr.CHKR_TILS        ]


class Queuer(contr.Ruler):

  def __init__(self, eitherJogosObjOrS2):
    self.jogosObj  = funcs.returnJogosObj(eitherJogosObjOrS2)
    self.runner    = Runner.Runner(self.jogosObj)
    self.streamObj = Stream.Stream(self.jogosObj)
    self.executePlan()
    self.close()
    self.logFile = funcs.mountLogFile(self, self.jogosObj)

  def executePlan(self):
    passNumber = 0
    for filtre in plannedFiltersList:
      passNumber += 1
      streamInType, streamOutType = getPlannedStreams(passNumber)
      if passNumber > 1:
        inBinFilename = self.streamObj.outBinFilename
        self.streamObj.setInFilename(inBinFilename)
      inBinFilename  = self.streamObj.inBinFilename
      outBinFilename = self.streamObj.outBinFilename
      logLine = '%s filter %d streamIn %s streamIn %s' %(time.ctime(), filtre, inBinFilename, outBinFilename)
      self.logFile.write(logLine)
      self.streamObj.setStreamIn(streamInType)
      self.streamObj.setStreamOut(streamOutType)
      self.runner.setStreamObj(streamObj)
      checkerObj = chkr.getCheckerObjById(filtre, self.jogosObj)
      self.runner.setCheckerObj(checkerObj)
      self.runner.run()

  def close(self):
    self.runner.close()

def queueFiltersToRunner():
  queue = Queue('lf')
  queue.executePlan()
  


if __name__ == '__main__':
  queueFiltersToRunner()
