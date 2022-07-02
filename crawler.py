#!/usr/bin/env python3
from dotenv import dotenv_values 
import itertools
import logging, time
import threading, asyncio
from core import get_db
db = get_db()
db.pages.drop()

config = dotenv_values(".env")
root_url = config['ROOT_NODE']
REC_I = 0
import httpx
START_TIME = time.time()
N_I = 0
async def scrape_page(page_url):
  global N_I
  print(f"{N_I} {REC_I} scrape_page: URL: {page_url}, time:{time.time() - START_TIME}s")
  try:
    limits = httpx.Limits(max_keepalive_connections=None, max_connections=None)
    async with httpx.AsyncClient(verify=False, follow_redirects=True, limits=limits) as client:
      r = await client.get(page_url)
    if r.status_code == 200:
      await urls_and_text(r)
    else: print(f"{N_I} {REC_I} Error: {page_url} status_code: {r.status_code}")
  except httpx.HTTPError as exc:
    print(f"{N_I} {REC_I} Error {exc} while requesting {exc.request.url}")
  N_I += 1
from bs4 import BeautifulSoup
async def urls_and_text(r):
  global REC_I
  soup = BeautifulSoup(r.text, 'html.parser')
  urls = soup.find_all('a')
  urls = [url.get('href') for url in urls]
  urls = my_url_parse(str(r.request.url), urls)
  text = soup.get_text()
  if len(urls)>1 and REC_I<2:
    REC_I+=1
    for url in urls:
      task = asyncio.create_task(scrape_page(url))
    await task
  if text:
    text = my_text_parse(text)
    save_to_db(str(r.request.url), text)
  else: print('None text')
import re
def my_text_parse(text):
    text = re.sub("\n+| +|\t+"," ", text)
    return text
import urllib
def my_url_parse(parPage, urls):
  gd_urls = list()
  done_paths = list()
  bad = ("jpg jpeg png mp4 m4a mov avi mpg ogg webm m4v m4p mpv mpg webp flv mpeg mp3 mkv gif" +
          "css js scss crt json rss sitemap stl").split(' ')
  for url in urls:
    o = urllib.parse.urlparse(url)
    if url and o.path.split('.')[-1] not in bad:
      if not o.scheme:
        url = urllib.parse.urljoin(parPage, url)
        o = urllib.parse.urlparse(url)
      if o.scheme in ['http', 'https'] and (dpath := o.netloc+o.path) not in done_paths:
        gd_urls.append(url)
        done_paths.append(dpath)
  return gd_urls
def save_to_db(url, text):
  inserted_id = db.pages.insert_one({url: text}).inserted_id
  print(f'Saved {url}, id {inserted_id}')

class node:
  def __init__(self, parent_node):
    self.url = url
    # Must be neighbours
    self.parents = [parent_node]
    self.childs = list()
class graph:
  def __init__(self, root_node):
    self.root = root_node
  def link(self, parent, child):
    parent.childs.append(child)
    child.parents.append(parent)
  def shortest_distance(from_node, to_node):
    if to_node in from_node.childs:
      return 1
    for ec in from_node.childs:
      if to_node in ec.childs:
        return 2

async def main():
  task = asyncio.create_task(
      scrape_page(root_url))
  await task
asyncio.run(main())
