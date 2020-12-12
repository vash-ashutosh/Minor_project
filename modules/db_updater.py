import numpy as np
import pandas as pd
import sqlite3


class db_updater():

    def __iniT__(self):
        pass

    def find_next_invoice_no(self, transactions_1):
        
        invoice_1 = transactions_1['Invoice']
        invoice_1 = sorted(invoice_1)
        
        if(len(invoice_1) == 0):
            return str(1)

        count = 0
        
        for i in invoice_1:
            if (i[0] == '1' or i[0] == '2' or i[0] == '3' or i[0] == '4' or i[0] == '5' or i[0] == '6' or i[0] == '7' or i[0] == '8' or i[0] == '9' or i[0] == '0' ):
                count = count + 1
            else:
                break

        if(count>0):
            count = count - 1

        # print("last index : ",count,"| value :", invoice_1[count])
        val = int(invoice_1[count])
        
        # print("next invoice number: ", val+1)
        return str(val+1)

    def update_store(self, retailer_id, stockcode, quantity, cursorObj, con):

        sql = "update store_"+str(retailer_id)+" set Quantity = Quantity - "+str(quantity)+" WHERE StockCode = ?"
        print(retailer_id, stockcode, quantity)
        cursorObj.execute(sql, (stockcode,))
        con.commit()
        print('updated store data of retailer')

    def insert_into_transactions(self, stockcode, description, quantity, price, country, customer_id, retailer_id, con, cursorObj):
    
        #name of retailor's transcations table
        val = cursorObj.execute('select Transactions_table from retailor_data where retailor_id = ?', (retailer_id,))

        transactions_table_name = val.fetchall()
        transactions_table_name = transactions_table_name[0][0]
        print("entered values in transactions_" +  str(retailer_id))

        #updating store_info of retailer
        
        sql = "update store_"+str(retailer_id)+" set Quantity = Quantity - "+str(quantity)+" WHERE StockCode = ?"
        cursorObj.execute(sql, (stockcode,))
        con.commit()
        print('updated store data of retailer_'+str(retailer_id))

        sql = "insert into "+str(transactions_table_name)+" values(?,?,?,?,?,?,?,?);"
        query = "select * from " + transactions_table_name
        
        #getting complete transaction table
        transactions_table = pd.read_sql_query(query,con)
        
        #Getting invoice number
        invoice = self.find_next_invoice_no(transactions_table)
        timestamp =  datetime.datetime.now().replace(microsecond = 0)
            
        details = (invoice, stockcode, description, quantity , timestamp, price, customer_id, country)
        cursorObj.execute(sql, details)

        #Entering in customer order
        sql = "insert into orders_"+str(customer_id)+" values(?,?,?,?,?,?,?);"
        details = (invoice, stockcode, description, quantity , timestamp, price, country)
        cursorObj.execute(sql, details)
        print("entered the placed order in order table of customer_"+str(customer_id))
        con.commit()

        print('successfully completed transcation!')

    def generate_sales(self, con, cursorObj, df, retailer_id):

        df['Price'] = df['Quantity']*df['Price']
        df['InvoiceDate_formatted'] = pd.to_datetime(df['InvoiceDate'])
        df['just_date'] = df['InvoiceDate_formatted'].dt.date
        dates = df['just_date'].unique()
        
        price_list = []
        dates_list = []
        
        for i in dates:
            amount = df[df['just_date'] == i]['Price'].sum()
            dates_list.append(i)
            price_list.append(amount)
        
        df[df['just_date'] == dates[0]]['Price'].sum()
        df = pd.DataFrame(list(zip(dates_list, price_list)), 
                    columns =['Date', 'Price']) 
        
        df.to_sql('sales_'+str(retailer_id),con, if_exists='replace',index = False , schema = 'schema_name') 
        con.commit()

    def upload_csv(self, con, cursorObj, retailer_id, store_info = pd.DataFrame, transactions_info = pd.DataFrame):
        if store_info.empty == False:
            store_info.to_sql("store_"+str(retailer_id), con, index = False, if_exists = 'replace')
            con.commit()
            print("store csv values uploaded in store_"+str(retailer_id))
        else:
            print("store table is empty")
        
        if transactions_info.empty == False:
            transactions_info.to_sql("transactions_"+str(retailer_id), con, index = False, if_exists = 'replace', schema = 'schema_name')
            self.generate_sales(con, cursorObj, transactions_info, retailer_id)
            print('sales_'+str(retailer_id)+' table also generated based on transactions')
            con.commit()
            print("transactions csv values uploaded in transactions_"+str(retailer_id))
        else:
            print("transaction table is empty")




db = db_updater()
con = sqlite3.connect('./database/new_data.db')
cursorObj = con.cursor()
df2 =  pd.read_sql_query('select * from transactions_1', con)
df  =  pd.read_sql_query('select * from store_1', con)
db.upload_csv(con, cursorObj, 1, df, df2)

print("updating for retailer 1")

df2 =  pd.read_sql_query('select * from transactions_2', con)
df  =  pd.read_sql_query('select * from store_2', con)
db.upload_csv(con, cursorObj, 2, df, df2)
print("updating for retailer 2")
con.close()