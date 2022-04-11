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
import getopt

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
    2: 'Connections Information',
    3: 'Innodb Buffer Pool Information',
    4: 'Query Information',
    5: 'Memory Usage',
    6: '',
    7: '',
    0: 'Exit'
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )
HOST = socket.gethostname()

def myfunc(argv):
    arg_server = ""
    arg_user = ""
    arg_password = ""
    arg_help = "{0} -s <server> -u <user> -p <password>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hs:u:p:", ["help", "server=",
        "user=", "password="])
    except:
        print(arg_help)
        sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(arg_help)  # print the help message
                sys.exit(2)
            elif opt in ("-s", "--server"):
                arg_server = arg
            elif opt in ("-u", "--user"):
                arg_user = arg
            elif opt in ("-p", "--password"):
                arg_password = arg

def clear():
    os.system('clear')

mydb = mysql.connector.connect(
host= '192.168.1.61',
auth_plugin='mysql_native_password',
user='pi',
password='hawk69')
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

    mycursor.execute("show global status like 'threads_connected'")
    threads_connected = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    print(tabulate(threads_connected, tablefmt='fancy_grid'))

    mycursor.execute("show global status like 'threads_running'")
    threads_running = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    print(tabulate(threads_running, tablefmt='fancy_grid'))

    mycursor.execute("SHOW GLOBAL STATUS LIKE 'Connection_errors%';")
    connection_errors = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    print(tabulate(connection_errors, tablefmt='fancy_grid'))

    mycursor.execute("SHOW GLOBAL STATUS LIKE 'Aborted_c%'")
    connection_aborted = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    print(tabulate(connection_aborted, tablefmt='fancy_grid'))



    #select variable_name,VARIABLE_VALUE from performance_schema.global_status where variable_name = 'Threads_running';

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
    print (color.YELLOW + "Only",round(int(row2)/int(row1) * 100, 2),"% of Buffer Pool reads come from disk." + color.END)
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

def fn_query():
    mycursor.execute("select query,db,exec_count,err_count,total_latency,max_latency,avg_latency from sys.statement_analysis where query not like '%commit%' order by exec_count desc limit 10")
    exe_count = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    print (color.YELLOW + 'Top 10 queries, based on execute count:' + color.END)
    print(tabulate(exe_count, headers=field_names, tablefmt='fancy_grid'))

    mycursor.execute("show global status like 'questions';")
    questions = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    print(tabulate(questions, tablefmt='fancy_grid'))

    mycursor.execute("show global status like 'com_select'")
    com_select = mycursor.fetchall()
    print(tabulate(com_select, tablefmt='fancy_grid'))

    mycursor.execute("show global status like 'com_insert'")
    com_insert = mycursor.fetchall()
    print(tabulate(com_insert, tablefmt='fancy_grid'))

    mycursor.execute(" show global status like 'com_update'")
    com_update = mycursor.fetchall()
    print(tabulate(com_update, tablefmt='fancy_grid'))

    mycursor.execute(" show global status like 'com_delete'")
    com_delete = mycursor.fetchall()
    print(tabulate(com_delete, tablefmt='fancy_grid')),

    

def fn_memory_usage():
    mycursor.execute("select * from sys.memory_global_total;")
    memory_global_total = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    print(tabulate(memory_global_total, headers=field_names, tablefmt='fancy_grid')),

    mycursor.execute("select thread_id,HIGH_NUMBER_OF_BYTES_USED/1024/1024 'MB Used' from performance_schema.memory_summary_by_thread_by_event_name order by HIGH_NUMBER_OF_BYTES_USED desc limit 10")
    memory_by_thread = mycursor.fetchall()
    print(color.YELLOW + 'Memory Used per Thread:' + color.END)
    field_names = [i[0] for i in mycursor.description]
    print(tabulate(memory_by_thread, headers=field_names, tablefmt='fancy_grid'))
if __name__=='__main__':
    #myfunc(sys.argv)
    clear()
    while(True):
        print(color.YELLOW + 'MySQL Monitor' + color.END)
        mycursor.execute("select mysql_version from sys.version;")
        version = mycursor.fetchall()
        field_names = [i[0] for i in mycursor.description]
        print(tabulate(version, headers=field_names, tablefmt='fancy_grid'))

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
             print(color.BLUE + 'Connection Information:' + color.END)
             fn_connections()
             fn_main_menu()
        elif option == 3:
            clear()
            print(color.BLUE + 'Buffer Pool Information:' + color.END)
            fn_bufferpool_eff()
            fn_main_menu()
        elif option == 4:
            clear()
            print(color.BLUE + 'Query Information:' + color.END)
            fn_query()
            fn_main_menu()
        elif option == 5:
            clear()
            print(color.BLUE + 'Memory Usage:' + color.END)
            fn_memory_usage()
            fn_main_menu()

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
