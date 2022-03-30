from http import client
from pymongo import MongoClient

client = MongoClient('172.17.0.3:27017')
clickfield_db = client['clickfield_data']
clickfield_col = clickfield_db['clickfield_data']
def get_part(sku):
    return clickfield_col.find_one({'sku': sku})

def get_parts(sku_list):
    price_list = []
    for sku in sku_list:
        price_list.append(get_part(sku))
    return price_list