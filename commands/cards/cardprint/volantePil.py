#!/usr/bin/env python
#-*-coding:utf8-*-
'''
volantePil.py
'''
import Image
import random
import sys # os,

a=1
#from cardprint
sys.path.insert(0, '')
from cardprint import volantePaperPrint as vpp
import CLClasses

im=Image.new('L',(500,500),'white')
im2=Image.new('L',(5,5),'black')
# im.show()
# im2.show()
im2=Image.new('L',(15,15),'black')
crop=im2.crop((0,0,15,15))
im.paste(crop, (0,0,15,15))
im.paste(crop, (30,30,45,45))

def geraVolante(jogoObj):
  jogo = jogoObj.jogo
  matrix = vpp.generateMatrix(jogo)
  print matrix

def geraVolantes():
  jogosObj=CLClasses.getJogosObj('lf')
  jogos = []
  for i in range(1,5):
    jogo = jogosObj.getJogos()[-i]
    jogos.append(jogo)
  matrix = vpp.Matrix('lf')
  #matrix.setJogo(jogo)
  matrix.generateFolha(jogos)
  #mat = matrix.generateMatrix()
  #matrix.generateVolante()
  #matrix.savePdf()
  #print mat

if __name__ == '__main__':
  geraVolantes()
