# Communication Contract

## Overview

Microservice will accept query requests via the CSV files that are written to a directory as discussed. For example, locally for me I have a directory "Microservice_A" in which both the main program and microservice read and write out of. Client writes a query with the name query.csv, while the microservice monitors the same directory and processes the query. This is done by looking up the resulting data in the 'internal' database, while the results are written as a CSV file named response.csv.

## How to Programmatically REQUEST Data:

To request your data from the microservice, the program writes a query.csv CSV file to our directory. The CSV file contains a header named 'value' and a row that contains the query string, which can be:
- A civilization name like Russia or England, where the microservices pulls the leaders that are associated with those civializations.
- A leaders name, such as Catherine or Victoria, in which case the microservice will return the specified leader details that were given to me by the directions.

### Example call in Python
```Python
import csv
import os

# this is the shared directory and file paths
SHARED_DIR = 'Microservice_A'
QUERY_FILE = os.path.join(SHARED_DIR, 'query.csv)

# existance check
if not os.path.exists(SHARED_DIR):
   os.makedirs(SHARED_DIR)

def request_data(query_value):
   """
   this writes the query CSV file that contains our query value,
   CSV contains one header with one row of the user input.
   """
   with open(QUERY_FILE, 'w', newline='') as csvfile:
      fieldnames = ['value']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerow({'value': query_value})
   print(f"request sent with query: {query_value}")

# example
request_data('Russia')
```

## How to Programatically RECEIVE Data:
After the microservice processes the request, it will write the output to a CSV file named response.csv in the same shared directory. Program then retrieves this file and accesses the data:

1. **Monitoring the directory:**
   Checks for the existence of our response.csv file, must wait until microservice has successfully processed the request
2. **Reading the CSV File:**
   Once our response.csv is available (which should be near instant), it is opened and read using our CSV parse library, this file contains our resulting data:
   - A civilization query will include a CSV with a header such as LeaderName with a row containing that leader's name
   - A leader query will include a CSV with a header such as LeaderName, Civilizations, LeaderBonus, YieldTagName and CustomTagName.
3. **Processing our data:**
   After the file is read, our data is processed. Included in the code is an optional delete regarding the response file so you can continue querying without worrying about file management.

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
## UML Diagram
[![](https://mermaid.ink/img/pako:eNqVU1trwjAU_ivhPDlQsfXSmgdhKHsThsIGoy9ZetRgTbpcdE7874tap53iXCCQc5LvwhfOBrhKESgY_HAoOQ4Em2q2SCTxK2faCi5yJi3pZwKlvew_iQzN2li8ghkKrpVBvRQcE3m4P_DUer0TkJJXLSySBLwHva5zs0yAVFbCzsi-Q5Ysc_hwIDjhap7lQEfJI59LtcownSKZ-BeEa2RWqEL13Mkv7aGSwipNJn6XHPyJHKBFbv8JGiFL74Ccl5Q8a8XRmCKNSqbU3OVESJIyy96ZOWZzQ_cYsUaTK2mwlLJvusyaqwmXnVzkvNrx3vja_gz5vAi3rH3rOy98TpST6Q2ZItb7FUZonZakP37Zh5hIqMIC9YKJ1I_DZgdNwM5wgQns_KRMz3eMW_-OOavGa8mBWu2wClq56QzohGXGVy73hMdB-un6gXhTqlQD3cAn0DAK6u1mNwzCsNWOgziuwhpop-7PUSdsNcO4E7Sb8bYKX3uCRr3biYKg0Wp1o6AZNcL29htTfkgn?type=png)](https://mermaid.live/edit#pako:eNqVU1trwjAU_ivhPDlQsfXSmgdhKHsThsIGoy9ZetRgTbpcdE7874tap53iXCCQc5LvwhfOBrhKESgY_HAoOQ4Em2q2SCTxK2faCi5yJi3pZwKlvew_iQzN2li8ghkKrpVBvRQcE3m4P_DUer0TkJJXLSySBLwHva5zs0yAVFbCzsi-Q5Ysc_hwIDjhap7lQEfJI59LtcownSKZ-BeEa2RWqEL13Mkv7aGSwipNJn6XHPyJHKBFbv8JGiFL74Ccl5Q8a8XRmCKNSqbU3OVESJIyy96ZOWZzQ_cYsUaTK2mwlLJvusyaqwmXnVzkvNrx3vja_gz5vAi3rH3rOy98TpST6Q2ZItb7FUZonZakP37Zh5hIqMIC9YKJ1I_DZgdNwM5wgQns_KRMz3eMW_-OOavGa8mBWu2wClq56QzohGXGVy73hMdB-un6gXhTqlQD3cAn0DAK6u1mNwzCsNWOgziuwhpop-7PUSdsNcO4E7Sb8bYKX3uCRr3biYKg0Wp1o6AZNcL29htTfkgn)
