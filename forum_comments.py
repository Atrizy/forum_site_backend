import mariadb as db
import dbinteractions as dbi

## This is getting all the comments that are connected to a forum posting
def get_all_comments():
    success = False
    ## This empty array will be filled with what is returned from the database in the select statement below
    comments = []
    ## Connecting to the db
    conn, cursor = dbi.connect_db()
    try:
        ## This select statement is grabbing all the forum comments and joining the the users table to get the commenters user id
        cursor.execute(
            "SELECT users.id, users.username, comment.content, comment.created_at, comment.id FROM comment INNER JOIN users ON users.id = comment.user_id")
        ## This is fetching all the comments and inputting into the empty comments ("comments = []") array
        comments = cursor.fetchall()
        success = True
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, comments

## This function is creating a comment, whatever the user inputs in the frontend it will be created as a comment
def insert_comment(login_token, content):
    success = False
    id = None
    ## Connecting to the db
    conn, cursor = dbi.connect_db()
    try:
        ## Getting the login token to figure out which user is trying to make a comment
        cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
        ## This fetchone statement is getting the everything about the user
        user = cursor.fetchone()
        ## Depending on what the user is inputting this INSERT statement will insert the users id and the content that is provided on the front end 
        cursor.execute("INSERT INTO comment(user_id, content) VALUES(?,?)", [user[0], content])
        ## Committing the changes in the db
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

## This is for editing comments dpending on what is input on the frontend 
def patch_comment_info(login_token, content, id):
    success = False
    ## Connecting to the db
    conn, cursor = dbi.connect_db()
    ## Getting the login token to figure out which user is trying to edit a comment
    cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
    ## Fetching the users information
    user = cursor.fetchone()
    try:
        ## This cursor.execute statement is updating the information on the backend through the db and taking in input from the frontend through the user to update their comment
        cursor.execute("UPDATE comment SET content=? WHERE id=? AND user_id=?", [content, id, user[0]])
        ## Committing all the changes
        conn.commit()
        success = True
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success 

## This function deletes a comment after confirming that the user trying to delete the comment is the owner of the comment
def delete_comment(login_token, id):
    success = False
    ## Connecting to the db
    conn, cursor = dbi.connect_db()
    try:
        ## This is grabbing your login token to make sure that you the owner of the forum post before the function can actually delete the posting
        cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
        ## Fetching the users information
        user = cursor.fetchone()
        ## This is deleting the comment from the db if the user_id matches up
        cursor.execute("DELETE FROM comment WHERE id=? AND user_id=?", [id, user[0]])
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