# audit-logs
This project which meant to run in an ubuntu env,
Fectches logs based on unique rules I edited, and then uploads it to a local sever(sqlite).
Afterwards, it uses some queries to fecth specific data based on the table.

# Dependencies
  1. Ubuntu 22.04 LTS
  2. auditd package ```sudo apt-get install auditd```
  3. sqlite3 ```pip install sqlite```

# Usage
Running ```python3 main.py```
