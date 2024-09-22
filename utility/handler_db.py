import sqlite3
from datetime import datetime as dt
from datetime import timedelta as td

global_con = None
global_cur = None
global_dbName = None


def checkConnection(dbName: str, logger):
    try:
        global global_con, global_cur, global_dbName
        global_dbName = dbName
        global_con = sqlite3.connect(dbName, check_same_thread=False)
        global_cur = global_con.cursor()
        logger.info(f"{dbName}: Up and running")
    except Exception:
        logger.info(f"Error with {dbName}: {Exception}")


def createTable(tableName, query, logger):
    global_cur.execute(query)

    res = global_cur.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';"
    )
    if res.fetchone():
        logger.info(f"Table {tableName} created successfully for {global_dbName}")
    else:
        logger.warning(f"Error creating table {tableName} with types: {query}")


def get_table_names(logger):
    command = """
    SELECT 
        name 
    FROM 
        sqlite_master 
    WHERE 
        type ='table' 
    AND 
        name NOT LIKE 'sqlite_%';"""
    res = global_cur.execute(command)
    res_fetched = res.fetchall()
    if len(res_fetched) > 0:
        return res_fetched
    else:
        return None


def getRow(tableName, column, condition):
    res = global_cur.execute(
        f"SELECT * FROM {tableName} WHERE {column} IS '{condition}'"
    )
    row = res.fetchone()
    if res is not None:
        return row
    else:
        return None


def addRow(tableName, data, logger):
    query = f"""
    INSERT INTO {tableName} 
    ({', '.join(data.keys())}) 
    VALUES 
    ({', '.join(['?' for _ in data])});
    """

    params = tuple(value for value in data.values())
    global_cur.execute(query, params)
    global_con.commit()

    res = global_cur.execute(f"SELECT * FROM {tableName}")
    row = res.fetchone()
    if row:
        logger.info(f"Activity '{row[0]}' successfully added to {tableName}")
    else:
        logger.warning(f'Error adding {data["fileName"]}')
        return None


def check_activitiy_exists(tableName, fileName, logger):
    query = f"""
    SELECT * FROM {tableName} WHERE fileName == '{fileName}';
    """
    res = global_cur.execute(query)
    logger.info(res)
    if res.fetchone():
        return True
    else:
        return False


def getSum(tableName, column, logger):
    query = f"SELECT SUM({column}) FROM {tableName};"
    result = global_cur.execute(query)
    logger.info(result)
    return result.fetchone()[0]


def countRows(tableName, logger):
    query = f"""
    SELECT COUNT(*) as number_activities
    FROM '{tableName}';
    """
    result = global_cur.execute(query)
    return result.fetchone()[0]


def getAvg(tableName, column, logger):
    query = f"SELECT AVG({column}) FROM {tableName} WHERE {column} != 0;"
    result = global_cur.execute(query)
    return result.fetchone()[0]


def dropTable(tableName, logger):
    command = f"DROP TABLE '{tableName}';"
    res = global_cur.execute(command)
    return res.fetchone()


def getTotalTime(tableName, logger):
    query = f"SELECT SUM(duration) FROM {tableName};"
    result = global_cur.execute(query)
    mm, ss = divmod(result.fetchone()[0], 60)
    hh, mm = divmod(mm, 60)
    return f'{hh} "Hours", {mm}, "Minutes", {ss}, "Seconds"'
