#!/usr/bin/env python3
"""
fs/dbfs/datafilefs/from_wks/ms_excel_read.py

"""
import glob
import os
import pandas
import pandas as pd

import local_settings as ls
filename_to_interpolate = "megasena_asloterias-com-br_ate_conc{nconc}_srt.xlsx"
lots_data_middlepath = 'dados/asloterias-com-br'


def get_ms_dados_folderpath():
  data_basedirpath = ls.get_data_basedirpath()
  lots_data_folderpath = os.path.join(data_basedirpath, lots_data_middlepath)
  return lots_data_folderpath


def get_ms_history_excelfilepath():
  folderpath = get_ms_dados_folderpath()
  sufix_files = sorted(glob.glob(folderpath + '/*_srt.xlsx'))
  if len(sufix_files) > 0:
    return sufix_files[-1]
  return None


def get_pandas_df_from_ms_history_excelfile(excel_filepath=None):
  """
  Concurso	Data	bola 1	bola 2	bola 3	bola 4	bola 5	bola 6

  Args:
    excel_filepath:

  Returns:
  """
  if excel_filepath is None:
    excel_filepath = get_ms_history_excelfilepath()
  columns = ['nconc', 'date', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6']
  df = pd.read_excel(excel_filepath, header=None, names=columns)
  df = df.dropna()
  # print(df.to_string())
  return df

def adhoctest():
  pass

def process():
  fp = get_ms_history_excelfilepath()
  df = get_pandas_df_from_ms_history_excelfile(fp)
  # print(df)


if __name__ == '__main__':
  adhoctest()
  process()
