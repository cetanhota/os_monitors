#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""""
3/14/2022
@author: wayne
"""""

from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host=input("localhost"),
        user=input("Enter username: "),
        auth_plugin='mysql_native_password',
        password=getpass("Enter password: "),
    ) as connection:
        print(connection)
except Error as e:
    print(e)
