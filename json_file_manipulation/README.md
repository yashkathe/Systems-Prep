# JSON File Manipulation

## 1 - One File

### a. salary per department

You are provided with a JSON file named employees.json containing an array of
employee records. Each record includes the employee's ID, name, department, and
salary. Write a script to:

    Calculate the average salary per department.
    Identify the department with the highest average salary.
    Print the results in a readable format.

Sample employees.json:

[ {"id": 1, "name": "Alice", "department": "Engineering", "salary": 95000},
{"id": 2, "name": "Bob", "department": "Marketing", "salary": 70000}, {"id": 3,
"name": "Charlie", "department": "Engineering", "salary": 105000}, {"id": 4,
"name": "Diana", "department": "HR", "salary": 60000}, {"id": 5, "name": "Evan",
"department": "Marketing", "salary": 75000} ]

## 2 - Two Files

### a. Student's Average Grade

You have two JSON files: students.json and grades.json. The students.json file contains student IDs and their names, while the grades.json file contains student IDs and their grades in various subjects. Write a script to:

    Merge the data from both files based on student IDs.
    Calculate each student's average grade.
    Print each student's name along with their average grade.

Sample students.json:

[
    {"student_id": 101, "name": "John Doe"},
    {"student_id": 102, "name": "Jane Smith"},
    {"student_id": 103, "name": "Emily Johnson"}
]

Sample grades.json:

[
    {"student_id": 101, "grades": {"Math": 85, "Science": 90, "History": 78}},
    {"student_id": 102, "grades": {"Math": 92, "Science": 88, "History": 95}},
    {"student_id": 103, "grades": {"Math": 79, "Science": 85, "History": 80}}
]

## 3 - Changing Structure

### a. Transform Json for Product Data

Given a JSON file named sales.json containing sales data with the following structure:

[
    {"region": "North", "sales": [{"product": "A", "quantity": 30}, {"product": "B", "quantity": 20}]},
    {"region": "South", "sales": [{"product": "A", "quantity": 25}, {"product": "C", "quantity": 15}]},
    {"region": "East", "sales": [{"product": "B", "quantity": 10}, {"product": "C", "quantity": 5}]},
    {"region": "West", "sales": [{"product": "A", "quantity": 20}, {"product": "B", "quantity": 25}]}
]

Write a script to transform this data into a new structure where each product is a key, and its value is a dictionary showing the total quantity sold per region. The output should be a JSON object like:

{
    "A": {"North": 30, "South": 25, "West": 20},
    "B": {"North": 20, "East": 10, "West": 25},
    "C": {"South": 15, "East": 5}
}

### b. Transoform Weather Data from API

You are given a JSON file named weather.json containing weather information for multiple cities. Each city has details about temperature, humidity, wind speed, and weather conditions. However, the data needs to be restructured for better readability.
Task

    Read weather.json and extract relevant information.
    Transform the structure so that each city becomes a key, and its values include only essential details (temperature, humidity, conditions).
    Store the transformed data in a new file (formatted_weather.json).