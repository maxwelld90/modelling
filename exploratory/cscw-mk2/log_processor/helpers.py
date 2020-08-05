import re
import pymongo
import configparser
from bson.objectid import ObjectId

def load_config_dict(path):
    """
    Loads the configuration file using a ConfigParser, and returns the object.
    """
    config = configparser.ConfigParser()
    config.read(path)

    return config


def get_groups(config):
    """
    Returns a list of group IDs to use.
    The source is taken from BasicConfig/GroupsPath in the configuration file.
    """
    groups_path = config['BasicConfig']['GroupsPath']
    groups = []

    with open(groups_path, 'r') as f:
        for line in f:
            line = line.strip()
            groups.append(line)

    return groups


def get_topics(config):
    """
    Returns a list of topics, extracted from the configuration passed through.
    """
    topics_config = config['BasicConfig']['Topics']
    return re.split('\W+', topics_config)


def get_database_connection(config):
    """
    Returns a PyMongo object, given the configuration passed through.
    """
    host = config['MongoConfig']['Host']
    port = int(config['MongoConfig']['Port'])
    database_name = config['MongoConfig']['Database']

    client = pymongo.MongoClient(host, port)
    database = client[database_name]

    return database


def get_data_filter(config, context):
    """
    Given a configuration, returns a reference to the filter provided.
    Essentially, this is a wee factory function.
    If no filter is provided, the SimpleFilter is used.
    If a parameter called 'context' is provided, it is ignored.
    """
    filters_module = __import__('log_processor.filters', fromlist=['object'])
    parameters = {'context': context}

    try:
        filter_name = config['FilterConfig']['FilterName']
    except KeyError:
        return getattr(filters_module, 'SimpleFilter')()

    for key in config['FilterConfig'].keys():
        if (key.lower() == 'filtername' or key.lower() == 'context'):
            continue
        
        parameters[key] = config['FilterConfig'][key]
    
    filter_class = getattr(filters_module, filter_name)
    return filter_class(**parameters)


def get_group_users(database, groups, group_id):
    """
    Given a dictionary of group information, returns a dictionary of user details.
    User IDs are keys, and the role assigned to the user is the value.
    """
    groups_collection = database.groups
    group_info = groups_collection.find_one({'_id': ObjectId(group_id)})
    users = {}

    for user in group_info['members']:
        users[user['userId']] = user['role']
    
    return users