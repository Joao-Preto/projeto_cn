import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient("mongodb+srv://bruno:123@cloudcomputing.2raxg.mongodb.net/CloudComputing?retryWrites=true&w=majority",server_api=ServerApi('1'))
chiptec_db = client['chiptec_data']
chiptec_col = chiptec_db['chiptec_data']

def get_part(sku):
    mongo_result = chiptec_col.find_one({'sku': sku})
    return {'sku': mongo_result['sku'], 'price': mongo_result['price']}

def get_parts(sku_list):
    price_list = []
    for sku in sku_list:
        price_list.append(get_part(sku))
    return price_list

def update_prices(body):
    chiptec_col.insert_many(json.loads(body))
