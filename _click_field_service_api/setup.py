import json
import os
from pymongo import MongoClient

dataset_path = '../datasets/clickfield/'
client = MongoClient('172.17.0.2:27017')
clickfield_db = client['clickfield_data']
clickfield_col = clickfield_db['clickfield_data']

def save_product_from_file(filepath):
    file = open(filepath, 'r')    
    product = json.load(file)
    clickfield_col.insert_one(product)
    
def create_database():
    file_iterator = os.scandir(dataset_path)
    for filename in file_iterator:
        save_product_from_file(filename)
    
    
if __name__ == '__main__':
    create_database() 