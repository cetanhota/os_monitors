111
import os
import psutil
import subprocess
import sys

menu_options = {
    1: 'RAM Usage',
    2: 'Total Memory Used',
    3: 'Current CPU Usage',
    4: 'CPU Load Over 15 mins',
    5: 'Exit',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option1():
    clear()
    # Getting % usage of virtual_memory ( 3rd field)
    tRAM = psutil.virtual_memory()[0]/1024/1024/1024
    aRAM = psutil.virtual_memory()[1]/1024/1024/1024
    print('Total RAM: ', round((tRAM),2),'GB' )
    print ('Avalible RAM: ', round((aRAM), 2),'GB')
    print ('RAM Used is: ', psutil.virtual_memory()[2], '%')
    input("Press Enter to return to menu.")

def option2():
    clear()
    # Getting loadover15 minutes
    load15 = psutil.getloadavg()[2]
    cpu_usage = (load15/os.cpu_count()) * 100
    print("The CPU usage is : ", cpu_usage)
    input("Press Enter to return to menu.")

def clear():
    os.system('clear')

def top():
    f = os.popen("top -p 1 -n 1", "r")
    text = f.read()
    print (text)

if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        elif option == 5:
            print('Have a Nice Day!')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 5.')
