from pymongo import MongoClient

client = MongoClient('172.17.0.3:27017')
assismatica_db = client['assismatica_data']
assismatica_col = assismatica_db['assismatica_data']

def get_part(sku):
    return assismatica_col.find_one({'sku': sku})

def get_parts(sku_list):
    price_list = []
    for sku in sku_list:
        price_list.append(get_part(sku))
    return price_list

def update_prices(data):
    assismatica_col.insert_many(data)