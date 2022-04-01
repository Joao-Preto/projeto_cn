from unittest import result
from pymongo import MongoClient

client = MongoClient('172.17.0.2:27017')
configuration_db = client['configuration_data']
configuration_col = configuration_db['configuration_data']

def create_configuration(username, body):
    body['user'] = username
    result = configuration_col.insert_one(body)
    return result.inserted_id

def get_configuration_by_id(configurationId):
    return configuration_col.find_one({'ObjectId': configurationId})

def update_configuration(configurationId, body):
    current = configuration_col.find_one({'ObjectId': configurationId})
    body['user'] = current['user']
    result = configuration_col.update_one({'ObjectId': configurationId}, body)
    return current['ObjectId']

def get_configuration_by_user_id(username):
    search_result = configuration_col.find({'user': username})
    conf_list = []
    for result in search_result:
        conf_list.append(result)
    return conf_list
