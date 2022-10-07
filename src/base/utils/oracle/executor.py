# https://www.geeksforgeeks.org/oracle-database-connection-in-python/
import cx_Oracle


def get_data_from_db(database_connection: str, sqlquery: str):
    """

    :rtype: object
    """
    try:
        con = cx_Oracle.connect(database_connection)
    except cx_Oracle.DatabaseError as er:
        print('There is an error in the Oracle database:', er)
    else:
        try:

            cur = con.cursor()

            # # fetchall() is used to fetch all records from result set
            # cur.execute(sqlquery)
            # rows = cur.fetchall()

            # fetchmany(int) is used to fetch limited number of records from result set based on integer argument passed in it
            cur.execute(sqlquery)
            rows = cur.fetchmany(3)

            # fetchone() is used fetch one record from top of the result set
            # cur.execute(sqlquery)
            # rows = cur.fetchone()

            # print(rows)
            return rows
        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:', er)
        except Exception as er:
            print('Error:' + str(er))
        finally:
            if cur:
                cur.close()
    finally:
        if con:
            con.close()
