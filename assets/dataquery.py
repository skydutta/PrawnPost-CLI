import mysql.connector as conn
from dotenv import load_dotenv
from pathlib import Path
import os, uuid, bcrypt

dotenv_path = Path("./.env")
load_dotenv(dotenv_path=dotenv_path)

# Database Connection Variables
remote_pass = os.getenv("skydutta_mysql_password")
global_host, global_port, global_user, global_password, global_database = "localhost", "3306", "root", "", "prawnpostdb"

# Data Query and Validation Functions Starts Below

def username_exists(username: str):
    """
    Input: username {str}
    Output: True {bool} -> If username Exists | False {bool} -> If username Does Not Exist
    """
    username = username.lower().replace(" ", "")
    mydb = conn.connect(
    host = global_host,
    port = global_port,
    user = global_user,
    password = global_password,
    database = global_database)
    cursor = mydb.cursor()
    Q = "SELECT username FROM users WHERE username='%s'"%(username)
    cursor.execute(Q)
    result = cursor.fetchall()
    mydb.commit()
    cursor.close()
    mydb.close()
    if len(result) == 0:
        return False
    return True

def create_new_user(new_username: str, password: str):
    """
    Input: new_username {str} | password {str}
    Output: None -> If username already exists | [Creates New User]
    """
    new_username = new_username.lower().replace(" ", "")
    password = password.replace(" ", "")
    mydb = conn.connect(
    host = global_host,
    port = global_port,
    user = global_user,
    password = global_password,
    database = global_database)
    cursor = mydb.cursor()
    new_user_id = str(uuid.uuid1())
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(14)
    hash_pw = bcrypt.hashpw(password_bytes, salt)
    hash_pw_str = hash_pw.decode("utf-8")
    if username_exists(new_username) == False:
      Q = "INSERT INTO users(user_id, username, password) VALUES('%s', '%s', '%s')"%(new_user_id, new_username, hash_pw_str)
      cursor.execute(Q)
      mydb.commit()
      cursor.close()
      mydb.close()
    else:
        return

def login_user(username: str, password: str):
    """
    Input: username {str} | password {str}
    Output: True {bool} -> username & password matches | False {bool} -> username & password does not match
    """
    username = username.lower().replace(" ", "")
    password = password.replace(" ", "")
    if username_exists(username) == True:
      mydb = conn.connect(
      host = global_host,
      port = global_port,
      user = global_user,
      password = global_password,
      database = global_database)
      cursor = mydb.cursor()
      Q = "SELECT username, password FROM users WHERE username='%s'"%(username)
      cursor.execute(Q)
      user_data = cursor.fetchone()
      username_fetched = user_data[0]
      hash_pw_str = user_data[1]
      hash_pw = hash_pw_str.decode("utf-8")
      password_in_bytes = password.encode("utf-8")
      match_pw = bcrypt.checkpw(password_in_bytes, hash_pw.encode("utf-8"))
      mydb.commit()
      cursor.close()
      mydb.close()
      if username_fetched == username and match_pw == True:
         return True
      else:
         return False
    return False

def fetch_user_id(username: str):
  """
  Input: username {str}
  Output: user_id {str} -> If username exists in 'users' Table | None -> If username does not exist in 'users' Table
  """
  username = username.lower().replace(" ", "")
  if username_exists(username) == True:
    mydb = conn.connect(
    host = global_host,
    port = global_port,
    user = global_user,
    password = global_password,
    database = global_database)
    cursor = mydb.cursor()
    Q = "SELECT user_id FROM users WHERE username='%s'"%(username)
    cursor.execute(Q)
    user_id = cursor.fetchone()
    user_id = user_id[0]
    mydb.commit()
    cursor.close()
    mydb.close()
    return user_id
  else:
     return

# Data Query and Validation Functions Ends Above

# Closing the Connections -> Function Specific
# mydb.commit()
# cursor.close()
# mydb.close()