import mariadb as db
import dbinteractions as dbi
import secrets
import hashlib

## This function is creaeting a login that will house all the user information.
def create_login_token():
    return secrets.token_urlsafe(70)

## This is the code that will be called when logging in a user
def login_user(email, password):
    success = False
    ## This is what is needed to actually connect to the database
    conn, cursor = dbi.connect_db()
    ## This is getting the user inputed email from the users table and comparing it to the salt that is in the db if they are both a match you will move onto the next step
    cursor.execute("SELECT salt FROM users WHERE email=?", [email])
    ## You only need to fetch one because with user input on the email the api only needs to compare one email to the salt
    salt = cursor.fetchone()
    ## This is the code thatis executing the login token creation
    login_token = create_login_token()
    ## This is comparing the salt to the password
    password = salt[0] + password
    ## This is comparing the password that has been input to the hashed version of the password
    password = hashlib.sha512(password.encode()).hexdigest()
    ## This is getting all of the users information
    cursor.execute("SELECT id, email, username, bio, dob, pfp, profile_banner FROM users WHERE email=? AND password=?", [email, password])
    ## This is the actually compiling all the user info into a single object
    user = cursor.fetchone()
    try:
        if(cursor.rownumber == 1):
            ## This is what will happen when your login is actually successful your login token and user id will be inserted into the user_session table 
            cursor.execute("INSERT INTO user_session(user_id, login_token) VALUES(?,?)", [user[0], login_token])
            conn.commit()
            success = True
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, login_token

## This is for deleting a user, you need a valid login token to prove you are the owner of the account.
def delete_user(login_token):
    success = False
    conn, cursor = dbi.connect_db()
    try:
        ## This will check your login_token and see your user credentials
        cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
        ## This acutally fetches everything from your login token
        user = cursor.fetchone()
        ## This will delete your user from the db if the user_id matches up
        cursor.execute("DELETE FROM users WHERE id=?", [user[0]] )
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