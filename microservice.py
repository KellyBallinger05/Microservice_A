import csv
import os
import time
import mysql.connector

# example file paths, change as needed
SHARED_DIR = 'Microservice_A'
QUERY_FILE = os.path.join(SHARED_DIR, 'query.csv')
RESPONSE_FILE = os.path.join(SHARED_DIR, 'response.csv')


if not os.path.exists(SHARED_DIR):
    os.makedirs(SHARED_DIR)

# query 1
query1 = """
SELECT 
    Leaders.LeaderName,
    GROUP_CONCAT(DISTINCT Civilizations.CivName),
    Leaders.LeaderBonus,
    GROUP_CONCAT(DISTINCT UniqueUnits.UnitName),
    GROUP_CONCAT(DISTINCT YieldTags.YieldName),
    GROUP_CONCAT(DISTINCT CustomTags.CustomTagName)
FROM 
    Leaders
LEFT JOIN 
    LeaderCivDetails ON Leaders.LeaderID = LeaderCivDetails.LeaderID
LEFT JOIN 
    Civilizations ON LeaderCivDetails.CivName = Civilizations.CivName
LEFT JOIN 
    UnitCivDetails ON Civilizations.CivName = UnitCivDetails.CivName
LEFT JOIN 
    UniqueUnits ON UnitCivDetails.UnitName = UniqueUnits.UnitName
LEFT JOIN 
    YieldTagsDetails ON Leaders.LeaderID = YieldTagsDetails.LeaderID
LEFT JOIN 
    YieldTags ON YieldTagsDetails.YieldTagName = YieldTags.YieldName
LEFT JOIN 
    CustomTagsDetails ON Leaders.LeaderID = CustomTagsDetails.LeaderID
LEFT JOIN 
    CustomTags ON CustomTagsDetails.CustomTagName = CustomTags.CustomTagName
WHERE 
    Leaders.LeaderName = %s
GROUP BY 
    Leaders.LeaderName, Leaders.LeaderBonus;
"""

# query 2
query2 = """
SELECT 
    Leaders.LeaderName
FROM 
    Leaders
JOIN 
    LeaderCivDetails ON Leaders.LeaderID = LeaderCivDetails.LeaderID
JOIN 
    Civilizations ON LeaderCivDetails.CivName = Civilizations.CivName
WHERE 
    Civilizations.CivName = %s;
"""

def process_query(query_data):
    """ this function processes the query csv and returns the string"""
    # assume the csv has a single column
    value = query_data.get('value', '').strip()
    if not value:
        return [['Error'], ['No query value provided']]

    return value


def execute_query(value):
    """
    query execution, result is returned as a list of rows
    if the user input is a civilization name, the microservice will return all leaders of that civilization,
    if the user input is a leader name, the microservice will return details for that leader:
      LeaderName, Civilizations, LeaderBonus, UniqueUnit, YieldTagName, CustomTagName.
    """
    leader_name, civ_name = value, value

    data_cursor.execute(query1, (leader_name,))
    result1 = data_cursor.fetchall()

    data_cursor.execute(query2, (civ_name,))
    result2 = data_cursor.fetchall()

    result = result1 + result2

    # if result is empty, return an error message
    if not result:
        result.append(['error'])
        result.append([f"query not found in database: {value}"])

    return result


def make_connection():
    """tries to open the mysql connection"""
    # try to connect tothe local mysql database
    try:
        global data_connection, data_cursor
        data_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1720',
            database='civ'
        )
        data_cursor = data_connection.cursor()
    except mysql.connector.Error as err:
        print(f"error connecting to the database: {err}")
        return
    return


def monitor_queries():
    """this monitors our directory for a new query fie"""
    
    print("Microservice started, monitoring for queries...")
    while True:
        if os.path.exists(QUERY_FILE):
            print("Query file found, processing...")
            with open(QUERY_FILE, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                query_data = next(reader)  # one query per file (assumption)
            
            # query processed based on the input value
            value = process_query(query_data)

            # result is processed, errors are handled
            if isinstance(value, str):
                result = execute_query(value)
            else:
                result = value

            # result is written to our response file
            with open(RESPONSE_FILE, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in result:
                    writer.writerow(row)
            
            # OPTIONAL file removal after processing. If you do not want the file to be removed, you can comment this out during implementation and choose what works for you.
            os.remove(QUERY_FILE)
            print("Query processed and response was successfully written.")
        time.sleep(1)


if __name__ == '__main__':
    make_connection()
    monitor_queries()
