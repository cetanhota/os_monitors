#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""""
3/14/2022
@author: wayne
"""""
import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.1.61",
  auth_plugin='mysql_native_password',
  user="pi",
  password="hawk69"
)

mycursor = mydb.cursor()
version = mydb.get_server_info()
stats = mydb.cmd_statistics()

mycursor.execute("show processlist")

results = mycursor.fetchall()

for x in results:
    print(x)

#print (version)
#print (stats)
  #cnx.commit()

mydb.close()
