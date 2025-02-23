# Communication Contract

## Overview

Microservice will accept query requests via the CSV files that are written to a directory as discussed. For example, locally for me I have a directory "Microservice_A" in which both the main program and microservice read and write out of. Client writes a query with the name query.csv, while the microservice monitors the same directory and processes the query. This is done by looking up the resulting data in the 'internal' database, while the results are written as a CSV file named response.csv.

## How to Programmatically REQUEST Data:

To request your data from the microservice, the program writes a query.csv CSV file to our directory. The CSV file contains a header named 'value' and a row that contains the query string, which can be:
- A civilization name like Russia or England, where the microservices pulls the leaders that are associated with those civializations.
- A leaders name, such as Catherine or Victoria, in which case the microservice will return the specified leader details that were given to me by the directions.

## How to Programatically RECEIVE Data:
After the microservice processes the request, it will write the output to a CSV file named response.csv in the same shared directory. Program then retrieves this file and accesses the data:

1. **Monitoring the directory:**
   Checks for the existence of our response.csv file, must wait until microservice has successfully processed the request
2. **Reading the CSV File:**
   Once our response.csv is available (which should be near instant), it is opened and read using our CSV parse library, this file contains our resulting data:
   - A civilization query will include a CSV with a header such as LeaderName with a row containing that leader's name
   - A leader query will include a CSV with a header such as LeaderName, Civilizations, LeaderBonus, YieldTagName and CustomTagName.
3. **Processing our data:**
   After the file is reader, our data is processed. Included in the code is an optional delete regarding the response file so you can continue querying without worrying about file management.

### Example Call in Python

```python
import csv
import os
import time

SHARED_DIR = 'Microservice_A'
RESPONSE_FILE = os.path.join(SHARED_DIR, 'response.csv')

def receive_data():
  """
  This is what checks for our response.csv file, reads the contents and returns the data as a list of rows.
  """
  while not os.path.esists(RESPONSE_FILE):
    print("waiting for a response..")
    time.sleep(1)

# CSV data is read and stored
  data = []
  with open(RESPONSE_FILE, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      data.append(row)

  print("Received data:")
  for row in data:
    print(row)

  # this optionally removes the response file after it is read, like mentioned above
  os.remove(RESPONSE_FILE)
  return data

if __name__ == '__main__':
  received_data = receive_data()
```
