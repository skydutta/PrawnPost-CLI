import mysql.connector as conn
from dotenv import load_dotenv
from pathlib import Path
import os, uuid

dotenv_path = Path("./.env")
load_dotenv(dotenv_path=dotenv_path)

mydb = conn.connect(
  host = "db4free.net",
  port = "3306",
  user = "skydutta",
  password = os.getenv("skydutta_mysql_password"),
  database = "prawnpostdb"
)

def star():
    print("Star on Fire")

for i in range(100000):
  unique_id_1 = uuid.uuid1()
  unique_id_2 = uuid.uuid1()
  if str(unique_id_1) == str(unique_id_2):
    print(str(unique_id_1))
    print(str(unique_id_2))
    break
print("Unique Success")
print(len(str(unique_id_1)))
print(len(str(unique_id_2)))
