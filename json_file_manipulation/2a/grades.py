"""
Merge the data from both files based on student IDs.
Calculate each student's average grade.
Print each student's name along with their average grade.
"""

import json
from collections import defaultdict

grades = defaultdict(dict)

with open('students.json', 'r') as f:

    reader = json.load(f)

    for line in reader:

        sid = line["student_id"]
        name = line["name"]

        grades[sid]["name"] = name

with open('grades.json', 'r') as f:

    reader = json.load(f)

    for line in reader:

        sid = line["student_id"]
        all_grades = line["grades"]

        grades[sid]["all_grades"] = list(all_grades.values())



avg_grades = defaultdict(int)

for k, v in grades.items():

    all_grades = v['all_grades']

    avg_grades[k, v['name']] =  sum(all_grades) // len(all_grades)

for k, v in sorted(avg_grades.items(), reverse=True, key = lambda x: x[1]):

    print(k, v)
    print()