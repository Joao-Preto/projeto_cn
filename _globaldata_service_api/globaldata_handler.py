from pymongo import MongoClient

client = MongoClient('172.17.0.2:27017')
globaldata_db = client['globaldata_data']
globaldata_col = globaldata_db['globaldata_data']

def get_part(sku):
    return globaldata_col.find_one({'sku': sku})

def get_parts(sku_list):
    price_list = []
    for sku in sku_list:
        price_list.append(get_part(sku))
    return price_list

def update_prices(data):
    globaldata_col.insert_many(data)