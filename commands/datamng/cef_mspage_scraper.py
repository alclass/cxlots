#!/usr/bin/env python3
"""
commands/datamng/cef_mspage_scraper.py
  Scrapes the webpage that contains the drawings of each 'concurso'.

Obs: the dozen drawings is rendered by Javascript, so it cannot be directly scraped.
     At the time of this writing, an attempt is to use 'selenium' for trying to fetch the drawings.

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]
"""
import datetime
import os.path
import requests
import local_settings as ls
MS_PAGE_URL = "https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx"
MS_FILENAME = "cef_ms_page.html"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'


def get_cef_ms_filepath():
  folderpath = ls.get_appsdata_basedirpath()
  filepath = os.path.join(folderpath, MS_FILENAME)
  return filepath


class CefMsScraper:

  def __init__(self):
    self.html_page = None
    self.page_already_downloaded = False

  @property
  def cef_ms_page_localfilename(self):
    return MS_FILENAME

  def has_page_already_been_downloaded(self):
    filepath = get_cef_ms_filepath()
    if os.path.isfile(filepath):
      self.page_already_downloaded = True
      return True
    self.page_already_downloaded = False
    return False

  def download(self):
    if self.has_page_already_been_downloaded():
      scrmsg = f"Filename '{self.cef_ms_page_localfilename}' has already been downloaded"
      print(scrmsg)
      return False
    print('Downloading', MS_PAGE_URL, 'with UA', USER_AGENT)
    headers = {'User-Agent': USER_AGENT}
    req = requests.get(MS_PAGE_URL, headers=headers)
    self.html_page = req.text
    return True

  def save_page_locally(self):
    filepath = get_cef_ms_filepath()
    print('Saving locally', filepath)
    fd = open(filepath, 'w', encoding='utf8')
    fd.write(str(self.html_page))
    fd.close()

  def process(self):
    if self.download():
      self.save_page_locally()

  def __str__(self):
    today = datetime.date.today()
    strdate = str(today)
    outstr = f"Filename '{self.cef_ms_page_localfilename}' on {strdate}"
    return outstr


def process():
  pass


def adhoc_test():
  co = CefMsScraper()
  co.process()


if __name__ == '__main__':
  """
  process()
  """
  adhoc_test()
