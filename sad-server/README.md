# Sad Servers Solutions and Notes

Table of Content

- [Sad Servers Solutions and Notes](#sad-servers-solutions-and-notes)
  - [Easy Level](#easy-level)
    - ["Saint John": what is writing to this log file?](#saint-john-what-is-writing-to-this-log-file)
    - [Answer 1](#answer-1)
    - [2. Counting IPs](#2-counting-ips)
    - [Answer 2](#answer-2)

## Easy Level

### "Saint John": what is writing to this log file?

**Type: Fix**

A developer created a testing program that is continuously writing to a log file
/var/log/bad.log and filling up disk. You can check for example with tail -f
/var/log/bad.log. This program is no longer needed. Find it and terminate it.

### Answer 1

- command 1

```bash
lsof | grep 'name of file'
```

to check the list of open file and get the pid of this process with grep

- command 2

pid - (pid we dot from lsof)

```bash
ps -ef | grep 'pid / name of the file'
```

or

```bash
ps auxf | grep 'pid / name of the file' # Ignore system processes [in brackets]
```

### 2. Counting IPs

**Tags: bash**

There's a web server access log file at /home/admin/access.log. The file
consists of one line per HTTP request, with the requester's IP address at the
beginning of each line.

Find what's the IP address that has the most requests in this file (there's no
tie; the IP is unique). Write the solution into a file
/home/admin/highestip.txt. For example, if your solution is "1.2.3.4", you can
do echo "1.2.3.4" > /home/admin/highestip.txt

### Answer 2

we can use the following command

```bash
cat /home/admin/access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -n 1
```

_always use sort before uniq -c because it counts consecutive similar elements_

sort  
-n numerically -r in reverse

_python script for the same function - [file](./E-2/e-2.py)_
