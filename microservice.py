import csv
import os
import time

# example file paths, change to what is necessary for you
SHARED_DIR = 'Microservice_A'
QUERY_FILE = os.path.join(SHARED_DIR, 'query.csv')
RESPONSE_FILE = os.path.join(SHARED_DIR, 'response.csv')

if not os.path.exists(SHARED_DIR):
    os.makedirs(SHARED_DIR)

# Example database, change as needed for your project
# civilization name is the key, our value is the leader names regarding civ queries
CIVILIZATION_DATA = {
    'Russia': ['Catherine', 'Peter'],
    'England': ['Elizabeth', 'Victoria']
}

# regarding leader queries, our key is the name and value is their details
LEADER_DATA = {
    'Catherine': {
        'LeaderName': 'Catherine',
        'Civilizations': 'Russia',
        'LeaderBonus': 'Extra diplomacy influence',
        'UniqueUnit': 'Cossack',
        'YieldTagName': 'Culture',
        'CustomTagName': 'Great Leader'
    },
    'Peter': {
        'LeaderName': 'Peter',
        'Civilizations': 'Russia',
        'LeaderBonus': 'Increased production',
        'UniqueUnit': 'Streltsy',
        'YieldTagName': 'Science',
        'CustomTagName': 'Innovator'
    },
    'Elizabeth': {
        'LeaderName': 'Elizabeth',
        'Civilizations': 'England',
        'LeaderBonus': 'Naval supremacy',
        'UniqueUnit': 'Redcoat',
        'YieldTagName': 'Gold',
        'CustomTagName': 'Explorer'
    },
    'Victoria': {
        'LeaderName': 'Victoria',
        'Civilizations': 'England',
        'LeaderBonus': 'Industrial bonus',
        'UniqueUnit': 'Musketeer',
        'YieldTagName': 'Production',
        'CustomTagName': 'Empire Builder'
    }
}

def process_query(query_data):
    """
    query processing, result is returned as a list of rows
    
    if the user input is a civilization name, the microservice will return all leaders of that civilization,
    if the user input is a leader name, the microservice will return details for that leader:
      LeaderName, Civilizations, LeaderBonus, UniqueUnit, YieldTagName, CustomTagName.
    """
    # as an example, assume our csv has a single column value that contains our string via your example you sent me on discord
    value = query_data.get('value', '').strip()
    result = []

    # check that our value matches a civilization 
    if value in CIVILIZATION_DATA:
        leaders = CIVILIZATION_DATA[value]
        if leaders:
            result.append(['LeaderName'])
            for leader in leaders:
                result.append([leader])
        else:
            result.append(['Error'])
            result.append([f"No leaders found for civilization: {value}"])
    # now, check that if it is a leader name thats in our local database
    elif value in LEADER_DATA:
        leader_info = LEADER_DATA[value]
        header = ['LeaderName', 'Civilizations', 'LeaderBonus', 'UniqueUnit', 'YieldTagName', 'CustomTagName']
        result.append(header)
        result.append([
            leader_info['LeaderName'],
            leader_info['Civilizations'],
            leader_info['LeaderBonus'],
            leader_info['UniqueUnit'],
            leader_info['YieldTagName'],
            leader_info['CustomTagName']
        ])
    else:
        result.append(['Error'])
        result.append([f"Query value not found in database: {value}"])
    
    return result

def monitor_queries():
    """this monitors our directory for a new query file"""
    print("Microservice started, monitoring for queries...")
    while True:
        if os.path.exists(QUERY_FILE):
            print("Query file found, processing...")
            with open(QUERY_FILE, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                query_data = next(reader)  # one query per file (assumption)
            
            # query processed based on the input value
            result = process_query(query_data)

            # result is written to our response file
            with open(RESPONSE_FILE, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in result:
                    writer.writerow(row)
            
            # query file is removed after processing
            os.remove(QUERY_FILE)
            print("Query processed and response was successfully written.")
        time.sleep(1)

if __name__ == '__main__':
    monitor_queries()
