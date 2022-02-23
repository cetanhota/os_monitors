#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""""
6/12/2018

@author: wayne

"""""

#import shutil
import time
import os
#import subprocess
import sys
import psutil
import socket
from psutil._common import bytes2human

class color:
        BOLD = '\033[1m'
        END = '\033[0m'
        RED = '\033[91m'

menu_options = {
    1: 'Free Memory',
    2: 'Disk Usage',
    3: 'SWAP Usage',
    4: 'System Load Average',
    5: 'Network Latency Check',
    6: 'System Overview',
    0: 'Exit'
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

HOST = socket.gethostname()
def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def ram():
    # Getting % usage of virtual_memory ( 3rd field)
    tRAM = psutil.virtual_memory()[0]/1024/1024/1024
    aRAM = psutil.virtual_memory()[1]/1024/1024/1024
    print (color.BOLD + 'RAM Usage:' + color.END)
    print ('Total RAM: ', round((tRAM),2),'GB' )
    print ('Avalible RAM: ', round((aRAM), 2),'GB')
    print ('RAM Used is: ', psutil.virtual_memory()[2], '%')

def parttition():
    print (color.BOLD + 'Disk Usage:' + color.END)
    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type","Mount"))
    for part in psutil.disk_partitions(all=False):
        #if os.name == 'nt':
            #if 'cdrom' in part.opts or part.fstype == '':
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                #continue
        usage = psutil.disk_usage(part.mountpoint)
        print(templ % (
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint))

def swap_fn():
        tSWAP = psutil.swap_memory()[0]/1024/1024/1024
        uSWAP = psutil.swap_memory()[1]/1024/1024/1024
        fSWAP = psutil.swap_memory()[2]/1024/1024/1024
        print (color.BOLD + 'SWAP Usage:' + color.END)
        print ('Total SWAP: ',round((tSWAP),2),'GB')
        print ('Used SWAP: ',round((uSWAP),2),'GB')
        print ('Free SWAP: ',round((fSWAP),2),'GB')

def ping_fn():
        server=input("Enter Server Name for Ping Test: ")
        print('\n')
        ping = os.system("ping -c 5 "+server)

def sys_load_avg():
    print (color.BOLD + 'Load Avg:' + color.END)
    sysload5 = psutil.getloadavg()[0]
    sysload10 = psutil.getloadavg()[1]
    sysload15 = psutil.getloadavg()[2]
    print ('5 min Load Avg:', round((sysload5),2))
    print ('10 min Load Avg:', round((sysload10),2))
    print ('15 min Load Avg:', round((sysload15),2))

def clear():
    os.system('clear')

def sysover():
    os.system('clear')
    print(color.BOLD + 'System Information:' + color.END)
    os.system('top -u mysqladm -n 1 -b -m')
    print('')
    free_fn()
    print('')
    swap_fn()
    print('')
    df_fn()
    print('')
    print(color.BOLD + 'MySQL Information:' + color.END)
    os.system('mysqladmin --socket=/home/mysqladm/tmp/mysql.sock status processlist')

if __name__=='__main__':
    clear()
    while(True):
        print(color.BOLD + 'OS Toolbox' + color.END)
        print (HOST, "has:", psutil.cpu_count(), "CPU's")
        print ('CPU Freq', psutil.cpu_freq()[2], "GHz")
        print ('Python Version is:',sys.version[0:5])
        print('Date and Time:',time.asctime())
        print('\nChoose Option: \n')
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
            clear()
            ram()
            print ('')
        elif option == 2:
             clear()
             parttition()
             print ('')
        elif option == 3:
            clear()
            swap_fn()
            print('')
        elif option == 4:
            clear()
            sys_load_avg()
            print('')
        elif option == 5:
            print('')
        elif option == 6:
            print(color.BOLD + 'System Information:' + color.END)
            print('')
            ram()
            print('')
            sys_load_avg()
            print('')
            swap_fn()
            print('')
            parttition()
            print('')
        elif option == 0:
             clear()
             print('Have a Nice Day!')
             exit()
        else:
             print('Invalid option. Please enter a number between 0 and 9.')

            #'print('OS Toolbox\n')',
            #'print (HOST, "has:", psutil.cpu_count(), "CPU's")',
            #'print ('Python Version is:',sys.version[0:5])',
            #'print('Date and Time:',time.asctime())',
            #'print('\nChoose Option: \n')'
