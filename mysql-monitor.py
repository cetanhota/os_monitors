#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""""
3/14/2022
@author: wayne
"""""

import socket
import time
import os
import sys
import mysql.connector
from tabulate import tabulate

class Color:
    '''
    colors
    '''
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
    6: 'Global IO Waits',
    0: 'Exit'
}

if len(sys.argv) < 4:
    print ('Usage:', sys.argv[0], 'server user password')
    sys.exit(1)  # abort because of error
server=sys.argv[1]
user=sys.argv[2]
password=sys.argv[3]

mydb = mysql.connector.connect(
host= server,
auth_plugin='mysql_native_password',
user= user,
password=password)
mycursor = mydb.cursor()

def print_menu():
    '''
    print main menu
    '''
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )
HOST = socket.gethostname()

def clear():
    '''
    clear the screen
    '''
    os.system('clear')

def fn_processlist():
    '''
    show processlist
    '''
    query = "show processlist"
    mycursor.execute(query)
    results = mycursor.fetchall()
    pl_field_names = [i[0] for i in mycursor.description]
    print(tabulate(results, headers=pl_field_names, tablefmt='fancy_grid'))

def fn_connections():
    '''
    show connections
    '''
    query = "SELECT IFNULL(usr,'All Users') user,IFNULL(hst,'All Hosts') \
        host,COUNT(1) Connections FROM ( SELECT user usr,LEFT(host,LOCATE (':',host) - 1) hst \
            FROM information_schema.processlist WHERE user NOT IN ('system user','root')) \
                A GROUP BY usr,hst WITH ROLLUP;"
    mycursor.execute(query)
    results = mycursor.fetchall()
    fnc1_field_names = [i[0] for i in mycursor.description]
    print(tabulate(results, headers=fnc1_field_names, tablefmt='fancy_grid'))

    mycursor.execute("show global status like 'threads_connected'")
    threads_connected = mycursor.fetchall()
    print(tabulate(threads_connected, tablefmt='fancy_grid'))

    mycursor.execute("show global status like 'threads_running'")
    threads_running = mycursor.fetchall()
    print(tabulate(threads_running, tablefmt='fancy_grid'))

    mycursor.execute("SHOW GLOBAL STATUS LIKE 'Connection_errors%';")
    connection_errors = mycursor.fetchall()
    print(tabulate(connection_errors, tablefmt='fancy_grid'))

    mycursor.execute("SHOW GLOBAL STATUS LIKE 'Aborted_c%'")
    connection_aborted = mycursor.fetchall()
    print(tabulate(connection_aborted, tablefmt='fancy_grid'))

def fn_bufferpool_eff():
    '''
    bufferpool information
    '''
    print()
    mycursor.execute("select variable_value \
        from performance_schema.global_status \
            where variable_name = 'Innodb_buffer_pool_read_requests'")
    bpoolrr = mycursor.fetchone()
    row1 = ''
    for row1 in bpoolrr:
        print ("Innodb_buffer_pool_read_requests:", row1)

    mycursor.execute("select variable_value \
        from performance_schema.global_status where variable_name = 'Innodb_buffer_pool_reads'")
    bpoolr = mycursor.fetchone()
    row2 = ''
    for row2 in bpoolr:
        print ("Innodb_buffer_pool_reads:", row2)

    print()
    print (Color.YELLOW + "Only",round(int(row2)/int(row1) * 100, 2),
    "% of Buffer Pool reads come from disk." + Color.END)
    print()
    mycursor.execute("select variable_value \
        from performance_schema.global_status \
            where variable_name = 'Innodb_buffer_pool_pages_total'")
    pool_page_total = mycursor.fetchone()
    row3 = ''
    for row3 in pool_page_total:
        print ("Innodb_buffer_pool_pages_total:", row3)

    mycursor.execute("select variable_value from performance_schema.global_status where \
        variable_name = 'Innodb_buffer_pool_pages_free'")
    pool_page_free = mycursor.fetchone()
    row4 = ''
    for row4 in pool_page_free:
        print ("Innodb_buffer_pool_pages_free:", row4)
    bp_free = round(int(row4), 2)
    bp_total = round(int(row3), 2)

    bp_tot_used = (bp_total - bp_free) / bp_total
    bp_tot_used = round(bp_tot_used * 100, 2)
    print()
    print (Color.YELLOW + "Buffer Pool Utilization: ", bp_tot_used, "%" + Color.END)

def fn_main_menu():
    '''
    main menu
    '''
    print ('')
    input("Press Enter to return to menu.")
    clear()

def fn_query():
    '''
    query info
    '''
    mycursor.execute("select query,db,exec_count,avg_latency from sys.statement_analysis \
        where query not like '%commit%' order by exec_count desc limit 10")
    exe_count = mycursor.fetchall()
    fnq_field_names = [i[0] for i in mycursor.description]
    print()
    print (Color.YELLOW + 'Top 10 queries, based on execute count:' + Color.END)
    print()
    print(tabulate(exe_count, headers=fnq_field_names, tablefmt='fancy_grid'))

    mycursor.execute("show global status like 'questions';")
    questions = mycursor.fetchall()
    questions = (tabulate(questions, tablefmt='plain'))
    questions = (questions.strip('Questions'))
    questions = int(questions)

    mycursor.execute("show global status like 'com_select'")
    com_select = mycursor.fetchall()
    select = (tabulate(com_select, tablefmt='plain'))
    select = (select.strip('Com_select'))
    select = int(select)

    mycursor.execute("show global status like 'com_insert'")
    com_insert = mycursor.fetchall()
    insert = (tabulate(com_insert, tablefmt='plain'))
    insert = (insert.strip('Com_insert'))
    insert = int(insert)

    mycursor.execute(" show global status like 'com_update'")
    com_update = mycursor.fetchall()
    update = (tabulate(com_update, tablefmt='plain'))
    update = (update.strip('Com_update'))
    update = int(update)

    mycursor.execute(" show global status like 'com_delete'")
    com_delete = mycursor.fetchall()
    delete = (tabulate(com_delete, tablefmt='plain'))
    delete = (delete.strip('Com_delete'))
    delete = int(delete)

    writes = delete + update + insert
    print()
    print(Color.YELLOW + 'Read/Write Metrics:' + Color.END)
    print()
    print ("Questions:", questions)
    print ("Selects:", select)
    print ("Writes:", writes)

def fn_global_io_waits():
    '''
    Global IO waits
    '''
    mycursor.execute("select * from sys.waits_global_by_latency;")
    memory_global_total = mycursor.fetchall()
    fng_field_names = [i[0] for i in mycursor.description]
    print(tabulate(memory_global_total, headers=fng_field_names, tablefmt='fancy_grid'))

def fn_memory_usage():
    '''
    memory usage
    '''
    mycursor.execute("select * from sys.memory_global_total;")
    memory_global_total = mycursor.fetchall()
    fnm_field_names = [i[0] for i in mycursor.description]
    print(tabulate(memory_global_total, headers=fnm_field_names, tablefmt='fancy_grid'))

    mycursor.execute("select thread_id,HIGH_NUMBER_OF_BYTES_USED/1024/1024 'MB Used' \
        from performance_schema.memory_summary_by_thread_by_event_name order\
             by HIGH_NUMBER_OF_BYTES_USED desc limit 10")
    memory_by_thread = mycursor.fetchall()
    print()
    print(Color.YELLOW + 'Memory Used per Thread:' + Color.END)
    fnt_field_names = [i[0] for i in mycursor.description]
    print(tabulate(memory_by_thread, headers=fnt_field_names, tablefmt='fancy_grid'))
    print()
    print(Color.YELLOW + 'Bufferpool Memory Breakdown:' + Color.END)
    mycursor.execute("SELECT * FROM sys.memory_global_by_current_bytes \
        WHERE event_name LIKE 'memory/innodb/buf_buf_pool';")
    innodb_bufpool = mycursor.fetchall()
    fnmt_field_names = [i[0] for i in mycursor.description]
    print(tabulate(innodb_bufpool, headers=fnmt_field_names, tablefmt='fancy_grid'))

    mycursor.execute("SELECT ( @@read_buffer_size \
    + @@read_rnd_buffer_size + @@sort_buffer_size \
    + @@join_buffer_size + @@binlog_cache_size + @@thread_stack \
    + @@tmp_table_size \
    + 2*@@net_buffer_length) / (1024 * 1024) AS 'Max memory per Connection.';")
    mem_by_conn = mycursor.fetchall()
    mbc_field_names = [i[0] for i in mycursor.description]
    print(tabulate(mem_by_conn, headers=mbc_field_names, tablefmt='fancy_grid'))


if __name__=='__main__':
    clear()
    while True:
        print(Color.YELLOW + 'MySQL Monitor' + Color.END)
        mycursor.execute("select mysql_version from sys.version;")
        version = mycursor.fetchall()
        ver_field_names = [i[0] for i in mycursor.description]
        print(tabulate(version, headers=ver_field_names, tablefmt='fancy_grid'))

        print ('Python Version is:',sys.version[0:5])
        print('Date and Time:',time.asctime())
        print(Color.YELLOW + '\nChoose Option:' + Color.END)
        print_menu()
        OPTION = ''
        try:
            OPTION = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
            #Check what choice was entered and act accordingly
        if OPTION == 1:
            clear()
            print(Color.BLUE + 'Processlist:' + Color.END)
            fn_processlist()
            fn_main_menu()
        elif OPTION == 2:
            clear()
            print(Color.BLUE + 'Connection Information:' + Color.END)
            fn_connections()
            fn_main_menu()
        elif OPTION == 3:
            clear()
            print(Color.BLUE + 'Buffer Pool Information:' + Color.END)
            fn_bufferpool_eff()
            fn_main_menu()
        elif OPTION == 4:
            clear()
            print(Color.BLUE + 'Query Information:' + Color.END)
            fn_query()
            fn_main_menu()
        elif OPTION == 5:
            clear()
            print(Color.BLUE + 'Memory Usage:' + Color.END)
            fn_memory_usage()
            fn_main_menu()
        elif OPTION == 6:
            clear()
            print(Color.BLUE + 'Global IO Waits' + Color.END)
            fn_global_io_waits()
            fn_main_menu()
        elif OPTION == 0:
            clear()
            print('Have a Nice Day!')
            mydb.close()
            sys.exit()
            break
    else:
        print('Invalid option. Please enter a number between 0 and 6.')
