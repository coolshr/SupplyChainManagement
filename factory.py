from utils import *
import subprocess as sp
from prettytable import PrettyTable
from datetime import datetime
import pymysql
import pymysql.cursors


def viewOrders(cid, password, cur):
    tmp = sp.call("clear", shell=True)
    query = "   SELECT PRODUCT.PRODUCT_NAME, SUPPLIER.SUPPLIER_NAME, QUANTITY, DATE_TIME \
                FROM FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER AS RSPBC, PRODUCT, SUPPLIER\
                WHERE FACTORY_ID = %d AND PRODUCT.PRODUCT_ID = RSPBC.PRODUCT_ID AND SUPPLIER.SUPPLIER_ID = RSPBC.SUPPLIER_ID" % (cid)
    try:
        cur.execute(query)
        results = cur.fetchall()
        if len(results) == 0:
            print("You have no orders\n")
        else:
            print("Your orders are:\n")
            x = PrettyTable()
            x.field_names = ["PRODUCT_NAME","SUPPLIER_NAME", "QUANTITY", "DATE_TIME"]
            for row in results:
                x.add_row(
                    [row['PRODUCT_NAME'], row['SUPPLIER_NAME'], row['QUANTITY'], row['DATE_TIME']])
            print(x)
    except Exception as e:
        print("Error: ", e)
        return


def viewFactoryProfile(cid, password, cur):
    query = "SELECT * FROM FACTORY WHERE FACTORY_ID = %d AND PASSWORD = '%s'" % (
        cid, password)
    try:
        cur.execute(query)
        result = cur.fetchall()
        x = PrettyTable()
        x.field_names = ["FACTORY_ID", "FACTORY_NAME", "PHONE_NO", "ADDRESS"]
        x.add_row([result[0]['FACTORY_ID'], result[0]['FACTORY_NAME'],
                   result[0]['PHONE_NO'], result[0]['ADDRESS']])
        print(x)

    except Exception as e:
        print("Error: ", e)
        return

def viewInventory(cid,password,cur):
    query = "SELECT PRODUCT.PRODUCT_NAME, QUANTITY \
            FROM PRODUCT_MADEBY_FACTORY AS DS, PRODUCT \
            WHERE FACTORY_ID = %d AND PRODUCT.PRODUCT_ID = DS.PRODUCT_ID" % (cid)
    try:
        cur.execute(query)
        results = cur.fetchall()
        if len(results) == 0:
            print("No products in inventory")
        else:
            print("Products in inventory:\n")
            x = PrettyTable()
            x.field_names = ["PRODUCT_NAME", "QUANTITY"]
            for row in results:
                x.add_row([row['PRODUCT_NAME'], row['QUANTITY']])
            print(x)
    except Exception as e:
        print("Error: ", e)
        return


def retailerOption(ch, cid, password, cur):
    """
    Fucntions for Retailer
    """
    if(ch == 1):                                # View Orders
        viewOrders(cid, password, cur)
    elif(ch == 2):                              # View Profile
        viewFactoryProfile(cid, password, cur)
    elif(ch == 3):                              # View Inventory
        viewInventory(cid, password, cur)
    else:
        print("Error: Invalid Option")

def factoryLogin(cur, con):
    """
    Function to implement option 1
    """
    print("Enter factory id: ")
    cid = int(input())
    if(not sanitiseInput(cid)):
        return
    print("Enter factory password: ")
    password = input()
    if(not sanitiseInput(password)):
        return
    query = "SELECT * FROM FACTORY WHERE FACTORY_ID = %d AND PASSWORD = '%s'" % (
        cid, password)
    try:
        cur.execute(query)
    except Exception as e:
        print("Error: ", e)
        return
    result = cur.fetchall()
    if(len(result) == 0):
        print("Invalid factory id or password")
        return
    else:
        while(1):
            print("Welcome factory %s" % result[0]['FACTORY_NAME'])
            print("1. View Orders")
            print("2. View Profile")
            print("3. View Inventory")
            print("4. Logout")
            ch = int(input("Please select an option> "))
            if(ch == 4):
                return
            retailerOption(ch, cid, password, cur)
            con.commit()


def factoryRegister(cur, con):
    """ 
    Function to register a Retailer
    """
    name = input("Enter Factory Name: ")
    if not sanitiseInput(name):
        return
    address = input("Enter Address: ")
    if not sanitiseInput(address):
        return
    phone = input("Enter Phone Number: ")
    if not sanitiseInput(phone):
        return
    password = input("Enter Password: ")
    if not sanitiseInput(password):
        return
    id = int(input("Enter Factory ID: "))
    if not sanitiseInput(id):
        return
    query = "INSERT INTO \
             FACTORY(FACTORY_ID, FACTORY_NAME,  ADDRESS, PHONE_NO, PASSWORD) \
                VALUES(%d, \'%s\',\'%s\', \'%s\', \'%s\')" % (id, name, address, phone, password)

    try:
        cur.execute(query)
        con.commit()
        print("Factory registered successfully")
        print("Factory ID: %d" % (id))
        print("Please remember your Factory id and password")
    except pymysql.err.IntegrityError:
        print("Error: Factory ID already exists")
        return
    except Exception as e:
        print("Error: ", e)
        return


def deleteFactory(cur, con):
    """
    Function to delete a Factory
    """
    print("Enter factory id: ")
    cid = int(input())
    # if(not sanitiseInput(cid)):
    #     return
    print("Enter factory password: ")
    password = input()
    if(not sanitiseInput(password)):
        return
    query = "DELETE FROM FACTORY WHERE FACTORY_ID = %d AND PASSWORD = \'%s\'" % (cid,password)
    try:
        cur.execute(query)
        print("Factory deleted successfully")
        con.commit()
    except Exception as e:
        print("Error: ", e)
        return
