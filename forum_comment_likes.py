import mariadb as db
import dbinteractions as dbi

## This is adding a like to a comment
def comment_like(login_token, comment_id):
    success = False
    id = None
    ## Connecting to the db
    conn, cursor = dbi.connect_db()
    try:
        ## Getting the login token to figure out which user is trying to like a comment
        cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
        ## This fetchone statement is getting the everything about the user
        user = cursor.fetchone()
        ## This is inserting the like onto the comment
        cursor.execute("INSERT INTO comment_like(user_id, comment_id) VALUES(?,?)", [user[0], comment_id])
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
    return success, id

def get_comment_like(comment_id):
    success = False
    ## This empty array will be filled with what is returned from the database in the select statement below
    likes = []
    ## Connecting to the db
    conn, cursor = dbi.connect_db()
    try:
        ## This select statement is grabbing all the comment likes and joining the the users table so that the backend can figure out what user[s] are liking the comment
        cursor.execute("SELECT users.username, comment_like.comment_id, comment_like.user_id FROM users INNER JOIN comment_like ON comment_like.user_id = users.id WHERE comment_like.comment_id=?", [comment_id])
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

def delete_comment_like(login_token, id, comment_id):
    success = False
    ## Connecting to the db
    conn, cursor = dbi.connect_db()
    try:
        ## Getting the login token to figure out which user is trying to delete like a forum post
        cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
        ## This fetchone statement is getting the everything about the user
        user = cursor.fetchone()
        ## This execute statement is removing the like from the comment depending on the users id
        cursor.execute("DELETE FROM comment_like WHERE id=? AND user_id=? AND comment_id=?", [id, user[0], comment_id] )
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