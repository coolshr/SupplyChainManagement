from utils import *
import subprocess as sp
from prettytable import PrettyTable
from datetime import datetime
import pymysql
import pymysql.cursors


def viewOrders(cid, password, cur):
    tmp = sp.call("clear", shell=True)
    query = "   SELECT PRODUCT.PRODUCT_NAME, QUANTITY, DATE_TIME \
                FROM RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER AS RSPBC, PRODUCT \
                WHERE CUSTOMER_ID = %d AND PRODUCT.PRODUCT_ID = RSPBC.PRODUCT_ID" % (cid)
    try:
        cur.execute(query)
        results = cur.fetchall()
        if len(results) == 0:
            print("You have no orders\n")
        else:
            print("Your orders are:\n")
            x = PrettyTable()
            x.field_names = ["PRODUCT_NAME", "QUANTITY", "DATE_TIME"]
            for row in results:
                x.add_row([row['PRODUCT_NAME'], row['QUANTITY'], row['DATE_TIME']])
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
            query = "   SELECT RP.RETAILER_ID, RETAILER.RETAILER_NAME, QUANTITY \
                        FROM RETAILER_HAS_PRODUCT AS RP, RETAILER \
                        WHERE RP.PRODUCT_ID = %d AND RETAILER.RETAILER_ID = RP.RETAILER_ID" % (pid)
            try:
                cur.execute(query)
                results = cur.fetchall()
                if len(results) == 0:
                    print("No retailer currently sells the product")
                    return
                else:
                    print("Retailers selling the product:\n")
                    x = PrettyTable()
                    x.field_names = ["RETAILER_ID",
                                     "RETAILER_NAME", "QUANTITY"]
                    for row in results:
                        x.add_row(
                            [row['RETAILER_ID'], row['RETAILER_NAME'], row['QUANTITY']])
                    print(x)
                    r_id = int(input("Enter retailer id to order from: "))
                    if not sanitiseInput(r_id):
                        return
                    quantity = int(input("Enter quantity to order: "))
                    if not sanitiseInput(quantity):
                        return
                    valid = False
                    for row in results:
                        if int(row['RETAILER_ID']) == r_id and int(row['QUANTITY']) >= quantity:
                            valid = True
                            break
                    if not valid:
                        print("Invalid order")
                        return

                    query = "   INSERT INTO \
                                RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER(RETAILER_ID, \
                                PRODUCT_ID, CUSTOMER_ID, QUANTITY, DATE_TIME) \
                                VALUES(%d, %d, %d, %d, \'%s\')" % (r_id, pid, cid, quantity, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    try:
                        cur.execute(query)
                    except Exception as e:
                        print("Error: ", e)
                        return
                    query = "   UPDATE RETAILER_HAS_PRODUCT  \
                                SET QUANTITY = QUANTITY - %d \
                                WHERE RETAILER_ID = %d AND PRODUCT_ID = %d" % (quantity, r_id, pid)
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


def writeReview(cid, password, cur):
    tmp = sp.call("clear", shell=True)
    query = "   SELECT PRODUCT.PRODUCT_ID, PRODUCT.PRODUCT_NAME, SUM(RSPBC.QUANTITY) \
                FROM RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER AS RSPBC, PRODUCT \
                WHERE CUSTOMER_ID = %d AND PRODUCT.PRODUCT_ID = RSPBC.PRODUCT_ID \
                GROUP BY PRODUCT.PRODUCT_ID" % (cid)    
    try:
        cur.execute(query)
        results = cur.fetchall()
        if len(results) == 0:
            print("You have no orders\n")
        else:
            print("Your orders are:\n")
            x = PrettyTable()
            x.field_names = ["PRODUCT_ID", "PRODUCT_NAME", "QUANTITY"]
            for row in results:
                x.add_row([row['PRODUCT_ID'], row['PRODUCT_NAME'],
                          row['SUM(RSPBC.QUANTITY)']])
            print(x)
            pid = int(input("Select a product to review>"))
            if not sanitiseInput(pid):
                return
            valid = False
            for row in results:
                if row['PRODUCT_ID'] == pid:
                    valid = True
            if valid == False:
                print("You haven't bought the product yet")
                return
            query = "   SELECT AVG(USER_REVIEW.USER_RATING) \
                        FROM USER_REVIEW \
                        WHERE USER_REVIEW.PRODUCT_ID = %d" % (pid)
            try:
                cur.execute(query)
                results = cur.fetchall()
                if len(results) == 0:
                    print("No reviews for this product")
                    return
                else:
                    print("Average rating for this product is: ",
                          results[0]['AVG(USER_REVIEW.USER_RATING)'])
                rating = int(input("Enter your rating for this product>"))
                if not sanitiseInput(rating):
                    return
                query = "   INSERT INTO USER_REVIEW(CUSTOMER_ID, PRODUCT_ID, USER_RATING) \
                                VALUES(%d, %d, %d)" % (cid, pid, rating)
                try:
                    cur.execute(query)
                    print("Review submitted successfully")
                except pymysql.err.IntegrityError:
                    print(
                        " Error: You have already enterd a review for the product with product id %d" % (pid))
                    return
                except Exception as e:
                    print("Error: ", e, type(e))
                    return
            except Exception as e:
                print("Error: ", e)
                return
    except Exception as e:
        print("Error: ", e)
        return


def viewUserProfile(cid, password, cur):
    query = "SELECT * FROM CUSTOMERS WHERE CUSTOMER_ID = %d AND PASSWORD = '%s'" % (
        cid, password)
    try:
        cur.execute(query)
        result = cur.fetchall()
        x = PrettyTable()
        x.field_names = ["CUSTOMER_ID", "F_NAME", "M_NAME", "L_NAME", "ADDRESS", "PHONE_NO", "EMAIL_ID"]
        x.add_row([result[0]['CUSTOMER_ID'], result[0]['F_NAME'], result[0]['M_NAME'], result[0]['L_NAME'], result[0]['ADDRESS'], result[0]['PHONE_NO'], result[0]['EMAIL_ID']])
        print(x)

    except Exception as e:
        print("Error: ", e)
        return


def cusotmerOption(ch, cid, password, cur,):
    """
    Fucntions for customers
    """
    if(ch == 1):                                # View Orders
        viewOrders(cid, password, cur)
    elif(ch == 2):                              # Place Order
        placeOrder(cid, password, cur)
    elif(ch == 3):                              # Write reviews
        writeReview(cid, password, cur)
    elif(ch == 4):                              # View Profile
        viewUserProfile(cid, password, cur)
    else:
        print("Error: Invalid Option")


def customerRegister(cur, con):
    """ 
    Function to register a customer
    """
    f_name = input("Enter First Name: ")
    if not sanitiseInput(f_name):
        return
    m_name = input("Enter Middle Name: ")
    if not sanitiseInput(m_name):
        return
    l_name = input("Enter Last Name: ")
    if not sanitiseInput(l_name):
        return
    address = input("Enter Address: ")
    if not sanitiseInput(address):
        return
    phone = input("Enter Phone Number: ")
    if not sanitiseInput(phone):
        return
    email = input("Enter Email: ")
    if not sanitiseInput(email):
        return
    password = input("Enter Password: ")
    if not sanitiseInput(password):
        return
    id = int(input("Enter Customer ID: "))
    if not sanitiseInput(id):
        return
    query = "   INSERT INTO \
                CUSTOMERS(CUSTOMER_ID,F_NAME, M_NAME, L_NAME, ADDRESS, PHONE_NO, EMAIL_ID, PASSWORD) \
                VALUES(%d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % (id,
                f_name, m_name, l_name, address, phone, email, password)
    try:
        cur.execute(query)
        con.commit()
        print("Customer registered successfully")
        print("Customer ID: %d" % (id))
        print("Please remember your customer id and password")
    except pymysql.err.IntegrityError:
        print("Error: Customer ID already exists")
        return
    except Exception as e:
        print("Error: ", e)
        return


def deleteCustomer(cur, con):
    """
    Function to delete a customer
    """
    print("Enter customer id: ")
    cid = int(input())
    # if(not sanitiseInput(cid)):
    #     return
    print("Enter customer password: ")
    password = input()
    if(not sanitiseInput(password)):
        return
    query = "DELETE FROM CUSTOMERS WHERE CUSTOMER_ID = %d" % (cid)
    try:
        cur.execute(query)
        print("Customer deleted successfully")
        con.commit()
    except Exception as e:
        print("Error: ", e)
        return

def customerLogin(cur, con):
    """
    Function to implement option 1
    """
    print("Enter customer id: ")
    cid = int(input())
    if(not sanitiseInput(cid)):
        return
    print("Enter customer password: ")
    password = input()
    if(not sanitiseInput(password)):
        return
    query = "SELECT * FROM CUSTOMERS WHERE CUSTOMER_ID = %d AND PASSWORD = '%s'" % (
        cid, password)
    try:
        cur.execute(query)
    except Exception as e:
        print("Error: ", e)
        return
    result = cur.fetchall()
    if(len(result) == 0):
        print("Invalid customer id or password")
        return
    else:
        while(1):
            print("Welcome Customer %s" % result[0]['F_NAME'])
            print("1. View Orders")
            print("2. Place Order")
            print("3. Write reviews")
            print("4. View Profile")
            print("5. Logout")
            ch = int(input("Please select an option> "))
            if(ch == 5):
                return
            cusotmerOption(ch, cid, password, cur)
            con.commit()
