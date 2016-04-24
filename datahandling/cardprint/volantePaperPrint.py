#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Image, sys

a=1
#sys.path.insert(0,'.')
sys.path.insert(0,'..')
import CLClasses
#import repeatsAverage

class Matrix(CLClasses.Base):


  fileCount = 1

  def __init__(self, eitherJogosObjOrS2):
    CLClasses.Base.__init__(self, eitherJogosObjOrS2)
    self.folhaA4 = Image.new('L',(400,400),'white')


  def setJogo(self, jogo):
    self.jogo = jogo

  def generateMatrix(self):
    print '='*30
    print self.jogo
    print '='*30; outMatrix = []
    for col in range(self.nOfCols):
      outRow = []
      for row in range(self.nOfLins):
        found = False
        for dezena in self.jogo:
          y = (dezena-1) / 5
          x = (dezena % 5) - 1
          if x == -1:
            x = 5 - 1
          if x==row and y==col:
            found = True
            dezenaOut = dezena
            break
        if found:
          outRow.append(1)
          print str(dezenaOut).zfill(2),
        else:
          outRow.append(0)
          print '__',
      outMatrix.append(outRow)
      print
    self.outMatrix = list(outMatrix)
    return outMatrix

  def generateVolante(self, folhaDx=0, folhaDy=0):
    volante = Image.new('L',(200,200),'white')
    dotBlock =Image.new('L',(15,15),'black')
    crop = dotBlock.crop((0,0,15,15))
    x = 0; y = 0
    for row in self.outMatrix:
      for col in row:
        if col == 1:
          volante.paste(crop, (x,y,x+15,y+15))
        x = x + 15
      y += 15
      x = 0
    crop = volante.crop((0,0,200,200))
    self.folhaA4.paste(crop, (folhaDx,folhaDy,folhaDx+200,folhaDy+200))
    print 'folhaDx,folhaDy,folhaDx+200,folhaDy+200', folhaDx,folhaDy,folhaDx+200,folhaDy+200
    #volante.show()

  def generateFolha(self, jogos):
    folhaCoords = ((0,0), (200,0),(0,200),(200,200))
    i=0
    for jogo in jogos:
      self.setJogo(jogo)
      self.generateMatrix()
      folhaDx, folhaDy = folhaCoords[i]
      self.generateVolante(folhaDx, folhaDy)
      i+=1
    self.savePdf()

  def savePdf(self):
    self.fileCount += 1
    print 'self.fileCount', self.fileCount
    filename = 'test%d.pdf' %(self.fileCount)
    filename = 'test1.pdf'
    self.folhaA4.save(filename)
    



def cardPrint(jogo):
  points=[]
  for dezena in jogo:
    y = (dezena-1) / 5
    x = (dezena % 5) - 1
    if x == 0:
      x = 5 - 1
    point = (x, y)
    points.append(point)
  print jogo
  generateMatrix(points)
  


if __name__ == '__main__':
  pass
  '''
  jogos = repeatsAverage.getHistoryJogos()
  for i in range(2):
    jogo = jogos[i]
    cardPrint(jogo)
    matrix = Matrix('lf')
    matrix.setJogo(jogo)
    matrix.generateMatrix()
    matrix.generateVolante
    #generateMatrix(jogo)
  '''