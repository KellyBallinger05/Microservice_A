""" 
This is simply a testing main program to better show the functionality of the microservice, 
per Canvas instructions - this should not be used nor is it required to be used to
use the microservice.
"""

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


def main():
    # prompt user for a query 
    value = input("Enter query value: ")
    
    write_query(value)
    
    # wait for the microservice 
    print("waiting...")
    while not os.path.exists(RESPONSE_FILE):
        time.sleep(1)

    # response display
    read_response()


if __name__ == '__main__':
    main()