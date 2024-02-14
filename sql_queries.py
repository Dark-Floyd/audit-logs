## Create a new table if not existed
CREATE_NEW_TABLE = """
    CREATE TABLE IF NOT EXISTS audit_logs (
                        type TEXT,
                        msg TEXT,
                        syscall INTEGER,
                        success TEXT,
                        exit INTEGER,
                        items INTEGER,
                        ppid INTEGER,
                        pid INTEGER,
                        comm TEXT,
                        exe TEXT,
                        key TEXT
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
"""
## Insert an entry to the table
INSERT_ENTRY_TO_TABLE = """INSERT INTO audit_logs(type, msg, syscall, success, exit, items, ppid, pid, comm, exe, key)
                        VALUES(:type, :msg, :syscall, :success, :exit, :items, :ppid, :pid, :comm, :exe, :key)                
"""
## The number of different "auditd" rules/commands in the database.
COUNT_DISTINCT_COMMANDS = "SELECT COUNT(DISTINCT comm) FROM audit_logs;"

## The command that appears most frequently.
MOST_FREQUENT_COMMAND = """
    SELECT comm, COUNT(*) as frequency 
    FROM audit_logs 
    GROUP BY comm 
    ORDER BY frequency DESC 
    LIMIT 1;
"""

## The user who executes the most commands.
USER_WITH_MOST_EXECUTES = """
    SELECT uid, COUNT(*) as command_count 
    FROM audit_logs 
    GROUP BY uid 
    ORDER BY command_count DESC 
    LIMIT 1;
"""

## The least common command.
LEAST_COMMON_COMMAND = """
    SELECT comm, COUNT(*) as frequency 
    FROM audit_logs 
    GROUP BY comm 
    ORDER BY frequency ASC 
    LIMIT 1;
"""

## The folder path that has the most activity
FOLDER_PATH_WITH_MOST_ACTIVITY = """
    SELECT cwd, COUNT(*) as activity 
    FROM audit_logs 
    GROUP BY cwd 
    ORDER BY activity DESC 
    LIMIT 1;
"""
