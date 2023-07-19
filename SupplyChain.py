import subprocess as sp
import pymysql
import pymysql.cursors
from customer import *
from utils import *
from prettytable import PrettyTable
from supplier import *
from retailer import *
from factory import *

def insertNew(cur, con):
    print("Register as new")
    print("1. Customer")
    print("2. Supplier")
    print("3. Retailer")
    print("4. Factory")
    print("5. Exit")
    ch = int(input("Enter your choice: "))
    if(ch == 5):
        return
    elif(ch == 1):
        customerRegister(cur, con)
    elif(ch == 2):
        supplierRegister(cur, con)
    elif(ch == 3):
        retailerRegister(cur, con)
    elif(ch == 4):
        factoryRegister(cur, con)

def deleteID(cur, con):
    print("Delete:")
    print("1. Customer")
    print("2. Supplier")
    print("3. Retailer")
    print("4. Factory")
    print("5. Exit")
    ch = int(input("Enter your choice: "))
    if(ch == 5):
        return
    elif(ch == 1):
        deleteCustomer(cur, con)
    elif(ch == 2):
        deleteSupplier(cur, con)
    elif(ch == 3):
        deleteRetailer(cur, con)
    elif(ch == 4):
        deleteFactory(cur, con)

def dispatch(ch, cur, con):
    """
    Function that maps helper functions to option entered
    """

    if(ch == 1):
        customerLogin(cur, con)
    elif(ch == 2):
        supplierLogin(cur,con)
    elif(ch == 3):
        retailerLogin(cur, con)
    elif(ch == 4):
        factoryLogin(cur, con)
    elif(ch == 5):
        insertNew(cur, con)
    elif(ch == 6):
        deleteID(cur,con)
    else:
        print("Error: Invalid Option")


# Global
while(1):
    tmp = sp.call('clear', shell=True)
    print("Welcome to Supply Chain Management System")

    try:
        # Set db name accordingly which have been create by you
        # Set host to the server's address if you don't want to use local SQL server

        tmp = sp.call('clear', shell=True)
        con = init()
        if(con == False):
            break
        tmp = input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while(1):
                # tmp = sp.call('clear', shell=True)
                print("Login as - ")
                print("1. Customer")
                print("2. Supplier")
                print("3. Retailer")
                print("4. Factory Owner")
                print("5. Make new ID")
                print("6. Delete ID")
                print("7. Logout")
                ch = int(input("Enter choice> "))
                if ch == 7:
                    exit()
                else:
                    dispatch(ch, cur, con)

    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
