#!/usr/bin/env python3
"""
commands/datamng/adhoctest_selenium_scrape.py
  Adhoctesting webscraping with Selenium.
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By




def extract_data(element):
  # get the 'img' element and extract the 'srcset' attribute
  img = element.find_element(By.TAG_NAME, "img").get_attribute("srcset")
  img = parse_img_url(img)
  # A>B means the B elements where A is the parent element.
  dietary_attrs = element.find_elements(By.CSS_SELECTOR, "div[class*='e-kz6gcj']>span")
  # if there aren't any, then 'dietary_attrs' will be None and 'if' block won't work
  # but if there are any dietary attributes, extract the text from them
  if dietary_attrs:
    dietary_attrs = [attr.get_attribute("textContent") for attr in dietary_attrs]
  else:
    # set the variable to None if there aren't any dietary attributes found.
    dietary_attrs = None
  # get the div>span elements where the parent is a 'div' element that
  # has 'e-k008qs' string in the 'class' attribute
  price = element.find_elements(By.CSS_SELECTOR, "div[class*='e-k008qs']>div>span")
  # extract the price text if we could find the price span
  if price:
    price = price[0].get_attribute("textContent")
  else:
    price = None
  name = element.find_element(By.CSS_SELECTOR, "span[class*='e-1kb3u2t']").get_attribute("textContent")
  size = element.find_element(By.CSS_SELECTOR, "div[class*='e-wfknno']").get_attribute("textContent")

  return {
    "price": price,
    "name": name,
    "size": size,
    "attrs": dietary_attrs,
    "img": img
  }


def parse_img_url(url):
  # get the first url
  url = url.split(', ')[0]
  # split it by '/'
  splitted_url = url.split('/')
  # loop over the elements to find where 'cloudfront' url begins
  for idx, part in enumerate(splitted_url):
    if 'cloudfront' in part:
      # add the HTTP scheme and concatenate the rest of the URL
      # then return the processed url
      return 'https://' + '/'.join(splitted_url[idx:])

    # as we don't know if that's the only measurement to take,
  # return None if the cloudfront couldn't be found
  return None


def scrape_via_selenium():
  # Define the Chrome webdriver options
  print('Define the Chrome webdriver options')
  options = webdriver.ChromeOptions()
  # set the Chrome webdriver to run in headless mode for scalability
  options.add_argument("--headless")
  # By default, Selenium waits for all resources to download before taking actions.
  # However, we don't need it as the page is populated with dynamically generated JavaScript code.
  options.page_load_strategy = "none"
  # Pass the defined options objects to initialize the web driver
  driver = Chrome(options=options)
  # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
  driver.implicitly_wait(5)
  url = "https://www.instacart.com/store/sprouts/collections/bread/872?guest=true"
  print(url)
  driver.get(url)
  print('wait 20 sec')
  time.sleep(20)
  content = driver.find_element(By.CSS_SELECTOR, "div[class*='e-14cjhfa'")
  breads = content.find_elements(By.TAG_NAME, "li")
  img = content.find_element(By.TAG_NAME, "img").get_attribute("srcset")
  img = parse_img_url(img)
# A>B means the B elements where A is the parent element.
  dietary_attrs = content.find_elements(By.CSS_SELECTOR, "div[class*='e-kz6gcj']>span")
  # if there aren't any, then 'dietary_attrs' will be None and 'if' block won't work
  # but if there are any dietary attributes, extract the text from them
  if dietary_attrs:
    dietary_attrs = [attr.get_attribute("textContent") for attr in dietary_attrs]
  else:
    # set the variable to None if there aren't any dietary attributes found.
    dietary_attrs = None
  # get the div>span elements where the parent is a 'div' element that
  # has 'e-k008qs' string in the 'class' attribute
  price = content.find_elements(By.CSS_SELECTOR, "div[class*='e-k008qs']>div>span")
  # extract the price text if we could find the price span
  if price:
    price = price[0].get_attribute("textContent")
  else:
    price = None
  name = content.find_element(By.CSS_SELECTOR, "span[class*='e-1kb3u2t']").get_attribute("textContent")
  size = content.find_element(By.CSS_SELECTOR, "div[class*='e-wfknno']").get_attribute("textContent")
  data = []
  for bread in breads:
    extracted_data = extract_data(bread)
    print('extracted_data', extracted_data)
    data.append(extracted_data)
  df = pd.DataFrame(data)
  print('Saving result.csv via pandas ')
  df.to_csv("result.csv", index=False)


def process():
  pass


def adhoc_test():
  print('scrape_via_selenium()')
  scrape_via_selenium()


if __name__ == '__main__':
  """
  process()
  """
  adhoc_test()
