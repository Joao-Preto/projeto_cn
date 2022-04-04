from pymongo import MongoClient

client = MongoClient('172.17.0.2:27017')
clickfield_db = client['clickfield_data']
clickfield_col = clickfield_db['clickfield_data']

def get_part(sku):
    return clickfield_col.find_one({'sku': sku})

def get_parts(sku_list):
    price_list = []
    for sku in sku_list:
        price_list.append(get_part(sku))
    return price_list

def update_prices(data):
    clickfield_col.insert_many(data)