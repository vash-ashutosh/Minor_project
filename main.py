from modules.apriori import Apriori
#    apriori.py will contain a class Apriori // similarly with other imported files

from modules.segmentation import segmentation
from sample_plots import plotting_sample
from modules.insights import insight_details,get_months_years
from modules.arima_forecast import forecasting
import sqlite3
import pandas as pd

# it will contain only retailor specific functions
class  Retailor():
    def __init__(self, seg=segmentation(), Apriori = Apriori() ):
        """
            loads respective class's object in Retailor class
        """
        # self.plotting = plotting_sample()
        self.seg = seg
        self.apriori = Apriori
        self.database = sqlite3.connect('./database/new_data.db')
        


    ###############################################################################
    #CLUBBING


    def clubbing(self,name):
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
        cursorObj.execute('SELECT Transactions_table FROM retailor_data where Name = ?',(name,))
        rows = cursorObj.fetchall()

        filename_table=''
        for row in rows:
            filename_table = row[0]
            
            print(filename_table)

        # cursorObj.execute('SELECT * FROM {}'.format(filename_table))
        # rows = cursorObj.fetchall()

        # print(rows[0])

        df = pd.read_sql_query("SELECT * FROM {}".format(filename_table), con)

        print(df.head())
        data = self.apriori.club(df)
        print(data.head())
        # pass



    ########################################################
    #FORCASTING


    def timeseries(self,name):

        filename = ""
        con = sqlite3.connect('database/new_data.db')
        cursorObj = con.cursor()
        cursorObj.execute('SELECT Sales_table FROM retailor_data where Name = ?',(name,))
        rows = cursorObj.fetchall()

        for row in rows:
            filename_table = row[0]
            
            print(filename_table)

        cursorObj.execute('SELECT * FROM {}'.format(filename_table))
        rows = cursorObj.fetchall()

        print(rows[0])

        df = pd.read_sql_query("SELECT * FROM {}".format(filename_table), con)

        print(df.head())


        forecasting(df)



    #####################################################################################
    #SEGMENTS


    def customer_segments(self,name):
        """
        plot 2 plots of customer segments after dividing customer in different segments using RFM technique
        """
        filename = ""
        con = sqlite3.connect('database/new_data.db')
        cursorObj = con.cursor()
        cursorObj.execute('SELECT Transactions_table FROM retailor_data where Name = ?',(name,))
        rows = cursorObj.fetchall()

        filename_table=''
        for row in rows:
            filename_table = row[0]
            
            print(filename_table)

        # cursorObj.execute('SELECT * FROM {}'.format(filename_table))
        # rows = cursorObj.fetchall()

        # print(rows[0])

        df = pd.read_sql_query("SELECT * FROM {}".format(filename_table), con)
        self.seg.get_customer_segments(df)



    #############################################################
    #INSIGHTS

    def insights(self,name):
        con = sqlite3.connect('database/new_data.db')
        cursorObj = con.cursor()
        cursorObj.execute('SELECT Transactions_table FROM retailor_data where Name = ?',(name,))
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


    #################################################################
    #LOGIN
    def login(self,email,password):
        type_of_user = ""
    
        con = sqlite3.connect('database/new_data.db')
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM registration_data where Email = ? AND Password = ?',(email,password,))
        rows = cursorObj.fetchall()

        for row in rows:

            type_of_user = row

        return type_of_user


    ##############################################################
    #REGISTER
    def register(self,name,email,password,type_of_user,phone):
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

            reply = 'account can be created'
            sql = ''' INSERT INTO customer_data(Name,Email,Password,Type,PhoneNo)
                      VALUES(?,?,?,?,?) '''
            details = (name,email,password,type_of_user,phone)
            cursorObj.execute(sql, details)
         
            
            
            
        elif(db_name != '' and db_phone ==''):
            reply = 'email is already registered'
            
        elif(db_name == '' and db_phone !=''):
            reply = 'phone no is already registered'
           
            
        else:
            reply = 'user account already exist'
            
        con.commit()

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

    ##login status
    loggedIn = False

    ##user login
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



    # reply = user.register(name,email,password,type_of_user,phone)

    # print(reply)


    ## forecasting

    name = details[2]
    print(details)
    type_of_user = details[5]
    print(name)


    if type_of_user=='retailer':
        print('-------------------------------------------FORECAST----------------------------------------')

        user.timeseries(name)
        print('-------------------------------------------INSIGHTS----------------------------------------')

        user.insights(name)

        print('-------------------------------------------CLUBBING----------------------------------------')
        user.clubbing(name)
        print('-------------------------------------------SEGMENTS----------------------------------------')
        user.customer_segments(name)


    else:
        print('Customer')
    # user.clubbing()

    # R.clubbing(name)
    # R.customer_segments(name)




