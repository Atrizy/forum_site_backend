import mariadb as db
import dbcreds as c

## This is connecting to the db
def connect_db():
    conn = None
    cursor = None
    try:
        ## This is getting all of the credentials from the dbcreds.py
        conn = db.connect(username=c.user, password=c.password, host=c.host, port=c.port, database=c.database)
        ## This is connecting the cursor
        cursor = conn.cursor()
    except db.OperationalError:
        print("Something is wrong with the DB, please try again in 5 minutes")
    except:
        print("Sorry, please try again")

    return conn, cursor

## Disconnecting the database
def disconnect_db(conn, cursor):
    try:
        cursor.close()
    except:
        print("Issue closing cursor. Someone should look into this.")
    try:
        conn.close()
    except:
        print("Issue closing connection. Someone should look into this.")