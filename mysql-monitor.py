#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""""
3/14/2022
@author: wayne
"""""
import mysql.connector
from tabulate import tabulate
import socket
import time
import os
import psutil
import sys

class color:
        BOLD = '\033[1m'
        END = '\033[0m'
        RED = '\033[91m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'

menu_options = {
    1: 'Show Processlist',
    2: 'Total Connections',
    3: 'Innodb Buffer Pool Information',
    4: 'System Load Average',
    5: 'Network Latency Check',
    6: 'System Overview',
    7: 'CPU Percent',
    0: 'Exit'
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )
HOST = socket.gethostname()

def clear():
    os.system('clear')

mydb = mysql.connector.connect(
host="192.168.1.61",
auth_plugin='mysql_native_password',
user="pi",
password="hawk69")
global mycursor
mycursor = mydb.cursor()

def fn_processlist():
    query = "show processlist"
    mycursor.execute(query)
    results = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]

    print(tabulate(results, headers=field_names, tablefmt='fancy_grid'))

def fn_connections():
    query = "SELECT IFNULL(usr,'All Users') user,IFNULL(hst,'All Hosts') host,COUNT(1) Connections FROM ( SELECT user usr,LEFT(host,LOCATE (':',host) - 1) hst FROM information_schema.processlist WHERE user NOT IN ('system user','root')) A GROUP BY usr,hst WITH ROLLUP;"
    mycursor.execute(query)
    results = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]

    print(tabulate(results, headers=field_names, tablefmt='fancy_grid'))

def fn_bufferpool_eff():
    print()
    mycursor.execute("select variable_value from performance_schema.global_status where variable_name = 'Innodb_buffer_pool_read_requests'")
    bpoolrr = mycursor.fetchone()
    for row1 in bpoolrr:
        print ("Innodb_buffer_pool_read_requests:", row1)

    mycursor.execute("select variable_value from performance_schema.global_status where variable_name = 'Innodb_buffer_pool_reads'")
    bpoolr = mycursor.fetchone()
    for row2 in bpoolr:
        print ("Innodb_buffer_pool_reads:", row2)

    print()
    print (color.YELLOW + "Innodb buffer pool efficiency is:", round(int(row2)/int(row1) * 100, 2), "% reads from disk." + color.END)
    print()
    mycursor.execute("select variable_value from performance_schema.global_status where variable_name = 'Innodb_buffer_pool_pages_total'")
    pool_page_total = mycursor.fetchone()
    for row3 in pool_page_total:
        print ("Innodb_buffer_pool_pages_total:", row3)

    mycursor.execute("select variable_value from performance_schema.global_status where variable_name = 'Innodb_buffer_pool_pages_free'")
    pool_page_free = mycursor.fetchone()
    for row4 in pool_page_free:
        print ("Innodb_buffer_pool_pages_free:", row4)
    bp_free = round(int(row4), 2)
    bp_total = round(int(row3), 2)

    x = (bp_total - bp_free) / bp_total
    xy = round(x * 100, 2)
    print()
    print (color.YELLOW + "Buffer Pool Utilization: ", xy, "%" + color.END)

def fn_main_menu():
    print ('')
    input("Press Enter to return to menu.")
    clear()

if __name__=='__main__':
    clear()
    while(True):
        print(color.YELLOW + 'MySQL Monitor' + color.END)
        print (HOST, "has:", psutil.cpu_count(), "CPU's")
        print ('CPU Freq', psutil.cpu_freq()[2], "GHz")
        print ('Python Version is:',sys.version[0:5])
        print('Date and Time:',time.asctime())
        print(color.YELLOW + '\nChoose Option:' + color.END)
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
            clear()
            print(color.BLUE + 'Processlist:' + color.END)
            fn_processlist()
            fn_main_menu()
        elif option == 2:
             clear()
             print(color.BLUE + 'Total Connections:' + color.END)
             fn_connections()
             fn_main_menu()
        elif option == 3:
            clear()
            print(color.BLUE + 'Buffer Pool Info:' + color.END)
            fn_bufferpool_eff()
            fn_main_menu()
        elif option == 4:
            clear()

            print('')
            input("Press Enter to return to menu.")
        elif option == 5:
            clear()

            print('')
            input("Press Enter to return to menu.")
        elif option == 6:
            print(color.BOLD + 'System Information:' + color.END)
            print('')

            print('')

            print('')

            print('')

            print('')

            print('')
            input("Press Enter to return to menu.")
        elif option == 7:
            print(color.BOLD + 'CPU Usage:' + color.END)
            clear()
            print('')

            print('')
            input("Press Enter to return to menu.")
        elif option == 0:
             clear()
             print('Have a Nice Day!')
             mydb.close()
             exit()
        else:
             print('Invalid option. Please enter a number between 0 and 7.')
