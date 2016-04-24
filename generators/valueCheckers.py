def checkIfValueIsInteger(value):
  if type(value) in [int, long]:
    return True
  try:
    n = int(value)
    return True 
  except ValueError:
    pass
  return False

def cleanCommas(value):
  value = value.replace(',', '')
  return value

def treatCommaAndPoint(value):
  if value.find(',') > -1:
    pp = value.split(',')
    if len(pp) == 2:
      if len(pp[-1]) <= 2: # should be cents
        # fine: got it
        if value.find('.') > -1:
          value = value.replace('.', '')
        value = value.replace(',', '.')
        return value
      else: # ie, len(pp[-1]) > 2:
        value = cleanCommas(value)
        return value
    elif len(pp) > 2:
      value = cleanCommas(value)
      return value
  elif value.find('.') > -1:
    pp = value.split('.')
    if len(pp) > 2:
      value = value.replace('.', '')
      return value
  # returning as it came
  return value

def checkIfValueIsCurrency(value):
  if type(value) in [float]:
    return True
  if type(value) == str:
    value = treatCommaAndPoint(value)
  try:
    value = float(value)
  except ValueError:
    return False
  return True

def normalizeDate(value):
  pp = value.split('/')
  year = pp[2]
  month = pp[1]
  day = pp[0]
  return year + '-' + month + '-' + day  