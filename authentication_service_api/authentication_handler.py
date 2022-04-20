from time import sleep
import uuid
from pymongo import MongoClient

client = MongoClient('172.17.0.2:27017')
configuration_db = client['user_data']
configuration_col = configuration_db['user_data']


#TODO
def flogin(): 
    sleep