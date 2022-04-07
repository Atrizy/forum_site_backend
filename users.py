import mariadb as db
import dbinteractions as dbi

## This function gets all the users.
def get_users():
    success = False
    ## This empty array will be filled with what is returned from the database in the select statement below
    users = []
    ## This is what is needed to actually connect to the database
    conn, cursor = dbi.connect_db()
    try:
        ## This select statement is making a request to get all of the users posts
        cursor.execute("SELECT id, username, email, pfp, profile_banner, bio, dob FROM users")
        ## This fetchall statement is getting all the users and actually putting what it grab into the empty users ("users = []") array
        users = cursor.fetchall()
        ## Once everything is done the success will return as true 
        success = True
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, users

def get_single_user(login_token):
    success = False
    user = []
    ## This is what is needed to actually connect to the database
    conn, cursor = dbi.connect_db()
    try:
        cursor.execute("SELECT username, pfp, profile_banner, dob, bio FROM users INNER JOIN user_session ON users.id = user_id WHERE login_token=?", [login_token])
        user = cursor.fetchone()
        success = True
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, user

def get_user_posts(username):
    success = False
    posts_and_poster = []
    ## This is what is needed to actually connect to the database
    conn, cursor = dbi.connect_db()
    try:
        cursor.execute("SELECT username, pfp, forum_post.header, forum_post.created_at, forum_post.id FROM users INNER JOIN forum_post ON users.id = user_id WHERE users.username=?", [username])
        posts_and_poster = cursor.fetchall()
        success = True
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, posts_and_poster