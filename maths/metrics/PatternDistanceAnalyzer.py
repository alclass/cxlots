import random

games=[]
def generate_random_games():
  for i in xrange(100):
    game =[]
    for j in xrange(6):
      i,j
      dozen = random.randint(1,60)
      game.append(dozen)
    games.append(game)

class Dict2(dict):
  def add_or_set_to_1(self, key):
    if self.has_key(key):
      self[key]+=1
    else:
      self[key]=1
    
histfreqdict=Dict2()
def find_frequencies():
  for game in games:
    for dozen in game:
      histfreqdict.add_or_set_to_1(dozen)
  
def process_1():
  generate_random_games()
  find_frequencies()
  print histfreqdict
  print 'min', min(histfreqdict.values())
  print 'max', max(histfreqdict.values())

class PatternDistanceAnalyzer(object):
  
  def __init__(self):
    self.wpattern_sequence = []
    self.distances_histogram = {}
  
  def add_pattern(self, wpattern):
    self.wpattern_sequence.append(wpattern)
    
  def mount_distances_histogram(self):
    wprocess_already_processed = []
    for i, wpattern in enumerate(self.wpattern_sequence[:-1]):
      if wpattern in wprocess_already_processed:
        continue
      distance_array = []; distance = 0; last_jump = 0
      for compare_wpattern in self.wpattern_sequence[i+1:]:
        distance += 1
        if wpattern == compare_wpattern:
          this_jump = distance - last_jump
          distance_array.append(this_jump)
          last_jump = distance 
      
      self.distances_histogram[wpattern]=distance_array
      wprocess_already_processed.append(wpattern)   

  def patterns_that_had_distance_1(self):
    for wpattern in self.distances_histogram.keys():
      distance_array = self.distances_histogram[wpattern]
      for distance in distance_array:
        if distance == 1:
          print wpattern 

  def summarize(self):
    print 'Distance Dict',
    for wpattern in self.distances_histogram:
      print wpattern, self.distances_histogram[wpattern]


wpatterns = [
  '02211',
  '21111',
  '22110',
  '22110',
  '33000',
  '22110',
  '20220',  
  ]
def adhoc_test():
  analyzer = PatternDistanceAnalyzer()
  for wpattern in wpatterns:
    analyzer.add_pattern(wpattern)
  analyzer.mount_distances_histogram()
  analyzer.summarize()

adhoc_test()