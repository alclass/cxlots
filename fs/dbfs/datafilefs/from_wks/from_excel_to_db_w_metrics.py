#!/usr/bin/env python3
"""
fs/dbfs/datafilefs/from_wks/from_excel_to_db_w_metrics.py

"""
import fs.dbfs.datafilefs.from_wks.ms_excel_read as mer  # get_pandas_df_from_ms_history_excelfile
import fs.jogosfs.jogos_functions as jf
import fs.jogosfs.jogos_metrics as jm


def get_data_n_build_metrics():
  df = mer.get_pandas_df_from_ms_history_excelfile()
  i = 0
  for row in df.iterrows():
    i += 1
    r = row[1]  # the series part
    nconc = r.nconc
    tupledozens = r.d1, r.d2, r.d3, r.d4, r.d5, r.d6
    jmetr = jm.JogoMetrics(nconc, tupledozens)
    print(jmetr)
    if i > 3:
      break


def adhoctest():
  pass


def process():
  get_data_n_build_metrics()


if __name__ == '__main__':
  adhoctest()
  process()
