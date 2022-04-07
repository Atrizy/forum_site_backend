import mariadb as db
import dbinteractions as dbi
import hashlib
import secrets

## Creating password encryption
def create_salt():
    return secrets.token_urlsafe(10)
## This is creating a login token that will contain everything the API would need to access the users information
def create_login_token():
    return secrets.token_urlsafe(70)
## This signup function is taking user input from the frontend and sending it to the backend to create a user
def signup(email, username, password, bio, dob, pfp, profile_banner):
    success = False
    id = None
    conn, cursor = dbi.connect_db()
    ## This is calling the salt that will be used as a password alternative
    salt = create_salt()
    ## This is creating the login token that will be used for everything (Literally)
    login_token = create_login_token()
    ## This is adding the salt to the password   
    password = salt + password
    ## This is hashing the password for better encryption
    password = hashlib.sha512(password.encode()).hexdigest()
    try:
        ## This insert statement is basically creating a user by actually inserting all the information provided by the users on the frontend
        cursor.execute("INSERT INTO users(email, username, password, bio, dob, pfp, profile_banner, salt) VALUES(?,?,?,?,?,?,?,?)", [email, username, password, bio, dob, pfp, profile_banner, salt])
        ## This is commiting the the insert statement into the db
        conn.commit()
        if(cursor.rowcount == 1):
            id = cursor.lastrowid
            ## This is what will happen when your signup is actually successful your login token and user id will be inserted into the user_session table 
            cursor.execute("INSERT INTO user_session(user_id, login_token) VALUES(?,?)", [id, login_token])
            ## This is commiting the the insert statement into the db
            conn.commit()
            success = True
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, id, login_token
## This function will update the users info depending on what the input within the frontend 
def patch_user_info(login_token, email, username, bio, dob, pfp, profile_banner):
    success = False
    ## This is what is needed to actually connect to the database
    conn, cursor = dbi.connect_db()
    ## This is needed to make sure you are actually the owner of the account
    cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
    ## Fetching the users information
    user = cursor.fetchone()
    try:
        ## These 6 cursor.execute statements are updating the information on the backend through the db and taking in input from the frontend through the user to update their profile
        cursor.execute("UPDATE users SET email=? WHERE id=?", [email, user[0]])
        cursor.execute("UPDATE users SET username=? WHERE id=?", [username, user[0]])
        cursor.execute("UPDATE users SET bio=? WHERE id=?", [bio, user[0]])
        cursor.execute("UPDATE users SET dob=? WHERE id=?", [dob, user[0]])
        ## These if statement are needed because whenever a user updates thier profile their profile picture and thier profile banner will be set to the default and the user would have to change it again
        if(pfp != None ):
            cursor.execute("UPDATE users SET pfp=? WHERE id=?", [pfp, user[0]])
        if(profile_banner != None):
            cursor.execute("UPDATE users SET profile_banner=? WHERE id=?", [profile_banner, user[0]])
        ## This is commiting the changes
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

