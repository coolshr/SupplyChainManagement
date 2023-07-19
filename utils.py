def sanitiseInput(input):
    """
    Function to sanitise input
    """
    if((str(input).find(';') >= 0) or (str(input).find('\'') >= 0) or (str(input).find('\"') >= 0)):
        print("Heeckeeeer!!!!")
        print("Please don't hack us by SQL injection")
        return False
    else:
        return True



def init():
    # The function connects to the db and initializes the cursor
    import pymysql.cursors
    import pymysql
    try:
        con = pymysql.connect(host='localhost',
                              port=30306,
                              user="root",
                              password="1234",
                              db='SUPPLY_CHAIN',
                              cursorclass=pymysql.cursors.DictCursor)
        if(con.open):
            print("Connected to DB")
            return con
    except Exception as e:
        print("Failed to connect")
        print(e)
        return False

