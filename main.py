import sqlite3
import pandas as pd

from modules.apriori import Apriori
from modules.segmentation import segmentation
from modules.insights import insight_details,get_months_years
from modules.arima_forecast import forecasting
from modules.db_updater import db_updater

# it will contain only retailor specific functions
class  Retailor():

    user_id = 0
    name = 'default'
    user_type = 'customer'
    
    def __init__(self, seg=segmentation(), Apriori = Apriori() ):
        """
            loads respective class's object in Retailor class
        """
        # self.plotting = plotting_sample()
        self.seg = seg
        self.apriori = Apriori
        


    ###############################################################################
    #CLUBBING


    def clubbing(self,id_no):
        """
        use apriori class functions 
        """
        # print('apriori')
        # df = pd.read_sql_query("select * from transactions_1", self.database)
        # data = self.apriori.club(df)
        # print(data.head())

        filename = ""
        
        con = sqlite3.connect('database/new_data.db')
        cursorObj = con.cursor()
        

        cursorObj.execute('SELECT Transactions_table FROM retailor_data where retailor_id = ?',(id_no,))
        rows = cursorObj.fetchall()

        filename_table=''
        for row in rows:
            filename_table = row[0]
            
            print(filename_table)

        # cursorObj.execute('SELECT * FROM {}'.format(filename_table))
        # rows = cursorObj.fetchall()

        # print(rows[0])

        df = pd.read_sql_query("SELECT * FROM {}".format(filename_table), con)
        con.close()

        data = pd.DataFrame
        if len(df) < 100000:
            print("Transactions too less for apriori")
        else:    
            data = self.apriori.club(df)
            if data.empty:
                print("No rules generated")
        
        print(data.head())
        

        # pass



    ########################################################
    #FORCASTING


    def timeseries(self,id_no):

        filename = ""
       
        con = sqlite3.connect('database/new_data.db')
        cursorObj = con.cursor()
        transactions = pd.read_sql_query('select * from transactions_'+str(id_no), con)
        db_updater().generate_sales(con, cursorObj, transactions, id_no)


        ## need to add generate sales function as new everytime sales table will be generated as new addition of transactions wont add anything to sales table
        cursorObj.execute('SELECT Sales_table FROM retailor_data where retailor_id = ?',(id_no,))
        rows = cursorObj.fetchall()

        for row in rows:
            filename_table = row[0]
            
            print(filename_table)

        cursorObj.execute('SELECT * FROM {}'.format(filename_table))
        rows = cursorObj.fetchall()

        print(rows[0])

        df = pd.read_sql_query("SELECT * FROM {}".format(filename_table), con)
        con.close()
        print(df.head())
        predictions,possible_min_sales,possible_max_sales,previous_sales = forecasting(df)

        return predictions,possible_min_sales,possible_max_sales,previous_sales





    #####################################################################################
    #SEGMENTS


    def customer_segments(self,id_no):
        """
        plot 2 plots of customer segments after dividing customer in different segments using RFM technique
        """
        filename = ""
        con = sqlite3.connect('database/new_data.db')
        cursorObj = con.cursor()
        
        cursorObj.execute('SELECT Transactions_table FROM retailor_data where retailor_id = ?',(id_no,))
        rows = cursorObj.fetchall()

        filename_table=''
        for row in rows:
            filename_table = row[0]
            
            print(filename_table)

        # cursorObj.execute('SELECT * FROM {}'.format(filename_table))
        # rows = cursorObj.fetchall()

        # print(rows[0])
        
        df = pd.read_sql_query("SELECT * FROM {}".format(filename_table), con)
        con.commit()
        con.close()
        user_map, sales_map, data_of_usermap, data_of_sales_map =  self.seg.get_customer_segments(df)

        # for i in user_map:
        #     print(i, len(user_map[i][0]),  user_map[i][1])

        # for i in sales_map:
        #     print(i, len(sales_map[i][0]),  sales_map[i][1])



        return user_map, sales_map, data_of_usermap, data_of_sales_map
        


    #############################################################
    #INSIGHTS

    def insights(self,id_no):
      
        con = sqlite3.connect('database/new_data.db')
        cursorObj = con.cursor()
        
        cursorObj.execute('SELECT Transactions_table FROM retailor_data where retailor_id = ?',(id_no,))
        rows = cursorObj.fetchall()

        transaction_table = ""
        for row in rows:
            transaction_table = row[0]
            
            print(transaction_table)


        data = pd.read_sql_query("SELECT * FROM {}".format(transaction_table), con)
        invoice_counts,customer_counts,country_best,country_worst,weekly_sales,hourly_sales = insight_details(data)
        months,years = get_months_years(data,invoice_counts)

        print('-----------------------invoice_counts-----------------------')
        print(months,years,list(invoice_counts))


        print('-----------------------customer_counts-----------------------')
        print(months,years,list(customer_counts))


        print('-----------------------country_best-----------------------')
        print(country_best['Country'],country_best['TotalPrice'])


        print('-----------------------country_worst-----------------------')
        print(country_worst['Country'],country_worst['TotalPrice'])


        print('-----------------------weekly_sales-----------------------')
        print(weekly_sales['WeekDay'],weekly_sales['TotalPrice'])


        print('-----------------------hourly_sales-----------------------')
        print(hourly_sales['Hour'],hourly_sales['TotalPrice'])

        con.close()
        return list(months),list(years),list(invoice_counts),list(customer_counts),list(country_best['Country']),list(country_best['TotalPrice']),list(country_worst['Country']),list(country_worst['TotalPrice']),list(weekly_sales['WeekDay']),list(weekly_sales['TotalPrice']),list(hourly_sales['Hour']),list(hourly_sales['TotalPrice'])


    #################################################################
    #LOGIN
    def login(self,email,password):
        
        type_of_user = ""
    
        con = sqlite3.connect('database/new_data.db')
        cursorObj = con.cursor()
        
        cursorObj.execute('SELECT * FROM registration_data where Email = ? AND Password = ?',(email,password,))
        rows = cursorObj.fetchall()

        for row in rows:
            
            details = row

        con.close()
        return details


    ##############################################################
    #REGISTER
    def register(self,name,email,password,type_of_user,phone,transactions_file,store_file):
        db_name = ""
        db_phone = ""
        reply = "created"

        con = sqlite3.connect('database/new_data.db')
        cursorObj = con.cursor()
        
        cursorObj.execute('SELECT Name FROM registration_data where Email = ?',(email,))
        rows = cursorObj.fetchall()
        


        for row in rows:
            db_name = row[0]

            
        cursorObj.execute('SELECT Name FROM registration_data where PhoneNo = ?',(phone,))
        rows = cursorObj.fetchall()
        
        for row in rows:
            db_phone = row[0]
            


        if (db_name == '' and db_phone == ''):

            reply = 'account  created'
            sql = ''' INSERT INTO registration_data(Name,Email,Password,Type,PhoneNo)
                      VALUES(?,?,?,?,?) '''
            details = (name,email,password,type_of_user,phone)
            cursorObj.execute(sql, details)
            
            #getting id which will be main component for distinguishing
        
            cursorObj.execute('select ID from registration_data where Email=? and PhoneNo = ?', (email, phone))
            id_no = cursorObj.fetchall()[0][0]

            if(type_of_user == 'customer'):
                
                # Entering values into customer_data

                sql = ''' INSERT INTO customer_data
                      VALUES(?,?,?) '''
                
                details = (str(id_no), name, "orders_"+str(id_no))
                cursorObj.execute(sql, details)
                
                #creating respective tables
                
                sql = "CREATE TABLE "+ "orders_"+str(id_no) +" (Invoice TEXT, StockCode TEXT, Description TEXT, Quantity INTEGER, InvoiceDate TIMESTAMP, Price REAL, Country TEXT);"
    
                cursorObj.execute(sql)

                print('successfully inserted into customer_data')
            else:
                # Entering values into retailer data
                sql = ''' INSERT INTO retailor_data
                      VALUES(?,?,?,?,?) '''
                
                details = (str(id_no), name, "store_"+str(id_no), "sales_"+str(id_no), "transactions_"+str(id_no))
                cursorObj.execute(sql, details)
                

                # Create respective tables
                
                #sales
                sql = "CREATE TABLE " + "sales_"+str(id_no) +" (Date    DATE, Price REAL);"
                cursorObj.execute(sql)

                #store
                sql = "CREATE TABLE "+"store_" + str(id_no)+" (StockCode    TEXT,Description    TEXT,Price  REAL,Quantity   INTEGER);"
                cursorObj.execute(sql)

                #transactions
                sql = "CREATE TABLE "+ "transactions_"+str(id_no) +" (Invoice TEXT, StockCode TEXT, Description TEXT, Quantity INTEGER, InvoiceDate TIMESTAMP, Price REAL, 'Customer ID' REAL, Country TEXT);"
                cursorObj.execute(sql)

                print('successfully inserted into retailer_data')

                df = pd.read_csv(store_file)
                df2 = pd.read_csv(transactions_file)

                db = db_updater()
                db.upload_csv(con, cursorObj, id_no, df, df2)

         
            
            
            
        elif(db_name != '' and db_phone ==''):
            reply = 'email is already registered'
            
        elif(db_name == '' and db_phone !=''):
            reply = 'phone no is already registered'
           
            
        else:
            reply = 'user account already exist'
            
        con.commit()
        con.close()

        return reply




# this object is for example only
# R = Retailor()
# R.clubbing('Sonu')
# R.customer_segments('Sonu')

# R.forecast()
# R.clubbing()


if __name__ == '__main__':
    
    ##class object
    
    user = Retailor()

    # ##login status
    # loggedIn = False

    # print(user.register('sonu', 'asob@gmail.com', 'aman1234', 'retailer', '82281121355'))
    # # print(user.register('sonu', 'asa@mail.com', 'aman1234', 'customer', '82213121355'))
    
    # print("user after registration")
    
    
    
    
    
    # exit()
    
    
    
    
    #user login
    print('-------------------------------------------LOGIN----------------------------------------')
    print('enter your details : ')
    email = input()
    password = input()


    details = user.login(email,password)

    if(details!=''):
        print(details)
        loggedIn = True
    else:
        print('no such user exist! Enter correct id and Pass')
        loggedIn = False


    # ##user registration
    # print('-------------------------------------------REGISTER----------------------------------------')

    # print('Enter the registration details : ')
    # name = input('Name : ')
    # phone = input('Phone : ')
    # password = input('Password : ')
    # type_of_user = input('Type user : ')
    # email = input('Email : ')



    # reply = user.register(name,email,password,type_of_user,phone,'sample_csv/new_retailer.csv','sample_csv/new_retailer_store.csv')

    # print(reply)


    #forecasting

    name = details[1]
    print(details)
    type_of_user = details[4]
    print(name)

    id_no = details[0]


    if type_of_user=='retailer':
        print('-------------------------------------------FORECAST----------------------------------------')

        predictions,possible_min_sales,possible_max_sales,previous_sales = user.timeseries(id_no)
        print('prediction in main.py : ',predictions)

        print('MAx sales : ',possible_max_sales)
        print('min sales : ',possible_min_sales)
        print('-------------------------------------------INSIGHTS----------------------------------------')

        user.insights(id_no)

        print('-------------------------------------------CLUBBING----------------------------------------')
        user.clubbing(id_no)
        print('-------------------------------------------SEGMENTS----------------------------------------')
        user_map, sales_map, data_of_usermap, data_of_sales_map = user.customer_segments(id_no)
        
        for i in user_map:
            print(i)
        for i in sales_map:
            print(i)
        # print(data_of_usermap)
        # print(data_of_sales_map)

    else:
        print('Customer')
    

    # R.clubbing(name)
    # R.customer_segments(name)
