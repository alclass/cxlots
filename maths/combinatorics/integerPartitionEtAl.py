# integerPartitions.py

'''
Created on 22/11/2011

@author: up15
'''

def doCombTertilSum6():
  sumTarget = 6; arraySize = 3 # sixtil
  nOfCombs = 0; d=[0]*arraySize
  for d[0] in range(0,7):
    for d[1] in range(0,7):
      for d[2] in range(0,7):
        s = sum(d)
        if s == sumTarget:
          nOfCombs += 1
          print s, nOfCombs, d
  print 'nOfCombs', nOfCombs
  print 'theory', 5+40+40+24+10+24+16+6+16+5



def doCombQuintilSum6():
  sumTarget = 6; arraySize = 6 # sixtil
  nOfCombs = 0; d=[0]*arraySize
  for d[0] in range(0,7):
    for d[1] in range(0,7):
      for d[2] in range(0,7):
        for d[3] in range(0,7):
          for d[4] in range(0,7):
            s = sum(d)
            if s == sumTarget:
              nOfCombs += 1
              print s, nOfCombs, d
  print 'nOfCombs', nOfCombs
  print 'theory', 5+40+40+24+10+24+16+6+16+5

def doCombSixtilSum6():
  sumTarget = 6; arraySize = 6 # sixtil
  nOfCombs = 0; d=[0]*arraySize
  for d[0] in range(0,7):
    for d[1] in range(0,7):
      for d[2] in range(0,7):
        for d[3] in range(0,7):
          for d[4] in range(0,7):
            for d[5] in range(0,7):
              s = sum(d)
              if s == sumTarget:
                nOfCombs += 1
                print s, nOfCombs, d
  print 'nOfCombs', nOfCombs

def balancePlusMinusOne(i_minusOne, i_plusOne, d):
  d[i_minusOne] -= 1
  d[i_plusOne] += 1

def ajustIndices(i_passing, i_hold, d, arraySize=5):
  # indices administration
  if i_passing + 1 < arraySize:
    if i_passing + 1 != i_hold:
      balancePlusMinusOne(i_passing, i_passing+1, d)
      i_passing+=1
    else:
      # i_passing and i_hold are equal:
      if i_passing + 2 < arraySize:
        balancePlusMinusOne(i_passing, i_passing+2, d)
        i_passing+=1
      else:
        # game over
        return
  elif i_passing + 1 == arraySize and i_hold < arraySize:
    if i_hold == 0 and d[i_hold] > 0:
      d[i_hold] -= 1
      i_passing = 1
      d[i_passing] = 6
     
     

def doComb():
  nOfCombs = 0; d=[0]*5; i_passing = i_hold = 0;  d[i_hold]=6
  while 1:
    s = sum(d)
    if s > 6:
      raise ValueError, 's > 6'
    if s == 6:
      nOfCombs += 1
      print s, nOfCombs, d
      ajustIndices(i_passing, i_hold, d)

nOfCombs = 0
def recurse(d):
  global nOfCombs
  if sum(d) == 6:
    nOfCombs += 1
    print nOfCombs, d
 
  return recurse(d)




def canIGoWestWithOneAmount(i_passing):
  if i_passing == 0:
    return False
  return True

class RecurseComb():
  def __init__(self):
    self.sumTarget = 6
    self.arraySize = 5
    self.d = [0] * self.arraySize
    #self.i_leftside  = 0
    self.i_midpoint  = 0
    self.process()
  def canIGoWestWithOneAmount(self):
    if self.i_rightside < self.arraySize - 1:
      return True
    return False
  def goWestWithOneAmount(self):
    print 'goWestWithOneAmount self.i_rightside',self.i_rightside,
    self.d[self.i_rightside]-=1
    self.d[self.i_rightside+1]+=1
    self.i_rightside+=1
    #return self.i_rightside+1
    print '=>', self.d
  def canISubtract1FromMidpointAndAdd1ToRightPoint(self):
    if self.d[self.i_midpoint] > 0:
      return True
    return False
  def subtract1FromMidpointAndComplementAdd1ToRightPoint(self):
    self.d[self.i_midpoint]-=1
   
    self.i_rightside = self.i_midpoint + 1
    self.d[self.i_rightside]+=1
  def isThereSubtractablesBetweenMidAndRight(self):
    pass
  def canIMoveMidpointToRightSide(self):
    if self.d[self.i_midpoint]==0:
      # if self.i_midpoint != self.i_rightside:
      return True
    return False
  def moveMidpointToRightSide(self):
    self.i_midpoint+=1
    self.i_rightside = self.i_midpoint + 1
    self.d = [0] * self.arraySize
    self.d[self.i_midpoint]=self.sumTarget
  def isRightSideOutbound(self):
    if self.i_rightside == self.arraySize:
      # well, self.i_rightside got outbound, it's game over, the algorithm has finished
      return True
    return False
  def process(self):
    # bootstrap (first) pass
    self.d[ 0 ]= self.sumTarget
    self.i_rightside = 0
    self.nComb = 0
    while 1:
      self.nComb += 1
      print 'nComb', self.nComb, self.d
      # ================================
      if self.isRightSideOutbound():
        # game over
        print 'game over self.isRightSideOutbound()'
        break
      # ================================
      elif self.canIGoWestWithOneAmount():
        self.goWestWithOneAmount()
        #return self.process()
      # ================================
#      elif self.isThereSubtractablesBetweenMidAndRight():
#        self.subtract1FromMidpointAndAdd1ToRightPoint()
      elif self.canISubtract1FromMidpointAndAdd1ToRightPoint():
        self.subtract1FromMidpointAndAdd1ToRightPoint()
        #return self.process()
      # ================================
      elif self.canIMoveMidpointToRightSide():
        self.moveMidpointToRightSide()
        #return self.process()
      # game over
      #return

rc = RecurseComb()   


# ==============================================

'''
Created on 23/11/2011

@author: up15
'''

def integerPartitionOf(n):
  a = [0 for i in range(n + 1)]
  k = 1
  a[0] = 0
  a[1] = n
  while k != 0:
      x = a[k - 1] + 1
      y = a[k] - 1
      k -= 1
      while x <= y:
          a[k] = x
          y -= x
          k += 1
      a[k] = x + y
      yield a[:k + 1]

def getIntOrRoundedIntOrNone(n):
  try:
    if n != int(n):
      n = round(n, 0)
  except ValueError:
    return None # well, n is not a number at all! Return None
  return n

def binarySearch(array, n):
  '''
  This is the entry point for the binarySearchRecursive
  Some checkings and preparations happen here
  '''
  if array == None or len(array)==0:
    return None, 1 # ie, array is either None or empty, so n is not found anyway :: 1 = nOfIterations
  # okay, array was checked for "noneness" or emptiness
  # now, let's check if n is really integer, if not, make it a rounded integer
  n = getIntOrRoundedIntOrNone(n)
  if n == None:
    return None, 1 # well, n is not a number at all! If so, obviously it cannot be found
  # as this is a preparing method for the recursive method, some processing may done to assure the array is in ascending order
  array.sort()
  if n < array[0] or n > array[-1]:
    return None, 1 # ie, n is either below the least integer or above the biggest integer in the array
  # if passed thru above conditions, it's "good to go"
  return binarySearchRecursive(array, n)

def binarySearchRecursive(array, n, pos=0, nOfIterations=1):
  tamanho = len(array)
  if n == array[0]:
    # recursion exit point n. 1 of 3
    foundPos = 0 + pos # + 1
    return foundPos, nOfIterations
  elif tamanho == 1:  # and it was not found above, so n is not here, return None meaning "not found"
    return None, nOfIterations # ie, not found
  lastPosition = tamanho - 1
  if n == array[lastPosition]:
    # recursion exit point n. 2 of 3
    foundPos = lastPosition + pos # + 1
    return foundPos, nOfIterations
  if tamanho % 2 == 0:
    mid = tamanho / 2 - 1
  else:
    mid = tamanho / 2
  #print 'mid', mid, ' array[mid] elem =', array[mid]
  if array[mid]==n:
    # recursion exit point n. 3 of 3
    foundPos = mid + pos # + 1
    return foundPos, nOfIterations
  elif array[mid] > n:
    array = array[:mid]
    # recursive call n. n. 1 / 2
    return binarySearchRecursive(array, n, pos, nOfIterations + 1)
  else: # array[mid] < n:
    array = array[mid+1:]
    # recursive call n. 2 / 2
    return binarySearchRecursive(array, n, pos + mid + 1, nOfIterations + 1)

import unittest, random
class Test(unittest.TestCase):
  def setUp(self):
    self.a10 = range(1,11)
    self.a20 = range(1,21)
    self.randomArray = random.sample(xrange(100000), 250)
    self.randomArray.sort() # this sort() must exist for it's looped over in a test case method below before getting a sort() inside binarySearch()
    self.calculateExpectedMaxNOfIterationsPlus1() 
  def calculateExpectedMaxNOfIterationsPlus1(self):   
    # calculating expectedMaxNOfIterationsPlus1 in THREE STEPS
    arraySize = len(self.randomArray) # 1st step
    expectedMaxNOfIterationsFloat = math.log(arraySize, 2) # 2nd step
    self.expectedMaxNOfIterations = int(expectedMaxNOfIterationsFloat) # 3rd step
    self.expectedMaxNOfIterationsPlus1 = self.expectedMaxNOfIterations + 1
  def test_binarySearch(self):
    indexPositionExpected = 6; nOfIterationsExpected = 3
    self.assertEqual(binarySearch(self.a10, 7), (indexPositionExpected, nOfIterationsExpected))
    self.assertEqual(binarySearch(self.a20, 1), (0, 1))
    self.assertEqual(binarySearch(self.a20, 20), (19, 1))
    self.assertEqual(binarySearch(self.a20, 15), (14, 2))
    self.assertEqual(binarySearch(self.a20, 18), (17, 3))
    self.assertEqual(binarySearch(self.a20, 19), (18, 4))
  def test_binarySearchWithShuffledArray(self):
    random.shuffle(self.a10)
    random.shuffle(self.a20)
    # order must be different now
    self.assertNotEqual(self.a10, range(1,11))
    self.assertNotEqual(self.a20, range(1,21))
    self.test_binarySearch()
    # order must be back the same, for a list is passing everywhere by reference and the sort() side effect has happened
    self.assertEqual(self.a10, range(1,11))
    self.assertEqual(self.a20, range(1,21))
  def test_binarySearchWithEmptyArrayOrNone(self):
    # binarySearch With Empty Array must return None for indexPositionExpected
    # and 1 for nOfIterationsExpected
    for someInteger in [-123, 0, 123]:
      for arrayEitherEmptyOrNone in [None, []]:
        noneReturned, nOfIterationsExpected = binarySearch(arrayEitherEmptyOrNone, someInteger)
        self.assertEqual(noneReturned, None)
        self.failUnless(nOfIterationsExpected == 1)
  def test_binarySearchWithNAsFloat(self):
    indexPositionExpected = 6; nOfIterationsExpected = 3
    self.assertEqual(binarySearch(self.a10, 6.8), (indexPositionExpected, nOfIterationsExpected))
    self.assertEqual(binarySearch(self.a20, 0.8), (0, 1))
    self.assertEqual(binarySearch(self.a20, 20.3), (19, 1))
  def test_binarySearchNotToFindInteger(self):
    self.assertEqual(binarySearch(self.a10, 11), (None, 1))
    self.assertEqual(binarySearch(self.a20, -1), (None, 1))
  def test_binarySearchWithRandomArrayInAscendingOrder(self):
    # 1st test with random: in ascending order
    for position in range(len(self.randomArray)):
      self.doLoopForBinarySearchWithRandomArray(position)
  def test_binarySearchWithRandomArrayInDescendingOrder(self):
    # 2nd test with random: in descending order
    for position in range(len(self.randomArray)-1, -1):
      self.doLoopForBinarySearchWithRandomArray(position)
  def test_binarySearchWithRandomArrayInRandomOrder(self):
    # 3rd test with random: in random shuffled order
    indices = range(len(self.randomArray))
    random.shuffle(indices)
    while len(indices) > 0:
      position = indices.pop()
      self.doLoopForBinarySearchWithRandomArray(position)
  def doLoopForBinarySearchWithRandomArray(self, positionExpected):
      element = self.randomArray[positionExpected]
      positionReturned, nOfIterationsReturned = binarySearch(self.randomArray, element)
      self.assertEqual(positionReturned, positionExpected)
      # Only in version 2.7 or above (we're using 2.6, so we'll comment these two lines below and apply an assertTrue
      #self.assertLess(nOfIterationsExpected, expectedMaxNOfIterationsPlus1)
      #self.assertGreater(nOfIterationsExpected, 0)
      self.assertTrue(nOfIterationsReturned < self.expectedMaxNOfIterationsPlus1)
      self.assertTrue(nOfIterationsReturned > 0)
   
   
def testAdHoc():
  randomArray = random.sample(xrange(100000), 17)
  randomArray.sort()
  indices = range(len(randomArray))
  random.shuffle(indices)
  while len(indices) > 0:
    position = indices.pop()
    integer = randomArray[position]
    print 'integer', integer
    positionReturned, nOfIterationsReturned = binarySearch(randomArray, integer)
    print randomArray
    print 'for', integer, '==>> positionReturned, nOfIterationsReturned', positionReturned, nOfIterationsReturned
   
#print integerPartitionOf(5)
print 'binarySearch(range(1,21), 19)', binarySearch(range(1,21), 19)
import math
print 'math.log(20,2)', math.log(20,2)
print 'unittest.main()'
unittest.main()
# testAdHoc()


'''
Created on 30/11/2011

@author: up15
'''
import hashlib, os, sqlite3 #, unicode

class Db():
  def __init__(self):
    self.conn = sqlite3.connect('fileSha1.sqlite')
    self.sqliteCreate()
    self.zeroRows()
  def sqliteCreate(self):
    sql = '''
  CREATE TABLE IF NOT EXISTS `fileSha1` (
    `hexSha1` VARCHAR(40) NOT NULL,
    `filePath` VARCHAR(400) NOT NULL,
  PRIMARY KEY ( `hexSha1` ) ) 
    '''
    retVal = self.conn.execute(sql)
    #print 'create table retVal', retVal
  def zeroRows(self):
    sql = 'delete from fileSha1 ;'
    retVal = self.conn.execute(sql)
    if retVal:
      self.conn.commit()
  def insertIntoSqlite(self, filePathObj):
    hexSha1 = filePathObj.getHexSha1()
    filePath = filePathObj.filePath
    sql = "insert into fileSha1 (hexSha1,filePath) values ('%s', '%s');" %(hexSha1, filePath)
    #print sql  
    #hashDict[hex] = filePathObj.filePath
    retVal = self.conn.execute(sql)
    if retVal:
      self.conn.commit()
  def isHexIsDb(self, hexSha1):
    #print 'isHexIsDb(self, hex):', '['+hexSha1+'] =', len(hexSha1)
    sql = "select * from `fileSha1` where `hexSha1` = '%s' ;" %(hexSha1)
    rows = self.conn.execute(sql)
    #cursor = self.conn.cursor()
    #rows = cursor._rows
    for row in rows:
      #if len(rows) > 1:
      hex = row[0]
      filePath = row[1]
      filePathObj = FileSha1(filePath, hex)
      return filePathObj
    return None
   
class FileSha1():
  def __init__(self, filePath, hex = None):
    self.filePath = filePath
    self.hexSha1 = None
    if hex == None:
      self.findSha1()
    else:
      self.hexSha1 = hex
  def getHexSha1(self):
    if self.hexSha1 != None:
      return self.hexSha1
    else:
      self.findSha1()
      if self.hexSha1 != None:
        return self.hexSha1
    return None
  def findSha1(self):
    fileContents = None; f = None
    try:
      # print 'self.filePath'
      f = open(self.filePath, 'rb') # read as Binary, so no encoding problem arises here, we just need the contents to pass the hash function
      if f != None:
        fileContents = f.read()  # unicode(   .read(), 'utf-8')
    except IOError:
      pass
    finally:
      if f!=None:
        f.close()
#    except TypeError:
#      print 'TypeError with file %s' %self.filePath
#      pass
    if fileContents != None:
      hashObj = hashlib.sha1()
      hashObj.update(fileContents)
      self.hexSha1 = hashObj.hexdigest()

totalOfRepeats = 0
def processFileIsRepeated(filePathObj, otherFileSha1):
  global totalOfRepeats,  count, noneFilesCount
  hex = filePathObj.getHexSha1()
  # otherFile = hashDict[hex]
  totalOfRepeats += 1
  print totalOfRepeats, 'Repeat: (  count, noneFilesCount ) = ',  count, noneFilesCount
  try:
    print hex,  filePathObj.filePath
  except UnicodeEncodeError:
    print 'UnicodeEncodeError'

hashDict = {}; count = 0; noneFilesCount = 0
def walkTree():
  global count, noneFilesCount
  dbObj = Db()
  for eachDir, dirs, files in os.walk('I:\\'):
    for file in files:
      count += 1
      #print count, 'Processing file', file
      #print ' ==========>>>>>>>>>>>> in', eachDir
      absPathOfCurrentDir = os.path.abspath(eachDir)
      filePath = os.path.join(absPathOfCurrentDir, file)
      filePath = unicode(filePath, 'latin1')
      filePathObj = FileSha1(filePath)
      hexSha1 = filePathObj.getHexSha1()
      # print count, hexSha1, 'noneFilesCount', noneFilesCount+1
      if hexSha1 != None:
        otherFileSha1 = dbObj.isHexIsDb(hexSha1)
        #in hashDict.keys():
        if otherFileSha1 != None:
          processFileIsRepeated(filePathObj, otherFileSha1)
        else:
          dbObj.insertIntoSqlite(filePathObj)
      else:
        noneFilesCount += 1

walkTree()

