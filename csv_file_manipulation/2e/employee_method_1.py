"""
Merge both files on EMPLOYEE_ID.

Compute a new variable:

productivity_score = (PROJECTS_COMPLETED / HOURS_WORKED) * CLIENT_RATINGS * EXPERIENCE_YEARS

Sort employees by productivity_score in descending order.

Print the sorted employee records including NAME, DEPARTMENT, and productivity_score.
"""

# method 1
# create new CSV file

import pandas as pd
import csv
from collections import defaultdict

#---------------------------------#
# Merge both files on EMPLOYEE_ID #
#---------------------------------#


df1 = pd.read_csv('./employees.csv')
df2 = pd.read_csv('./performance.csv')

combined = pd.merge(df1, df2, on='EMPLOYEE_ID')

combined.to_csv('combined_csv.csv')


#----------------------------------------------------------------------------------------------# 
# productivity_score = (PROJECTS_COMPLETED / HOURS_WORKED) * CLIENT_RATINGS * EXPERIENCE_YEARS #
#----------------------------------------------------------------------------------------------#

employee_score = defaultdict(int)

with open('./combined_csv.csv', 'r') as f:

    reader = csv.DictReader(f)

    for line in reader:

        projected_completed = float(line['PROJECTS_COMPLETED'])
        hours = float(line['HOURS_WORKED'])
        rating = float(line['CLIENT_RATINGS'])
        experience = float(line['EXPERIENCE_YEARS'])

        emp = line['EMPLOYEE_ID']

        rating =  (projected_completed / hours) * rating * experience

        employee_score[emp] = round(rating, 2)


#---------------------------------------------------------------------------------------#
# Sort employees by productivity_score in descending order                              #
# Print the sorted employee records including NAME, DEPARTMENT, and productivity_score  #
#---------------------------------------------------------------------------------------#

for k, v in sorted(employee_score.items(), reverse=True, key = lambda x: x[1]):
    print(k, v)

"""
104 0.48
107 0.37
103 0.31
106 0.25
101 0.19
105 0.12
102 0.09
108 0.06
"""