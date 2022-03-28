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
    1: 'Free Memory',
    2: 'Disk Usage',
    3: 'SWAP Usage',
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

#version = mydb.get_server_info()
#stats = mydb.cmd_statistics()

def fn_processlist():
    query = "show processlist"
    mycursor.execute(query)
    results = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]

    print(tabulate(results, headers=field_names, tablefmt='fancy_grid'))
    mydb.close()

def fn_connections():
    query = "SELECT user usr,LEFT(host,LOCATE (':',host) - 1) hst FROM information_schema.processlist WHERE user NOT IN ('system user','root')) A GROUP BY usr,hst WITH ROLLUP"
    mycursor.execute(query)
    results = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]

    print(tabulate(results, headers=field_names, tablefmt='fancy_grid'))
    mydb.close()

if __name__=='__main__':
    clear()
    while(True):
        print(color.YELLOW + 'OS Toolbox' + color.END)
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
            fn_processlist()
            print ('')
        elif option == 2:
             clear()
             fn_connections()
             print ('')
             input("Press Enter to return to menu.")
        elif option == 3:
            clear()
            swap_fn()
            print('')
            input("Press Enter to return to menu.")
        elif option == 4:
            clear()
            sys_load_avg()
            print('')
            input("Press Enter to return to menu.")
        elif option == 5:
            clear()
            ping_fn()
            print('')
            input("Press Enter to return to menu.")
        elif option == 6:
            print(color.BOLD + 'System Information:' + color.END)
            print('')
            check_cpu_percent()
            print('')
            ram()
            print('')
            sys_load_avg()
            print('')
            swap_fn()
            print('')
            partition()
            print('')
            input("Press Enter to return to menu.")
        elif option == 7:
            print(color.BOLD + 'CPU Usage:' + color.END)
            clear()
            print('')
            check_cpu_percent()
            print('')
            input("Press Enter to return to menu.")
        elif option == 0:
             clear()
             print('Have a Nice Day!')
             exit()
        else:
             print('Invalid option. Please enter a number between 0 and 7.')
