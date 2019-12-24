import mysql.connector
 
mydb = mysql.connector.connect(
  host="192.168.5.31",
  user="root",
  passwd="123456"
)
 
mycursor = mydb.cursor()
 
mycursor.execute("CREATE DATABASE runoob_db")