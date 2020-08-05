from enum import Enum
from log_processor.helpers import get_data_filter, get_group_users

class States(Enum):
    QUERY = 1
    RESULTS = 2
    RECENT = 3
    SAVED = 4


def main(config, groups, topics, database):
    """
    Does the magic!
    """
    logs_collection = database.logs  # Assuming that the logs exist in the "logs" collection.
    do_aggregate_groups = config['BasicConfig'].getboolean('AggregateGroups')  # None if not provided!

    for group_id in groups:
        users = get_group_users(database, groups, group_id)

        for user_id in users:
            for topic in topics:
                session_string = f'{group_id}-{topic}-S1'
                log_entries = logs_collection.find({'sessionId': session_string, 'userId': user_id})

                session = SearchSession(config, group_id, user_id, topic, log_entries)
                session.process()


class SearchSession(object):
    """
    Represents a search session, including counts of all the relevant events that occur.
    Note that each session represents an individual user's interactions.
    """
    def __init__(self, config, group_id, user_id, topic, log_entries):
        self.group_id = group_id
        self.user_id = user_id
        self.topic = topic
        self.log_entries = log_entries

        self.__current_state = None
        self.__context = {
            'start_time': None,
        }

        self.__filter = get_data_filter(config, self.__context)
    
    def process(self):
        for entry in self.log_entries:
            print(entry)
        
        # Work on the processing function.
        # Consider the state, events, etc.
        # Can we have a model class that we can inject in?
        # i.e. it keeps track of all the states and transitions.