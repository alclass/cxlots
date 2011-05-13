#!/usr/bin/env python
#--*--encoding:utf8--*--
import os, time, sys

def divideFile(filenameApostasIn):
  '''
  This will divide more than 24 jogos into 24-jogo files.
  '''
  outFilenameBasename = 'apostas-to-print-%02d.txt'
  next = 1
  outFilename = outFilenameBasename %(next)
  
  print 'writing', outFilename
  outfile = open(outFilename, 'w')

  fileApostasIn = open(filenameApostasIn)
  line = fileApostasIn.readline(); c = 0

  while line:
    c+=1
    outfile.write(line)
    lastFileRecorded = outFilename # this may be improved, it's just to avoid an extra and empty file when having a multiple of 24 apostas
    if c % 24 == 0:
      outfile.close()
      next += 1
      outFilename = outFilenameBasename %(next)
      print 'writing', outFilename
      outfile = open(outFilename, 'w')
    line = fileApostasIn.readline()
  outfile.close()
  if lastFileRecorded != outFilename:
    os.remove(outFilename)

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print 'please, enter apostas filename.'
    sys.exit(0)
  filenameApostasIn = sys.argv[1]
  if not os.path.isfile(filenameApostasIn):
    print 'file', filenameApostasIn, 'does not exist. Please, retry.'
    sys.exit(0)
  divideFile(filenameApostasIn)
