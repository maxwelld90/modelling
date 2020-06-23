#
# Retrieves raw counts for movements between states from CSCW log data.
# 
# Author: David Maxwell
# Date: 2020-06-11
#


import sys
import pymongo

import itertools
from enum import Enum


def get_groups(groups_filename):
    """
    Opens the groups file, and returns a list of each group ID (line-by-line).
    """
    f = open(groups_filename, 'r')
    groups = []

    for line in f:
        line = line.strip()
        groups.append(line)

    f.close()
    return groups


def main(database, groups, topics):
    """
    Extracts the log entries, and filters them by the group specificed.
    """
    logs = database.logs

    for group_id in groups:
        for topic in topics:
            session_string = f'{group_id}-{topic}-S1'
            log_entries = logs.find({'sessionId': session_string})

            session = SearchSession(group_id, topic, log_entries)
            session.process()


class States(Enum):
    """

    """
    QUERY = 1
    RESULTS = 2
    RECENT = 3
    SAVED = 4

def get_transition_combinations():
    transition_orders = []
    combinations = list(itertools.combinations(States, 2))

    for combination in combinations:
        transition_orders.append((combination[0], combination[1]))
        transition_orders.append((combination[1], combination[0]))
    
    return transition_orders


str_mappings = {
    States.QUERY: 'query',
    States.RESULTS: 'results',
    States.RECENT: 'recent',
    States.SAVED: 'saved',
}

OUTPUT = [
    {'raw': [States.QUERY, States.RESULTS, States.RECENT, States.SAVED]},
    {'transitions': get_transition_combinations()}
]

HEADER = "group_id,topic,raw_query,raw_results,raw_recent,raw_saved"

for combination in get_transition_combinations():
    start = str_mappings[combination[0]]
    end = str_mappings[combination[1]]
    HEADER = f"{HEADER},{start}2{end}"

print(HEADER)

class SimpleFilter(object):

    def __init__(self, context):
        self._context = context

    def include(self, log_entry):
        return True


class FirstFiveMinutesFilter(SimpleFilter):
    
    def __init(self, context):
        super().__init__(self, context)
    
    def include(self, log_entry):
        start_time = self._context['start_time']

        if start_time is None or (log_entry['date'] - start_time).seconds < 300:
            return True

        return False

class SecondFiveMinuteFilter(SimpleFilter):
    
    def __init(self, context):
        super().__init__(self, context)
    
    def include(self, log_entry):
        start_time = self._context['start_time']
        
        if start_time is None or ((log_entry['date'] - start_time).seconds > 300 and (log_entry['date'] - start_time).seconds < 600):
            return True

        return False


class SearchSession(object):
    """

    """
    def __init__(self, group_id, topic, log_entries):
        """

        """
        self.group_id = group_id
        self.topic = topic
        self.log_entries = log_entries
        

        self.__current_state = None
        self.__context = {
            'start_time': None,
            'current_state': None,
        }

        self.filter = SecondFiveMinuteFilter(self.__context)

        self.__mapping = {
            'QUERYSUGGESTIONS_GET': States.QUERY,
            'SEARCHRESULT_HOVERENTER': States.RESULTS,
            'QUERYHISTORY_HOVERENTER': States.RECENT,
            'BOOKMARK_HOVERENTER': States.SAVED,
        }

        self.__initialise_counters()
    

    def __initialise_counters(self):
        """

        """
        self.__counts = {}
        self.__counts['raw'] = {}

        for state in States:
            self.__counts['raw'][state] = 0
        
        combinations = get_transition_combinations()
        self.__counts['transitions'] = []

        for combination in combinations:
            transition = {'start': combination[0],
                          'end': combination[1],
                          'count': 0}
            
            transition2 = {'start': combination[1],
                          'end': combination[0],
                          'count': 0}
            
            self.__counts['transitions'].append(transition)
            self.__counts['transitions'].append(transition2)


    def increment_transition(self, new_state):
        """

        """
        old_state = self.__context['current_state']
        transitions = self.__counts['transitions']

        for combination in transitions:
            if combination['start'] == old_state and combination['end'] == new_state:
                combination['count'] += 1
                break
    
    def find_transition(self, start_state, end_state):
        for entry in self.__counts['transitions']:
            if entry['start'] == start_state and entry['end'] == end_state:
                return entry
        
        return None

    def switch_state(self, new_state):
        """

        """
        if new_state != self.__context['current_state']:
            self.__counts['raw'][new_state] += 1
            self.increment_transition(new_state)
        
        self.__context['current_state'] = new_state


    def generate_report(self):
        combined_str = ""

        for entry in OUTPUT:
            for key in entry.keys():
                if key == 'transitions':
                    for combination in entry[key]:
                        combined_str = f"{combined_str},{self.find_transition(combination[0], combination[1])['count']}"
                    continue
                    
                for value in entry[key]:
                    combined_str = f"{combined_str},{self.__counts[key][value]}"
        
        combined_str = f"{self.group_id},{self.topic}{combined_str}"
        print(combined_str)

    def __update_start_time(self, entry):
        if self.__context['start_time'] is None:
            self.__context['start_time'] = entry['date']

    def process(self):
        """

        """
        for entry in self.log_entries:
            if self.filter.include(entry):
                event = entry['event']
                date = entry['date']

                if event in self.__mapping:
                    self.switch_state(self.__mapping[event])
                
                self.__update_start_time(entry)

        self.generate_report()
            


if __name__ == '__main__':
    mongo_client = pymongo.MongoClient('localhost', 27017)
    database = mongo_client['searchx-cikm']
    topics = ['341', '367', '650']
    groups = get_groups('/Users/David/Desktop/groups_single.txt')
    
    main(database, groups, topics)