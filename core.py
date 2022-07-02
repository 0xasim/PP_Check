from pymongo import MongoClient
def get_db():
  CONNECTION_STRING = "mongodb://127.0.0.1:27017/"
  client = MongoClient(CONNECTION_STRING)
  return client.pp_rank_db
