import sqlite3
import re
import os
from datetime import datetime

import config
from sql_queries import (
    CREATE_NEW_TABLE,
    INSERT_ENTRY_TO_TABLE,
    COUNT_DISTINCT_COMMANDS,
    MOST_FREQUENT_COMMAND,
    USER_WITH_MOST_EXECUTES,
    LEAST_COMMON_COMMAND,
    FOLDER_PATH_WITH_MOST_ACTIVITY,

)

def create_connection(db_file):
    """ Create a database connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

# Function to create tables
def create_table(conn):
    """ Create table if it doesn't exist """
    try:
        cursor = conn.cursor()
        cursor.execute(CREATE_NEW_TABLE)
        conn.commit()
    except Exception as e:
        print(e)

# Function to insert a log entry into the table
def insert_log_entry(conn, log_entry):
    """ Insert a log entry into the audit_logs table """
    cur = conn.cursor()
    cur.execute(INSERT_ENTRY_TO_TABLE, log_entry)
    conn.commit()
    return cur.lastrowid

# Function to parse log file
def parse_log_file(file_path):
    """Parse the log file and extract relevant information."""
    log_entries = []
    pattern = re.compile(
        r"type=(?P<type>\w+) msg=audit\((?P<msg>\d+\.\d+):\d+\): "
        r"(?:.*?syscall=(?P<syscall>\d+))?"
        r"(?:.*?success=(?P<success>\w+))?"
        r"(?:.*?exit=(?P<exit>\d+))?"
        r"(?:.*?items=(?P<items>\d+))?"
        r"(?:.*?ppid=(?P<ppid>\d+))?"
        r"(?:.*?pid=(?P<pid>\d+))?"
        r"(?:.*?comm=\"(?P<comm>[^\"]+)\")?"
        r"(?:.*?exe=\"(?P<exe>[^\"]+)\")?"
        r"(?:.*?key=\"(?P<key>[^\"]+)?\")?"
    )
    # Open and read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                matched_dict = match.groupdict()
                # Assign None if key field is empty
                if 'key' not in matched_dict or matched_dict['key'] is None:
                    matched_dict['key'] = None
                if matched_dict['msg']:
                    timestamp = float(matched_dict['msg'])
                    matched_dict['msg'] = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
                log_entries.append(matched_dict)    
    return log_entries

# Function to query the database and display results
def query_db(conn, query):
    """ Query the database and return the results """
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)

def get_most_frequent_command(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute(MOST_FREQUENT_COMMAND)
    result = cur.fetchone()
    if result:
        return result
    else:
        return None, 0
    
def get_count_distinct_commands(conn: sqlite3.Connection):
    pass

def execute_query(conn: sqlite3.Connection, query: str, params=()):
    """
    Execute a SQL query and return the result.

    :param conn: The SQLite database connection object.
    :param query: SQL query string.
    :param params: Parameters for the SQL query.
    :return: The first row of the result set or None if no result.
    """
    cur = conn.cursor()
    cur.execute(query, params)
    return cur.fetchone()

## use of main query function
def get_count_distinct_commands(conn: sqlite3.Connection):
    query = "SELECT COUNT(DISTINCT comm) FROM audit_logs;"
    return execute_query(conn, query)



# Main queries function
def execute_all_queries(conn: sqlite3.Connection):
    try:
        #printing all the outputs, should log this too
        print("Most frequent command:", get_most_frequent_command(conn))
        print("Number of distinct commands:", get_count_distinct_commands(conn))

        #example of use
        most_frequent_command = get_most_frequent_command(conn)
        if most_frequent_command:
            print(f"Most frequent command: {most_frequent_command[0]} with {most_frequent_command[1]} occurrences.")
    
    
    except Exception as e:
        print(f"An error occurred: {e}")


# Main function
def main():
    
    try:
        conn = create_connection(config.DATABASE_NAME)
        create_table(conn)

        # Parse log file and insert entries
    
        log_entries = parse_log_file(config.AUDIT_LOG_FILE)
        for entry in log_entries:
            insert_log_entry(conn, entry)
            #print(entry)
        # print(log_entries)
        execute_all_queries(conn)   
        # Execute specific queries
        query_db(conn, "SELECT COUNT(DISTINCT comm) FROM audit_logs_table;")
    except Exception as e:
        print(f"An error occurred: {e}")
    
        # Clean-up code if needed

    
    finally:
        if conn:
                conn.close()

if __name__ == '__main__':
    main()
