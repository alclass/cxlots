#!/usr/bin/env python
# -*- coding: utf-8 -*-

FilterNamesDict = {}

nOfFilter = 0
FILTSOMA = nOfFilter
FilterNamesDict[FILTSOMA] = 'FILTSOMA'

nOfFilter += 1
FILTCONSECS = nOfFilter
FilterNamesDict[FILTCONSECS] = 'FILTCONSECS'

nOfFilter += 1
FILTRADII = nOfFilter
FilterNamesDict[FILTRADII] = 'FILTRADII'

nOfFilter += 1
FILTREMAINDERS = nOfFilter
FilterNamesDict[FILTREMAINDERS] = 'FILTREMAINDERS'

nOfFilter += 1
FILTREPEATS = nOfFilter
FilterNamesDict[FILTREPEATS] = 'FILTREPEATS'

nOfFilter += 1
FILTTILS  = nOfFilter
FilterNamesDict[FILTTILS] = 'FILTTILS'

FilterList = FilterNamesDict.keys()
FilterList.sort()

if __name__ == '__main__':
  pass
