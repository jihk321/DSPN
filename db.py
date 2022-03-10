import sqlite3

con = sqlite3.connect("client.db")

cursor = con.cursor()

con.execute('CREATE TABLE client_date(id TEXT, name TEXT)')