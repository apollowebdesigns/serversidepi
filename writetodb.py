import MySQLdb as my
 
db = my.connect(host="127.0.0.1",
user="root",
passwd="",
db="world"
)
 
cursor = db.cursor()
 
sql = "insert into city VALUES(null, 'Mars City', 'MAC', 'MARC', 1233)"
 
number_of_rows = cursor.execute(sql)
db.commit()   # you need to call commit() method to save 
              # your changes to the database
 
 
db.close()