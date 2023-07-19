from utils import *
import subprocess as sp
from prettytable import PrettyTable
from datetime import datetime
import pymysql
import pymysql.cursors


def viewOrders(cid, password, cur):
    tmp = sp.call("clear", shell=True)
    query = "   SELECT PRODUCT.PRODUCT_NAME, SUPPLIER.SUPPLIER_NAME, QUANTITY, DATE_TIME \
                FROM SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY AS RSPBC, PRODUCT, SUPPLIER\
                WHERE RETAILER_ID = %d AND PRODUCT.PRODUCT_ID = RSPBC.PRODUCT_ID AND SUPPLIER.SUPPLIER_ID = RSPBC.SUPPLIER_ID" % (cid)
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
            query = "   SELECT RP.SUPPLIER_ID, SP.SUPPLIER_NAME, QUANTITY \
                        FROM SUPPLIER_HAS_PRODUCT AS RP, SUPPLIER AS SP \
                        WHERE RP.PRODUCT_ID = %d AND SP.SUPPLIER_ID = RP.SUPPLIER_ID" % (pid)
            try:
                cur.execute(query)
                results = cur.fetchall()
                if len(results) == 0:
                    print("No supplier currently sells the product")
                    return
                else:
                    print("Supplier selling the product:\n")
                    x = PrettyTable()
                    x.field_names = ["SUPPLIER_ID",
                                     "SUPPLIER_NAME", "QUANTITY"]
                    for row in results:
                        x.add_row(
                            [row['SUPPLIER_ID'], row['SUPPLIER_NAME'], row['QUANTITY']])
                    print(x)
                    r_id = int(input("Enter supplier id to order from: "))
                    if not sanitiseInput(r_id):
                        return
                    quantity = int(input("Enter quantity to order: "))
                    if not sanitiseInput(quantity):
                        return
                    valid = False
                    for row in results:
                        if int(row['SUPPLIER_ID']) == r_id and int(row['QUANTITY']) >= quantity:
                            valid = True
                            break
                    if not valid:
                        print("Invalid order")
                        return

                    query = "   INSERT INTO \
                                SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY(SUPPLIER_ID, \
                                PRODUCT_ID, FACTORY_ID, QUANTITY, DATE_TIME, RETAILER_ID) \
                                VALUES(%d, %d, \
                                (SELECT DISTINCT FACTORY_ID FROM FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER WHERE SUPPLIER_ID = %d), %d,  \
                                  \'%s\',%d)" % (r_id, pid,r_id,  quantity, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),cid)
                    try:
                        cur.execute(query)
                        # print("Order placed successfully")
                        query = "   INSERT INTO  \
                                    RETAILER_HAS_PRODUCT(PRODUCT_ID,RETAILER_ID,QUANTITY) \
                                    VALUES(%d,%d,%d) \
                                    ON DUPLICATE KEY UPDATE QUANTITY = QUANTITY + %d" % (pid, cid, quantity, quantity)
                        try:
                            cur.execute(query)
                        except Exception as e:
                            print("Error: ", e)
                            return
                        query = "UPDATE SUPPLIER_HAS_PRODUCT  \
                                SET QUANTITY = QUANTITY - %d \
                                WHERE SUPPLIER_ID = %d AND PRODUCT_ID = %d" % (quantity, r_id, pid)
                    except Exception as e:
                        print("Error: ", e)
                        return

            except Exception as e:
                print("Error: ", e)
                return
    except Exception as e:
        print("Error: ", e)
        return


def viewRetailerProfile(cid, password, cur):
    query = "SELECT * FROM RETAILER WHERE RETAILER_ID = %d AND PASSWORD = '%s'" % (
        cid, password)
    try:
        cur.execute(query)
        result = cur.fetchall()
        x = PrettyTable()
        x.field_names = ["RETAILER_ID", "RETAILER_NAME", "PHONE_NO", "ADDRESS"]
        x.add_row([result[0]['RETAILER_ID'], result[0]['RETAILER_NAME'],
                   result[0]['PHONE_NO'], result[0]['ADDRESS']])
        print(x)

    except Exception as e:
        print("Error: ", e)
        return

def viewInventory(cid,password,cur):
    query = "SELECT PRODUCT.PRODUCT_NAME, QUANTITY \
            FROM RETAILER_HAS_PRODUCT AS DS, PRODUCT \
            WHERE RETAILER_ID = %d AND PRODUCT.PRODUCT_ID = DS.PRODUCT_ID" % (cid)
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
    elif(ch == 2):                              # Place Order
        placeOrder(cid, password, cur)
    elif(ch == 3):                              # View Profile
        viewRetailerProfile(cid, password, cur)
    elif(ch == 4):                              # View Inventory
        viewInventory(cid, password, cur)
    else:
        print("Error: Invalid Option")


def retailerRegister(cur, con):
    """ 
    Function to register a Retailer
    """
    name = input("Enter Retialer Name: ")
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
    id = int(input("Enter Retailer ID: "))
    if not sanitiseInput(id):
        return
    query = "INSERT INTO \
             RETAILER(RETAILER_ID, RETAILER_NAME,  ADDRESS, PHONE_NO, PASSWORD) \
                VALUES(%d, \'%s\',\'%s\', \'%s\', \'%s\')" % (id, name, address, phone, password)

    try:
        cur.execute(query)
        con.commit()
        print("Retailer registered successfully")
        print("Retailer ID: %d" % (id))
        print("Please remember your Retailer id and password")
    except pymysql.err.IntegrityError:
        print("Error: Retiaer ID already exists")
        return
    except Exception as e:
        print("Error: ", e)
        return


def deleteRetailer(cur, con):
    """
    Function to delete a Retailer
    """
    print("Enter retailer id: ")
    cid = int(input())
    # if(not sanitiseInput(cid)):
    #     return
    print("Enter retialer password: ")
    password = input()
    if(not sanitiseInput(password)):
        return
    query = "DELETE FROM RETAILER WHERE RETAILER_ID = %d" % (cid)
    try:
        cur.execute(query)
        print("Retialer deleted successfully")
        con.commit()
    except Exception as e:
        print("Error: ", e)
        return


def retailerLogin(cur, con):
    """
    Function to implement option 1
    """
    print("Enter retailer id: ")
    cid = int(input())
    if(not sanitiseInput(cid)):
        return
    print("Enter retailer password: ")
    password = input()
    if(not sanitiseInput(password)):
        return
    query = "SELECT * FROM RETAILER  WHERE RETAILER_ID = %d AND PASSWORD = '%s'" % (
        cid, password)
    try:
        cur.execute(query)
    except Exception as e:
        print("Error: ", e)
        return
    result = cur.fetchall()
    if(len(result) == 0):
        print("Invalid retailer id or password")
        return
    else:
        while(1):
            print("Welcome reatiler %s" % result[0]['RETAILER_NAME'])
            print("1. View Orders")
            print("2. Place Order")
            print("3. View Profile")
            print("4. View Inventory")
            print("5. Logout")
            ch = int(input("Please select an option> "))
            if(ch == 5):
                return
            retailerOption(ch, cid, password, cur)
            con.commit()
