import uuid
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient("mongodb+srv://bruno:123@cloudcomputing.2raxg.mongodb.net/CloudComputing?retryWrites=true&w=majority",server_api=ServerApi('1'))
configuration_db = client['configuration_data']
configuration_col = configuration_db['configuration_data']

def create_configuration(username, body):
    print(body)
    configuration_object = {}
    configuration_object['user'] = username
    configuration_object['uuid'] = str(uuid.uuid1())
    configuration_object['parts'] = body['parts']
    result = configuration_col.insert_one(configuration_object)
    print(result)
    return configuration_object['uuid']

def get_configuration_by_id(configurationId):
    result = configuration_col.find_one({'uuid': configurationId})
    print(configuration_col.find_one({'uuid': configurationId}))
    return create_message_object(result)

def update_configuration(configurationId, body):
    current = configuration_col.find_one({'uuid': configurationId})
    configuration_object = {}
    configuration_object['user'] = current['user']
    configuration_object['uuid'] = current['uuid']
    configuration_object['parts'] = body['parts']
    result = configuration_col.update_one({'uuid': configurationId}, configuration_object)
    return current['configuration_id']

def get_configuration_by_user_id(username):
    search_result = configuration_col.find({'user': username})
    conf_list = []
    for result in search_result:
        conf_list.append(create_message_object(result, username))
    return conf_list

def create_message_object(db_object, user='error'):
    if db_object is None:
        return {'error': user}
    return {'user':db_object['user'], 'uuid': db_object['uuid'], 'parts': db_object['parts']}


if __name__ == '__main__':
    print(get_configuration_by_user_id('jan'))