'''
Created on 22/11/2011

@author: friend
'''

d=6,0,0
d=list(d)
i1=0
i2=1
def decrLeft():
  d[i1]-=1
  d[i2]=+1
  
ENDLINE = False; nComb = 1  
while 1:
  nComb += 1
  print 'nComb', nComb, 'd =',d,  'i1 =', i1, 'i2 =', i2
  if nComb == 20:
    break
  if d[i1] > 0 and i2 < len(d):
    d[i1]-=1
    d[i2]+=1
    i1+=1
    i2+=1
    if i2 == len(d):
      ENDLINE=True
      for j in [1,0]:
        if d[j]!=0:
          i1=j
          d[i2-1]-=1
          d[i1]-=1
          d[i1+1]+=2
          ENDLINE=False
      if ENDLINE:
        break
      continue
'''        
  elif i2 == len(d):
    for j in [1,0]:
      if d[j]!=0:
        d[2]-=1
        i1=j
        d[i1]-=1
        i2=j+1
        partialSoma = sum(d)
        dif = 6 - partialSoma 
        d[i2]=6-diff
        continue
    # all lefts are zero
      break
  else:
    # seach leftwards
    for j in [1,0]:
      if d[j] > 1:
        i1=j
        d[j]-=1
        i2=j+1
        d[i2]+=1
'''    
print 'end', d, i1, i2
        