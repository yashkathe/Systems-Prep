# CSV File Manipulation Questions

## 1. Single CSV File Questions

### a. Log File Analysis

Scenario: You are provided with a CSV file named server_logs.csv containing
server access logs with the following columns:

TIMESTAMP, USER_ID, ACTION, RESOURCE, RESPONSE_TIME_MS 2025-02-05 09:00:00,
12345, GET, /index.html, 150 2025-02-05 09:01:00, 12346, POST, /api/data, 200
...

Task: Write a program to read server_logs.csv and perform the following:

    Calculate the average response time for each unique ACTION.
    Identify the USER_ID with the highest number of POST actions.
    Determine the most frequently accessed RESOURCE.

### b. System Metrics Aggregation

Scenario: A CSV file named system_metrics.csv contains system performance
metrics with the following structure:

TIMESTAMP, CPU_USAGE, MEMORY_USAGE, DISK_IO, NETWORK_IO 2025-02-05 09:00:00, 45,
70, 120, 300 2025-02-05 09:01:00, 50, 65, 110, 320 ...

Task: Develop a script to:

    Compute the average CPU_USAGE, MEMORY_USAGE, DISK_IO, and NETWORK_IO over the entire dataset.
    Identify the time period (start and end TIMESTAMP) during which CPU_USAGE exceeded 80%.
    Find the peak MEMORY_USAGE and the corresponding TIMESTAMP.

### c. Log Parsing and Analysis

Scenario: You have a log file in CSV format named application_logs.csv with the
following columns:

TIMESTAMP, LOG_LEVEL, MESSAGE 2025-02-05 09:00:00, INFO, Application started
2025-02-05 09:01:00, ERROR, Null pointer exception ...

Task: Develop a script to:

    Count the number of occurrences for each LOG_LEVEL.
    Extract and display all unique error messages along with their first occurrence TIMESTAMP.
    Identify the time periods with the highest frequency of ERROR logs.

## 2. Two CSV File Questions:

### a. User Activity Correlation

Scenario: You have two CSV files: user_profiles.csv and user_activity.csv.

user_profiles.csv:

USER_ID, NAME, AGE, COUNTRY 12345, Alice, 30, USA 12346, Bob, 25, UK ...

user_activity.csv:

USER_ID, LOGIN_TIMESTAMP, ACTIVITY_TYPE, DURATION_MIN 12345, 2025-02-05
09:00:00, Reading, 30 12346, 2025-02-05 09:05:00, Writing, 45 ...

Task: Create a program to:

    Merge the two datasets based on USER_ID.
    Calculate the total DURATION_MIN spent by each user on different ACTIVITY_TYPE.
    Identify the top 3 countries with the highest average activity duration.

### b. Product Sales Analysis

Scenario: Two CSV files are provided: products.csv and sales.csv.

products.csv:

PRODUCT_ID, PRODUCT_NAME, CATEGORY, PRICE 101, Widget A, Gadgets, 19.99 102,
Widget B, Gizmos, 29.99 ...

sales.csv:

SALE_ID, PRODUCT_ID, SALE_DATE, QUANTITY 1001, 101, 2025-02-05, 3 1002, 102,
2025-02-06, 2 ...

Task: Write a script to:

    Join the two files on PRODUCT_ID.
    Calculate the total revenue generated for each CATEGORY.
    Determine the best-selling PRODUCT_NAME based on QUANTITY sold.

### c. Bipedal dinosaurs from fastest to slowest

Scenario: You are supplied with two CSV files in CSV format. The first file
contains statistics about various dinosaurs. The second file contains additional
data. Given the following formula:

```txt
speed = ((STRIDE_LENGTH / LEG_LENGTH) - 1) _ SQRT(LEG_LENGTH _ g)
Where g = 9.8
m/s^2 (gravitational constant)
```

Task: Write a program to read in the data files from disk, then print the names
of only the bipedal dinosaurs from fastest to slowest.

### d. Configuration File Comparison [Incomplete]

Scenario: Two CSV files, config_old.csv and config_new.csv, represent system
configurations at different times. Both files have the structure:

PARAMETER, VALUE max_connections, 100 timeout, 30 ...

Task: Write a program to:

    Compare the two configuration files and list parameters that have changed values.
    Identify parameters present in config_new.csv but missing in config_old.csv and vice versa.
    Generate a summary report of the differences.
