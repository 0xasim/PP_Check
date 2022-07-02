#!/usr/bin/env python3
from collections import Counter
def search(query):
  query = query.strip().split(' ')
  results = list()
  for w in query:
    matches = db.inverted_index.find({'word': w})
    results.append(list(matches))
  if results[0]:
    urls = list()
    for er in results:
      urls = urls + er[0]['urls']
    points = Counter(urls).most_common()
    print(points)

if __name__ == '__main__':
  from core import get_db
  db = get_db()
  while True:
    query = input('Search: ')
    search(query)
