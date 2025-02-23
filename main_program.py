import csv
import os
import time

# example directory
SHARED_DIR = 'Microservice_A'
QUERY_FILE = os.path.join(SHARED_DIR, 'query.csv')
RESPONSE_FILE = os.path.join(SHARED_DIR, 'response.csv')

if not os.path.exists(SHARED_DIR):
    os.makedirs(SHARED_DIR)

def write_query(value):
    """
    writes our csv file that contains our query value
    
    contains the 'value' header and the row containing user input
    """
    with open(QUERY_FILE, 'w', newline='') as csvfile:
        fieldnames = ['value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': value})
    print(f"Query written with value: {value}")

def read_response():
    """this reads and prints our csv file response"""
    if os.path.exists(RESPONSE_FILE):
        with open(RESPONSE_FILE, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            print("Received response:")
            for row in reader:
                print(row)
        # remove response file after reading, this is entirely optional
        os.remove(RESPONSE_FILE)
    else:
        print("Response file not found.")

# example usage:
# change value to test different scenarios for your project (different civ queries), or different leader queries
# write_query('Russia')  # civilization query
# write_query('Catherine')  # leader query

# response generation wait
while not os.path.exists(RESPONSE_FILE):
    print("Waiting for response...")
    time.sleep(1)

# response display
read_response()
