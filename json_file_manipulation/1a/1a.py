"""
Calculate the average salary per department.
Identify the department with the highest average salary.
Print the results in a readable format.
"""

import json
from collections import defaultdict

dept_salary = defaultdict(list)

with open('./employees.json', 'r') as f:

    reader = json.load(f)

    for line in reader:
        
        department = line["department"] 
        salary = int(line["salary"])

        dept_salary[department].append(salary)

avg_salary = { k: sum(v)//len(v) for k, v in dept_salary.items() }

print(avg_salary)