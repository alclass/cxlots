class Dict1(dict):
  #dictVar = {}
  def __init__(self):
#    super(dict, self).__init__()
    self.dictVar = {}
  def __setitem__(self, key, value):
    self.dictVar[key] = value
  def __getitem__(self, key):
    return self.dictVar[key]
  def __repr__(self):
    return str(self.dictVar)

#'''
d=Dict1()
d['a']=10
print d['a']
print d
#'''

class Dict2():
  #dictVar = {}
  def __init__(self):
    self.dictVar = {}
  def __setitem__(self, key, value):
    self.dictVar[key] = value
  def __getitem__(self, key):
    return self.dictVar[key]
  def __repr__(self):
    return str(self.dictVar)

dd=Dict2()
dd['a']=1
print dd['a']
print d