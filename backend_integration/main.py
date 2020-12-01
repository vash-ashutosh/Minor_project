#from modules.apriori import Apriori

#    apriori.py will contain a class Apriori // similarly with other imported files

from sample_plots import plotting_sample
from arima_forecast import forecasting
import pandas as pd


import sqlite3

# it will contain only retailor specific functions
class  Retailor():
    def __init__(self):
        """
            loads respective class's object in Retailor class
        """
        # self.plotting = plotting_sample()
        
    def clubbing(self):
        """
        use apriori class functions 
        """
        # print('apriori')
        # self.Apriori.show()
        pass

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

    def insights(self):
        pass

    def login(self,email,password):
        type_of_user = ""
    
        con = sqlite3.connect('database/new_data.db')
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM registration_data where Email = ? AND Password = ?',(email,password,))
        rows = cursorObj.fetchall()

        for row in rows:

            type_of_user = row

        return type_of_user

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
        

    def recommend(self):
        pass


        



if __name__ == '__main__':
    
    ##class object
    user = Retailor()

    ##login status
    loggedIn = False

    ##user login
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
    print(name)


    user.timeseries(name)


