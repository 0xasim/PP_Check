#!/usr/bin/env python3
from core import get_db
db = get_db()
db.inverted_index.drop()
pages = list(db.pages.find({}))

bad_words = set(""". , ; : ' " / * ! @ # $ % ^ & * ( ) - _ + = [ ] { } \\ | ? ` ~""".split(' '))
inverted_index = list()
done_words = dict()
for page in pages:
  url = list(page.keys())[1]
  words = page[url].lower().split(' ')
  for i, w in enumerate(words):
    if w and w not in bad_words:
      if w not in done_words:
        inverted_index.append({'word': w, 'urls': [url], 'indexes': [i]})
        done_words[w] = len(inverted_index)-1
      elif w in words:
        if url not in inverted_index[done_words[w]]['urls']:
          inverted_index[done_words[w]]['urls'].append(url)
          inverted_index[done_words[w]]['indexes'].append(i)
          done_words[w] = len(inverted_index) - 1

print(list(done_words.keys()))
inserted_id = db.inverted_index.insert_many(inverted_index).inserted_ids
