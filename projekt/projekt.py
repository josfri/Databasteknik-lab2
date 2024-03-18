from bottle import get, post, run, response, request
from urllib.parse import unquote
import sqlite3

# Set-up
PORT = 7007
# sqlite3 lab3.sqlite < lab3.sql
db = sqlite3.connect("/Users/josefinefrid/Desktop/Databasteknik/lab2/Databasteknik-lab2/lab3/lab3.sqlite")
db.execute("PRAGMA foreign_keys = ON")

#functions start here 



#Reset database

#Add and check customers

#Add and check ingredients

#Add and check recipes/ookies

#Add and check pallets

#Blocking and unblocking

#Cookies part 2



#functions end here 

run(host='localhost', port=PORT)
