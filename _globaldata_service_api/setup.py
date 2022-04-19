import json
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

dataset_path = '../datasets/globaldata/'
client = MongoClient("mongodb+srv://bruno:123@cloudcomputing.2raxg.mongodb.net/CloudComputing?retryWrites=true&w=majority",server_api=ServerApi('1'))
clickfield_db = client['globaldata_data']
clickfield_col = clickfield_db['globaldata_data']

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