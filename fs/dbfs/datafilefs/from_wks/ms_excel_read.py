#!/usr/bin/env python3
"""
fs/dbfs/datafilefs/from_wks/ms_excel_read.py

"""
import glob
import os
import pandas as pd
import local_settings as ls
filename_to_interpolate = "megasena_asloterias-com-br_ate_conc{nconc}_sorteio.xlsx"
glob_asterisco_sorteio_xlsx = "*_sorteio.xlsx"
aslots_foldername_u_appsdatafolder = 'DB asloterias-com-br et al'


def get_ms_dados_folderpath():
  appsdata_basedirpath = ls.get_appsdata_basedirpath()
  lots_data_folderpath = os.path.join(appsdata_basedirpath, aslots_foldername_u_appsdatafolder)
  return lots_data_folderpath


def get_ms_history_excelfilepath():
  folderpath = get_ms_dados_folderpath()
  sufix_files = sorted(glob.glob(folderpath + '/' + glob_asterisco_sorteio_xlsx))
  if len(sufix_files) > 0:
    # the last item is also the most recent
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
  _, excel_filename = os.path.split(excel_filepath)
  scrmsg = f'Reading file {excel_filename}'
  print(scrmsg)
  columns = ['nconc', 'concdate', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6']
  df = pd.read_excel(excel_filepath, header=None, names=columns)
  df = df.dropna()
  # print(df.to_string())
  return df


def adhoctest():
  pass


def process():
  fp = get_ms_history_excelfilepath()
  df = get_pandas_df_from_ms_history_excelfile(fp)
  print(df.to_string())


if __name__ == '__main__':
  adhoctest()
  process()
