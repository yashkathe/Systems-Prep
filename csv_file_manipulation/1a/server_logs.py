"""
Task: Write a program to read server_logs.csv and perform the following:

    Calculate the average response time for each unique ACTION.
    Identify the USER_ID with the highest number of POST actions.
    Determine the most frequently accessed RESOURCE.

TIMESTAMP, USER_ID, ACTION, RESOURCE, RESPONSE_TIME_MS, HTTP_METHOD, STATUS_CODE, DEVICE_TYPE, BROWSER, IP_ADDRESS
"""

import csv
from collections import defaultdict

# -----------------------------------------------#
# 1 average response time for each unique ACTION #
# -----------------------------------------------#

avg_response = defaultdict(list)

with open('./server_logs.csv', 'r') as f:

    reader = csv.DictReader(f)
    # next(reader) # no need when DictReader is used

    for line in reader:
        action = line['ACTION']
        response_time = int(line['RESPONSE_TIME_MS'])
        avg_response[action].append(response_time)

avg_response = { k: sum(v)//len(v) for k, v in avg_response.items()}

print(avg_response)

# {'GET': 160, 'POST': 237, 'DELETE': 300, 'PUT': 260}

#----------------------------------------------------------------#
# 2 Identify the USER_ID with the highest number of POST actions #
#----------------------------------------------------------------#

freq_post = defaultdict(int)

with open('./server_logs.csv', 'r') as f:

    reader = csv.DictReader(f)

    for line in reader:
        action = line['ACTION']

        if action == 'POST':

            uid = line['USER_ID']

            freq_post[uid] += 1

print(freq_post)

#-------------------------------------------------#
# Determine the most frequently accessed RESOURCE #
#-------------------------------------------------#

freq_resource = defaultdict(int)

with open('./server_logs.csv', 'r') as f:

    reader = csv.DictReader(f)

    for line in reader:

        resource = line['RESOURCE']

        freq_resource[resource] += 1

max_resource = max(freq_resource.items(), key= lambda x: x[1])
print(max_resource)