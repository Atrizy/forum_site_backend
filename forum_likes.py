import mariadb as db
import dbinteractions as dbi

## This function is adding a like to a forum
def rate_forum(login_token, forum_id):
    success = False
    id = None
    ## Connecting to the db
    conn, cursor = dbi.connect_db()
    try:
        ## Getting the login token to figure out which user is trying to make like a forum post
        cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
        ## This fetchone statement is getting the everything about the user
        user = cursor.fetchone()
        ## This is inserting the like onto the forum post
        cursor.execute("INSERT INTO forum_rating(user_id, forum_id) VALUES(?,?)", [user[0], forum_id])
        ## Commiting the changes
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
            id = cursor.lastrowid
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, id, forum_id

def get_forum_rating(forum_id):
    success = False
    ## This empty array will be filled with what is returned from the database in the select statement below
    likes = []
    ## Connecting to the db
    conn, cursor = dbi.connect_db()
    try:
        ## This select statement is grabbing all the forum likes and joining the the users table so that the backend can figure out what user[s] are liking the forum
        cursor.execute("SELECT users.username, forum_rating.forum_id, forum_rating.user_id FROM users INNER JOIN forum_rating ON forum_rating.user_id = users.id WHERE forum_rating.forum_id=?", [forum_id])
        ## This is fetching all the comments and inputting into the empty likes ("likes = []") array
        likes = cursor.fetchall()
        success = True
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, likes

def delete_forum_rating(login_token, id, forum_id):
    success = False
    conn, cursor = dbi.connect_db()
    try:
        ## Getting the login token to figure out which user is trying to delete like a forum post
        cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
        ## This fetchone statement is getting the everything about the user
        user = cursor.fetchone()
        ## This execute statement is removing the like from the forum posting depending on the users id
        cursor.execute("DELETE FROM forum_rating WHERE id=? AND user_id=? AND forum_id=?", [id, user[0], forum_id])
        ## Commiting the changes
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
            id = cursor.lastrowid
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success