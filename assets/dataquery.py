import mysql.connector as conn
from dotenv import load_dotenv
from pathlib import Path
import os, uuid, bcrypt

dotenv_path = Path("./.env")
load_dotenv(dotenv_path=dotenv_path)

# Database Connection Variables
remote_pass = os.getenv("skydutta_mysql_password")
global_host, global_port, global_user, global_password, global_database = "localhost", "3306", "root", "", "prawnpostdb"

# Connection Function -> Test with Sign-Up and Log-In Functions (Then All Other Functions)
def db_connect():
   try:
      mydb = conn.connect(host = global_host, port = global_port, user = global_user, password = global_password, database = global_database)
      if mydb.is_connected() == True:
         return True
   except:
      return False

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

def create_new_post(user_id: str, post_title: str, post_content: str):
   """
   Input: user_id {str} | post_title {str} | post_content {str}
   Output: [Creates New Post]
   """
   new_post_id = str(uuid.uuid1())
   Q = "INSERT INTO posts VALUES('%s', '%s', '%s', '%s')"%(new_post_id, post_title, post_content, user_id)
   mydb = conn.connect(host = global_host, port = global_port, user = global_user, password = global_password, database = global_database)
   cursor = mydb.cursor()
   cursor.execute(Q)
   mydb.commit()
   cursor.close()
   mydb.close()

def fetch_username(user_id: str):
   """
   Input: user_id {str}
   Output: username {str} -> If Valid user_id is given | None -> If Valid user_id is not given
   """
   mydb = conn.connect(host = global_host, port = global_port, user = global_user, password = global_password, database = global_database)
   cursor = mydb.cursor()
   Q = "SELECT username FROM users WHERE user_id='%s'"%(user_id)
   cursor.execute(Q)
   username_tuple = cursor.fetchone()
   username = username_tuple[0]
   mydb.commit()
   cursor.close()
   mydb.close()
   return username

def fetch_all_posts():
   """
   Input: [Nothing]
   Output: posts {list} -> Contains Tuples of Posts with username, post_id, post_title, post_content
   """
   mydb = conn.connect(host = global_host, port = global_port, user = global_user, password = global_password, database = global_database)
   cursor = mydb.cursor()
   Q = "SELECT user_id, post_id, post_title, post_content FROM posts"
   cursor.execute(Q)
   posts_fetched = cursor.fetchall()
   posts = list()
   for post in posts_fetched:
      username = fetch_username(post[0])
      posts.append((username, post[1], post[2], post[3]))
   mydb.commit()
   cursor.close()
   mydb.close()
   return posts

def valid_post_id(post_id: str):
   """
   Input: post_id {str}
   Output: True {bool} -> If Post-ID is Valid | False {bool} -> If Post-ID is InValid
   """
   post_id = post_id.replace(" ", "")
   mydb = conn.connect(host = global_host, port = global_port, user = global_user, password = global_password, database = global_database)
   cursor = mydb.cursor()
   Q = "SELECT post_id FROM posts WHERE post_id='%s'"%(post_id)
   cursor.execute(Q)
   post_id_data = cursor.fetchone()
   mydb.commit()
   cursor.close()
   mydb.close()
   try:
      if post_id_data[0] == post_id:
        return True
   except:
      return False
   
def create_comment(user_id: str, post_id: str, comment: str):
   """
   Input: user_id {str} | post_id {str} | comment {str}
   Output: [Creates the Comment in the comments table]
   """
   comment_id = str(uuid.uuid1())
   mydb = conn.connect(host = global_host, port = global_port, user = global_user, password = global_password, database = global_database)
   cursor = mydb.cursor()
   Q = "INSERT INTO comments VALUES('%s', '%s', '%s', '%s')"%(comment_id, comment, user_id, post_id)
   cursor.execute(Q)
   mydb.commit()
   cursor.close()
   mydb.close()

def fetch_post(post_id: str):
   """
   Input: post_id {str}
   Output: post {tuple} -> Fetched from MySQL DB using post_id
   """
   post_id = post_id.replace(" ", "")
   mydb = conn.connect(host = global_host, port = global_port, user = global_user, password = global_password, database = global_database)
   cursor = mydb.cursor()
   Q = "SELECT * FROM posts WHERE post_id='%s'"%(post_id)
   cursor.execute(Q)
   post = cursor.fetchone()
   mydb.commit()
   cursor.close()
   mydb.close()
   return post

def fetch_post_comments(post_id: str):
   """
   Input: post_id {str}
   Output: post_comments {list} -> Fetched from MySQL DB using post_id
   """
   post_id = post_id.replace(" ", "")
   mydb = conn.connect(host = global_host, port = global_port, user = global_user, password = global_password, database = global_database)
   cursor = mydb.cursor()
   Q = "SELECT * FROM comments WHERE post_id='%s'"%(post_id)
   cursor.execute(Q)
   post_comments = cursor.fetchall()
   mydb.commit()
   cursor.close()
   mydb.close()
   return post_comments

# Data Query and Validation Functions Ends Above

