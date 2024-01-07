#!/usr/bin/env python
"""
fs/strfs/str_patterns.py

"""
import string
import sys
letters52 = string.ascii_letters


def is_list_an_intlist(inlist):
  try:
    outlist = trans_list_to_intlist(inlist)
    if len(inlist) == len(outlist):
      return True
  except (TypeError, ValueError):
    pass
  return False


def trans_list_to_intlist(inlist):
  outlist = []
  for e in inlist:
    try:
      outlist.append(int(e))
    except ValueError:
      continue
  return outlist


def trans_intlist_to_zfillstrlist(intlist, zfill=None, dosort=False):
  """
  This function converts a dozens list to a zfilled string whose items are space-separated
  Example:
    f([1,2,3,4,5,6]) => '01 02 03 04 05 06'
  """
  if intlist is None or len(intlist) == 0:
    return ''
  intlist = trans_list_to_intlist(intlist)
  if dosort:
    intlist.sort()
  try:
    in_zfill = int(zfill)
  except TypeError:
    in_zfill = None
  if in_zfill is None:
    dezenas_strlist = map(lambda e: str(e), intlist)
  else:
    in_zfill = in_zfill if in_zfill > -1 else -in_zfill
    largest_i = 10 ** in_zfill - 1
    intlist = filter(lambda i: i < largest_i+1, intlist)
    dezenas_strlist = map(lambda e: str(e).zfill(zfill), intlist)
  all_dezenas_as_str = ' '.join(dezenas_strlist)
  return all_dezenas_as_str


def trans_intlist_to_descendant_stair_strlist(intlist):
  """
  Example:
    f([1, 3, 4, 2, 6, 5]) => '0123456'

  """
  # 1st step: filter out zeroes
  intlist = filter(lambda n: n != 0, intlist)
  # 2nd step: sort descendantly
  intlist.sort()
  # 3rd step: invert order
  intlist.reverse()
  intlist_as_str = ''.join(map(str, intlist))
  return intlist_as_str


def trans_list_to_nonspace_jointstr(olist):
  olist = filter(lambda o: o is not None, olist)
  return ''.join(map(str, olist))


def trans_intlist_spacesep_printable_str(intlist, zfill=2):
  """
  Example:
    f([1,2,3,4,5,6]) => '01 02 03 04 05 06'

  """
  return trans_intlist_to_zfillstrlist(intlist, zfill)


def reverse_string(line):
  char_list = strToCharList(line)
  char_list.reverse()
  new_line = ''.join(char_list)
  return new_line

def trans_spacesep_numberstr_to_intlist(line):
  """
  Example:
    f('01 02 03 04 05 06') => [1,2,3,4,5,6]
  """
  try:
    line = line.strip(' \t\r\n')
    pp = line.split(' ')
  except (AttributeError, TypeError):
    return []
  intlist = []
  for e in pp:
    try:
      i = int(e)
      intlist.append(i)
    except ValueError:
      continue
  return intlist


def number_list_to_str_commaless(lista, n_for_zfill=2):
  """
  Pretty Print for a list
  Instead of coming out like [5,12,...]
  it will come out like 05 12 ...
  """
  new_list = []
  for elem in lista:
    new_list.append(str(elem).zfill(n_for_zfill))
  s = str(new_list)
  s = s.replace("'",'')
  s = s.replace(",",'')
  s = s[1:-1]
  return s

def number_list_to_str_no_pretty_print(jogo):
  """
  Not Pretty Print for jogo list
  Instead of coming out like [5,12,...]
  it will come out like 5 12 ...
  The pretty-print version above, instead, will come out like 05 12 ...
  """
  s = str(jogo)
  s = s.replace("'",'')
  s = s.replace(",",'')
  s = s[1:-1]
  return s

def number_list_to_sticked_char(jogo, n_for_zfill=2):
  """
  Spaceless Pretty Print for jogo list
  Instead of coming out like [5,12,...]
  it will come out like 0512 ...
  """
  s = number_list_to_str_commaless(jogo, n_for_zfill)
  s = s.replace(" ",'')
  return s

def number_list_to_a_whole_int(jogo):
  """
  Example for Lotofácil
    nLower = 10203040506070809101112131415
    nUpper = 111213141516171819202122232425
  """
  s = number_list_to_sticked_char(jogo)
  if s[0] == '0':
    s = s[1:]
  #print 's', s
  whole_int = int(s)
  return whole_int

def print_number_list(lista, n_of_zfill=2):
  for elem in lista:
    print( str(elem).zfill(n_of_zfill),)
  print()

def print_list(lista):
  for elem in lista:
    print(elem)

def strToCharList(s):
  lista = []
  for x in s:
    lista.append(x)
  return lista

def printJogos(jogos):
  c=0
  for jogo in jogos:
    c+=1
    print_number_list(jogo)

def print_hist_g(hist_g):
  if hist_g == None:
    return 
  numbers = hist_g.keys()
  numbers.sort()
  for number in numbers:
    print( number, '=> quant:', hist_g[number])


def print_dict(occur_dict):
  if occur_dict is None or len(occur_dict) == 0:
    print( "occurDict is None or empty.")
    return
  occurences = occur_dict.get_keys()
  occurences.sort()
  for occurence in occurences:
    parcel_str = '%s:%s ' %(str(occurence), str(occur_dict[occurence]))
    print(parcel_str, )
  min_value = min(occur_dict.values())
  max_value = max(occur_dict.values())
  print('min', min_value, ':: max', max_value)


def ad_hoctest_print_dict():
  d_dict = {'a':33, 'b':17, 'c':21, 'd':-3}
  print_dict(d_dict)
# testAdHocPrintDict()  
  

'''
def getClassName(selfRef):
  rep = repr(selfRef)
  piece = rep.split(' ')[0]
  if piece.find('__main__.') > -1:
    className = piece[len(main):]
  else:
    dotPos = piece.find('.')  # Eg '<Stat.Stat object at 0xb7fc156c>' ==>> 'Stat'
    className = piece[dotPos+1:]
  return className

def mountLogFile(selfRef, jogosObj):
  className    = getClassName(selfRef)
  now = datetime.date.today()
  sigla = jogosObj.sqlTable
  ultimoNDoConc = len(jogosObj.getJogos())
  logFilename = 'logs/%s-%s-%d--%s.log' %(sigla, className, ultimoNDoConc, now)
  logFile = open(logFilename,'w')
  return logFile

def returnJogosObj(eitherJogosObjOrS2):
  jogosObj = None
  if type(eitherJogosObjOrS2) == str:
    standard2LetterName = eitherJogosObjOrS2
    jogosObj = CLClasses.getJogosObj(standard2LetterName)
  elif type(eitherJogosObjOrS2) == CLClasses.Jogos:
    jogosObj = eitherJogosObjOrS2
  else:
    errorMsg = 'eitherJogosObjOrS2 should be eitherJogosObjOrS2 but it is = %s' %(eitherJogosObjOrS2)
    raise ValueError, errorMsg
  return jogosObj

def calcConsecPattern(jogo, standard2LN):
  if standard2LN == 'MS':
    calcConsecPatternMS(jogo)
  elif standard2LN == 'LF':
    calcConsecPatternMS(jogo)
'''

def convert_consecs_to_chars(consecs):
  consecStr = ''
  for consec in consecs:
    if consec == 0:
      break
    if consec > 61:
      error_msg = 'max value for consec is 61 :: it was = %d' % consec
      raise ValueError(error_msg)
    if consec < 10:
      consecStr += str(consec)
    else:
      dif = consec - 10
      consecStr += letters52[dif]
  return consecStr
        
def calc_consec(jogo):
  n_de_dezenas = len(jogo)
  n_de_dezenas_menos_um = n_de_dezenas - 1
  consecs = [0] * n_de_dezenas_menos_um

  for i in range(n_de_dezenas-1, 0, -1):
    for j in range(i-1, -1, -1):
      inc = i - j
      if jogo[i] == jogo[j] + inc:
        consecs[inc-1] += 1
      else:
        break

  '''
  # code below is not working

  for i in range(0, n_de_dezenas_menos_um):
    for j in range(i+1, n_de_dezenas):
      inc = j - i
      if jogo[i] == jogo[j] + inc:
        consecs[inc-1] += 1
      else:
        break
  '''

  if consecs[0] == 0:
    return 0

  consec_pattern = convert_consecs_to_chars(consecs)

  '''  consec_pattern = 0; i = 0
  for consec in consecs:
    if consec == 0:
      break
    consec_pattern += consec * 10 ** i
    i += 1
  '''
  return consec_pattern


def no_point_and_comma_to_point(value):
  if value is None or not isinstance(value, str):
    return value
  if value.find('.') > -1:
    value = value.replace('.','') # ie, 1.000,00 should become 1000,00
  if value.find(',') > -1:
    value = value.replace(',','.') # ie, 1000,00 should become 1000.00
  return value

def form_arg_caller(methodToBeCalled):
  moduleName = sys.argv[0]
  moduleName = moduleName.lstrip('./')
  moduleName = moduleName.rstrip('.py')
  argCaller  = moduleName + '.' + methodToBeCalled
  #print 'argCaller', argCaller
  try:
    argCaller  = eval(argCaller)
  except NameError:
    #print 'importing moduleName'
    exec('import ' + moduleName)
    argCaller  = eval(argCaller)
  #print 'argCaller', argCaller
  return argCaller

'''
def updateCaller(methodToBeCalled):
  moduleName = sys.argv[0]
  moduleName
  if len(sys.argv) >= 3:
    arg = sys.argv[1]
    if arg == '-u':
      jogoTipo = sys.argv[2] # eg 'MS'
      argCaller = form_arg_caller(methodToBeCalled)
      #sys.exit(0)
      argCaller(jogoTipo)
      return
  pprint.printUsage()
'''

def test_calc_consec():
  jogo = [1,2,4,5,30,31]
  #jogo = [1,4,30,35,40,47]
  patt = calc_consec(jogo)
  print( jogo, patt)


if __name__ == '__main__':
  ad_hoctest_print_dict()
