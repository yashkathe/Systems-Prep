"""
Merge both files on EMPLOYEE_ID.

Compute a new variable:

productivity_score = (PROJECTS_COMPLETED / HOURS_WORKED) * CLIENT_RATINGS * EXPERIENCE_YEARS

Sort employees by productivity_score in descending order.

Print the sorted employee records including NAME, DEPARTMENT, and productivity_score.
"""

# method 2
# iterate over both files

import csv
from collections import defaultdict

employees = defaultdict(dict)

# iterate 1

with open('./employees.csv', 'r') as f:

    reader = csv.DictReader(f)

    for line in reader:
        
        eid = int(line['EMPLOYEE_ID'])
        name = line['NAME']
        department = line['DEPARTMENT']
        experience = float(line['EXPERIENCE_YEARS'])

        employees[eid] = {
            "name": name,
            "department": department,
            "experience": experience
        }

# iterate 2 
# update dict - dont overwrite !

with open('./performance.csv', 'r') as f:

    reader = csv.DictReader(f)

    for line in reader:

        eid = int(line['EMPLOYEE_ID'])
        projects = int(line['PROJECTS_COMPLETED'])
        hours = float(line['HOURS_WORKED'])
        rating = float(line['CLIENT_RATINGS'])

        employees[eid]["projects"] = projects 
        employees[eid]["hours"] = hours
        employees[eid]["rating"] = rating


# calculate score

#----------------------------------------------------------------------------------------------# 
# productivity_score = (PROJECTS_COMPLETED / HOURS_WORKED) * CLIENT_RATINGS * EXPERIENCE_YEARS #
#----------------------------------------------------------------------------------------------#

emp_scores = defaultdict(list)

for k, v in employees.items():

    score = ( v["projects"] / v["hours"] ) * v["rating"] * v["experience"]

    emp_scores[k].append([round(score, 2), v["name"], v["department"]])

#---------------------------------------------------------------------------------------#
# Sort employees by productivity_score in descending order                              #
# Print the sorted employee records including NAME, DEPARTMENT, and productivity_score  #
#---------------------------------------------------------------------------------------#

for k, v in sorted(emp_scores.items(), key = lambda x: x[1][0], reverse= True):
    print(v)
