'''
Created on 03/11/2011

@author: friend
'''

def returnMegasenaFieldLongNamesStr():
  return '''Concurso
Data Sorteio
1ª Dezena
2ª Dezena
3ª Dezena
4ª Dezena
5ª Dezena
6ª Dezena
Arrecadacao_Total
Ganhadores_Sena
Rateio_Sena
Ganhadores_Quina
Rateio_Quina
Ganhadores_Quadra
Rateio_Quadra
Acumulado
Valor_Acumulado
Estimativa_Prêmio
Acumulado_Natal'''

def getDBFieldLongNames():
  megasenaFieldNames = returnMegasenaFieldLongNamesStr().split('\n')
  return megasenaFieldNames

def mappingHtmlColumnsToSqlColumns():
  # html name versus sql name
  htmlColumns = '''
  
  '''
  return htmlColumns

   
