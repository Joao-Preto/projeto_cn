import json
from pymongo import MongoClient

client = MongoClient('172.17.0.2:27017')
globaldata_db = client['globaldata_data']
globaldata_col = globaldata_db['globaldata_data']

def get_part(sku):
    mongo_result = globaldata_col.find_one({'sku': sku})
    return {'sku': mongo_result['sku'], 'price': mongo_result['price']}

def get_parts(sku_list):
    price_list = []
    for sku in sku_list:
        price_list.append(get_part(sku))
    return price_list

def update_prices(body):
    globaldata_col.insert_many(json.loads(body))