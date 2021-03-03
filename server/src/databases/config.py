import mysql.connector

try:
  
  myDB = mysql.connector.connect(
    host="db4free.net",
    user="visie_user",
    password="visie_pass",
    database= "visie_db"
  )

  myDriver = myDB.cursor()

  print("[database] Connected")

except Exception as e:
  print("ERROR on database:", e)


