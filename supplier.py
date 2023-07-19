from utils import *
import subprocess as sp
from prettytable import PrettyTable
from datetime import datetime
import pymysql
import pymysql.cursors


def viewOrders(cid, password, cur):
    tmp = sp.call("clear", shell=True)
    query = "   SELECT PRODUCT.PRODUCT_NAME, FACTORY.FACTORY_NAME, QUANTITY, DATE_TIME \
                FROM FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER AS RSPBC, PRODUCT , FACTORY\
                WHERE SUPPLIER_ID = %d AND PRODUCT.PRODUCT_ID = RSPBC.PRODUCT_ID AND FACTORY.FACTORY_ID = RSPBC.FACTORY_ID" % (cid)
    try:
        cur.execute(query)
        results = cur.fetchall()
        if len(results) == 0:
            print("You have no orders\n")
        else:
            print("Your orders are:\n")
            x = PrettyTable()
            x.field_names = ["PRODUCT_NAME","FACTORY_NAME", "QUANTITY", "DATE_TIME"]
            for row in results:
                x.add_row(
                    [row['PRODUCT_NAME'], row['FACTORY_NAME'], row['QUANTITY'], row['DATE_TIME']])
            print(x)
    except Exception as e:
        print("Error: ", e)
        return


def placeOrder(cid, password, cur):
    query = "SELECT PRODUCT_ID, PRODUCT_NAME FROM PRODUCT"
    try:
        cur.execute(query)
        results = cur.fetchall()
        if len(results) == 0:
            print("No products to order")
            return
        else:
            print("Products available for order:\n")
            x = PrettyTable()
            x.field_names = ["PRODUCT_ID", "PRODUCT_NAME"]
            for row in results:
                x.add_row([row['PRODUCT_ID'], row['PRODUCT_NAME']])
            print(x)
            print("Enter product id to order: ")
            pid = int(input())
            if not sanitiseInput(pid):
                return
            query = "   SELECT RP.FACTORY_ID, FACTORY.FACTORY_NAME, QUANTITY \
                        FROM PRODUCT_MADEBY_FACTORY AS RP, FACTORY \
                        WHERE RP.PRODUCT_ID = %d AND FACTORY.FACTORY_ID = RP.FACTORY_ID" % (pid)
            try:
                cur.execute(query)
                results = cur.fetchall()
                if len(results) == 0:
                    print("No factory currently makes the product")
                    return
                else:
                    print("factories making the product:\n")
                    x = PrettyTable()
                    x.field_names = ["FACTORY_ID",
                                     "FACTORY_NAME", "QUANTITY"]
                    for row in results:
                        x.add_row(
                            [row['FACTORY_ID'], row['FACTORY_NAME'], row['QUANTITY']])
                    print(x)
                    r_id = int(input("Enter factory id to order from: "))
                    if not sanitiseInput(r_id):
                        return
                    quantity = int(input("Enter quantity to order: "))
                    if not sanitiseInput(quantity):
                        return
                    valid = False
                    for row in results:
                        if int(row['FACTORY_ID']) == r_id and int(row['QUANTITY']) >= quantity:
                            valid = True
                            break
                    if not valid:
                        print("Invalid order")
                        return

                    query = "   INSERT INTO \
                                FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER(SUPPLIER_ID, \
                                PRODUCT_ID, FACTORY_ID, QUANTITY, DATE_TIME) \
                                VALUES(%d, %d, %d, %d, \'%s\')" % (cid, pid,r_id , quantity, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    try:
                        cur.execute(query)
                        # print("Order placed successfully")
                        query = "   UPDATE SUPPLIER_HAS_PRODUCT \
                                    SET QUANTITY = QUANTITY + %d \
                                    WHERE SUPPLIER_ID = %d AND PRODUCT_ID = %d" % (quantity, cid, pid)
                        try:
                            cur.execute(query)
                            print("Order placed successfully")
                        except Exception as e:
                            print("Error: ", e)
                            return
                    except Exception as e:
                        print("Error: ", e)
                        return

            except Exception as e:
                print("Error: ", e)
                return
    except Exception as e:
        print("Error: ", e)
        return


def viewSupplierProfile(cid, password, cur):
    query = "SELECT * FROM SUPPLIER WHERE SUPPLIER_ID = %d AND PASSWORD = '%s'" % (
        cid, password)
    try:
        cur.execute(query)
        result = cur.fetchall()
        x = PrettyTable()
        x.field_names = ["SUPPLIER_ID", "SUPPLIER_NAME", "PHONE_NO", "ADDRESS"]
        x.add_row([result[0]['SUPPLIER_ID'], result[0]['SUPPLIER_NAME'],
                   result[0]['PHONE_NO'], result[0]['ADDRESS']])
        print(x)

    except Exception as e:
        print("Error: ", e)
        return

def viewInventory(cid,password,cur):
    query = "SELECT PRODUCT.PRODUCT_NAME, QUANTITY \
            FROM SUPPLIER_HAS_PRODUCT AS DS, PRODUCT \
            WHERE SUPPLIER_ID = %d AND PRODUCT.PRODUCT_ID = DS.PRODUCT_ID" % (cid)
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


def supplierOption(ch, cid, password, cur,):
    """
    Fucntions for Supplier
    """
    if(ch == 1):                                # View Orders
        viewOrders(cid, password, cur)
    elif(ch == 2):                              # Place Order
        placeOrder(cid, password, cur)
    elif(ch == 3):                              # View Profile
        viewSupplierProfile(cid, password, cur)
    elif(ch == 4):                              # View Inventory
        viewInventory(cid, password, cur)
    else:
        print("Error: Invalid Option")


def supplierRegister(cur, con):
    """ 
    Function to register a Suppleir
    """
    name = input("Enter Supplier Name: ")
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
    id = int(input("Enter Supplier ID: "))
    if not sanitiseInput(id):
        return
    query = "INSERT INTO \
             SUPPLIER(SUPPLIER_ID,SUPPLIER_NAME,  ADDRESS, PHONE_NO, PASSWORD) \
                VALUES(%d, \'%s\',\'%s\', \'%s\', \'%s\')" % (id, name, address, phone, password)

    try:
        cur.execute(query)
        con.commit()
        print("Supplier registered successfully")
        print("Supplier ID: %d" % (id))
        print("Please remember your supplier id and password")
    except pymysql.err.IntegrityError:
        print("Error: Supllier ID already exists")
        return
    except Exception as e:
        print("Error: ", e)
        return


def deleteSupplier(cur, con):
    """
    Function to delete a Supplier
    """
    print("Enter supplier id: ")
    cid = int(input())
    if(not sanitiseInput(cid)):
        return
    print("Enter supplier password: ")
    password = input()
    if(not sanitiseInput(password)):
        return
    query = "DELETE FROM SUPPLIER WHERE SUPPLIER_ID = %d" % (cid)
    try:
        cur.execute(query)
        print("Supplier deleted successfully")
        con.commit()
    except Exception as e:
        print("Error: ", e)
        return


def supplierLogin(cur, con):
    """
    Function to implement option 1
    """
    print("Enter supplier id: ")
    cid = int(input())
    if(not sanitiseInput(cid)):
        return
    print("Enter supplier password: ")
    password = input()
    if(not sanitiseInput(password)):
        return
    query = "SELECT * FROM SUPPLIER  WHERE SUPPLIER_ID = %d AND PASSWORD = '%s'" % (
        cid, password)
    try:
        cur.execute(query)
    except Exception as e:
        print("Error: ", e)
        return
    result = cur.fetchall()
    if(len(result) == 0):
        print("Invalid supplier id or password")
        return
    else:
        while(1):
            print("Welcome supplier %s" % result[0]['SUPPLIER_NAME'])
            print("1. View Orders")
            print("2. Place Order")
            print("3. View Profile")
            print("4. View Inventory")
            print("5. Logout")
            ch = int(input("Please select an option> "))
            if(ch == 5):
                return
            supplierOption(ch, cid, password, cur)
            con.commit()
"""
result 
[0] -> [SUPPLIER_ID, SUPPLIER_NAME, ADDRESS, PHONE_NO, PASSWORD]
result[0]['SUPPLIER_ID']
"""