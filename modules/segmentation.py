import numpy as np
import os
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from modules.utils import *
from datetime import datetime, timedelta
from datetime import *
import matplotlib

class segmentation():

    def __init__(self):
        # self.sales = pd.read_csv(str(os.getcwd())+'/Apriori/onlineretail2_clean.csv')
        self.sales = None
        self.processed_data = None
        self.cluster1_data = None
        self.cluster2_data = None
        self.load()

    def load(self):
        self.cluster1_data = data
        self.cluster2_data = cluster_info

    def get_customer_segments(self,df):
        self.sales = df
        self.preprocess()
        # self.plot()
        # print(self.processed_data['new_label'].unique())
        # print(self.processed_data['new_label'][:10])
        # print(self.processed_data['sales_label'][:10])
        # print(self.processed_data['comms_label'][:10])
    
        return self.get_formatted_data(self.processed_data)
    
    def get_formatted_data(self, df):
        """
        generated map as required by frontend only Customer ID, sales_label, new_label

        structure of map
        {
            'loyal customer' : [ ('set of cutomer IDs' ), 'count'],
            'lost'           : [  (                   ),        ]         
        }
        """
        
        df = df[['Customer ID','new_label','sales_label']]
        


        mp = dict()
        new_label = df['new_label'].unique()

        mp2 = dict()
        sales_label = df['sales_label'].unique()

        for i in new_label:
            mp[i] = [ set(), 0]

        for i in sales_label:
            mp2[i] = [ set(), 0]


        for i in range(len(df)):
            mp[df['new_label'][i]][0].add(df['Customer ID'][i])
            mp2[df['sales_label'][i]][0].add(df['Customer ID'][i])

        for i in mp:
            mp[i][0] = list(mp[i][0])
            mp[i][1] = len(mp[i][0])
        
        for i in mp2:
            mp2[i][0] = list(mp2[i][0])
            mp2[i][1] = len(mp2[i][0])

        # for i in mp2:
        #     print(i, len(mp2[i][0]), mp2[i][1])
        
        # cluster1_data is for mp2 
        # cluster2_data i for mp
        #  
        return mp,mp2,self.cluster2_data,self.cluster1_data

    def preprocess(self):
        # self.sales['InvoiceDate'] = self.sales['InvoiceDate'].astype('string')
        # print(self.sales.info())
        self.sales['InvoiceDate'] = pd.to_datetime((self.sales['InvoiceDate']))
        # print(self.sales.info())
        self.remove_null_data()
        sales = self.sales


        ## Now Lets find the first and second time a customer ordered by aggregating the values
        sales_ = sales.groupby('Invoice').agg(
            Customer =('Customer ID', 'first'),
            InvoiceDate2=('InvoiceDate', 'min'))
        sales_.reset_index(inplace = True)
        sales_['daterank'] = sales_.groupby('Customer')['InvoiceDate2'].rank(method="first", ascending=True)

        # find customers second purchase and name dataframe sales_
        sales_ = sales_[sales_['daterank']== 2]
        sales_.drop(['Invoice', 'daterank'], axis=1, inplace=True)
        sales_.columns = ['Customer ID', 'InvoiceDate2']
    
        sales['amount'] = sales['Price']*sales['Quantity']
        
        salesgroup = sales.groupby('Customer ID').agg(
            Country=('Country', 'first'),
            sum_price=('Price', 'sum'),
            sum_quantity=('Quantity', 'sum'),
            max_date=('InvoiceDate', 'max'),
            min_date=('InvoiceDate', 'min'),
            count_order=('Invoice', 'nunique'),
            avgitemprice=('Price', 'mean'),
            monetary =('amount', 'sum'),
            count_product=('Invoice', 'count'))
        
        salesgroup.reset_index(inplace = True)

        maxdate = sales['InvoiceDate'].max()

        #Calculate AOV. Item per basket
        salesgroup['avgordervalue'] = salesgroup['monetary']/salesgroup['count_order']
        salesgroup['itemsperbasket'] = salesgroup['sum_quantity']/salesgroup['count_order']
        
        # join the data with the dataframe containing customer id with 2nd visits
        salesgroup = pd.merge(salesgroup, sales_ , how='left', on=['Customer ID'])
        
        # find difference between first purchase and 2nd purchase 
        salesgroup['daysreturn'] = salesgroup['InvoiceDate2']- salesgroup['min_date']
        salesgroup['daysreturn'] = salesgroup['daysreturn']/np.timedelta64(1,'D')
        salesgroup['daysmaxmin'] = salesgroup['max_date']- salesgroup['min_date']
        salesgroup['daysmaxmin'] = (salesgroup['daysmaxmin']/np.timedelta64(1,'D')) + 1


        #RFM CALCULATION:
        salesgroup['frequency'] = np.where(salesgroup['count_order'] >1,salesgroup['count_order']/salesgroup['daysmaxmin'],0)
        salesgroup['recency']  = maxdate- salesgroup['max_date']
        salesgroup['recency'] = salesgroup['recency']/np.timedelta64(1,'D')


        # Now we have the values for Recency, Frequency and Monetary parameters. Each customer will get a note between 1 and 4 for each parameter.
        #By Applying quantile method we group each quantile into 25% of the population. 


        #so letsdefine the quantile and save it ina dictionary
        quintiles = salesgroup[['recency', 'frequency', 'monetary']].quantile([.25, .50, .75]).to_dict()
        quintiles2 = salesgroup[['recency', 'frequency', 'monetary']].quantile([.2, .4, 0.6, .8]).to_dict()

        #lets get the RFM values by calling the function above

        salesgroup['R'] = salesgroup['recency'].apply(lambda x: self.r_score(x, quintiles))
        salesgroup['F'] = salesgroup['frequency'].apply(lambda x: self.fm_score(x, 'frequency', quintiles))
        salesgroup['M'] = salesgroup['monetary'].apply(lambda x: self.fm_score(x, 'monetary', quintiles))

        salesgroup['RFM Score'] = salesgroup['R'].map(str) + salesgroup['F'].map(str) + salesgroup['M'].map(str)
        salesgroup['RFM Score'] = salesgroup['RFM Score'].astype(int)


        pd.DataFrame(salesgroup.dtypes, columns=['Type'])
        salesgroup['RFM Score'] = salesgroup['RFM Score'].astype(int)
       

        salesgroup['comms_label'] = salesgroup.apply(self.rrr, axis=1)
        
        salesgroup['sales_label'] = salesgroup.apply(self.www, axis=1)


        #so letsdefine the quantile and save it ina dictionary
        quintiles2 = salesgroup[['recency', 'frequency', 'monetary']].quantile([.2, .4, 0.6, .8]).to_dict()

        #lets get the RFM values by calling the function above

        salesgroup['R2'] = salesgroup['recency'].apply(lambda y: self.r_score2(y, quintiles2))
        salesgroup['F2'] = salesgroup['frequency'].apply(lambda y: self.fm_score2(y, 'frequency', quintiles2))
        salesgroup['M2'] = salesgroup['monetary'].apply(lambda y: self.fm_score2(y, 'monetary', quintiles2))

        salesgroup['RFM Score2'] = salesgroup['R2'].map(str) + salesgroup['F2'].map(str) + salesgroup['M2'].map(str)
        salesgroup['RFM Score2'] = salesgroup['RFM Score2'].astype(int)

        ##So lets group the customersinto 11 based on RFM scores.

        salesgroup['new_label'] = ''

        salesgroup = self.mapl(salesgroup, (4,5), (4,5), 'Champions')
        salesgroup = self.mapl(salesgroup, (2,5), (3,5), 'Loyal customers')
        salesgroup = self.mapl(salesgroup, (3,5), (1,3), 'Potential loyalist')
        salesgroup = self.mapl(salesgroup, (4,5), (0,1), 'New customers')
        salesgroup = self.mapl(salesgroup, (3,4), (0,1), 'Promising')
        salesgroup = self.mapl(salesgroup, (2,3), (2,3), 'Needing attention')
        salesgroup = self.mapl(salesgroup, (2,3), (0,2), 'About to sleep')
        salesgroup = self.mapl(salesgroup, (0,2), (2,5), 'At risk')
        salesgroup = self.mapl(salesgroup, (0,1), (4,5), 'Cant loose them')
        salesgroup = self.mapl(salesgroup, (1,2), (1,2), 'Hibernating')
        salesgroup = self.mapl(salesgroup, (0,2), (0,2), 'Lost')

        self.processed_data = salesgroup
        
    
    def plot(self):
        # self.plot_sales_plot()
        # self.plot_customer_plot()
        pass
       

    def plot_sales_plot(self):
        # plt.figure()
        fig_size = plt.rcParams["figure.figsize"]
        fig_size[0] = 15
        fig_size[1] = 8
        plt.rcParams["figure.figsize"] = fig_size

        # plt.figure()
        sns.set(style="darkgrid")
        ax = sns.countplot(x="sales_label", data=self.processed_data)
        # plt.scatter(x=[1,2,3,4],y=[1,2,3,4])
        plt.show()
    
    def plot_customer_plot(self):
        ax = sns.countplot(x="new_label", data=self.processed_data)
        plt.show()




    def r_score(self, x, quintiles):
        if x <= quintiles['recency'][.25]:
            return 1
        elif x <= quintiles['recency'][.50]:
            return 2
        elif x <= quintiles['recency'][.75]:
            return 3
        else:
            return 4
        
    def fm_score(self, x, c, quintiles):
        if x <= quintiles[c][.25]:
            return 1
        elif x <= quintiles[c][.50]:
            return 2
        elif x <= quintiles[c][.75]:
            return 3
        else:
            return 4   

    def rrr(self, salesgroup):
        if salesgroup['RFM Score'] == 111 :
            d = 'Best Customers'
        elif salesgroup['RFM Score'] == 112 :
            d = 'High Spending New Customers'
        elif salesgroup['RFM Score'] == 113 :
            d = 'Lowest Spending Active Loyal Customers'
        elif salesgroup['RFM Score'] == 114 :
            d = 'Lowest Spending Active Loyal Customers'
        elif salesgroup['RFM Score'] == 422 :
            d = 'Churned Best Customers'
        elif salesgroup['RFM Score'] == 421 :
            d = 'Churned Best Customers'
        elif salesgroup['RFM Score'] == 412 :
            d = 'Churned Best Customers'
        elif salesgroup['RFM Score'] == 411 :
            d = 'Churned Best Customers'
        else:
            d = 'Unclassed'
        return d


    def www(self,salesgroup):
        if salesgroup['RFM Score'] == 111 : 
            d = 'Core'
        elif salesgroup['F'] == 1 : 
            d = 'Loyal'
        elif salesgroup['M'] == 1 : 
            d = 'Whales'
        elif salesgroup['F'] == 1 &  salesgroup['M'] == 3: 
            d = 'Promising'
        elif salesgroup['F'] == 1 &  salesgroup['M'] == 4: 
            d = 'Promising'
        elif salesgroup['R'] == 1 & salesgroup['F'] == 4: 
            d = 'Rookies'
        elif salesgroup['R'] == 4 & salesgroup['F'] == 4 : 
            d = 'Slipping'
        else:
            d = 'Unclassed'
        return d
    

    def r_score2(self, y, quintiles2):
        if y <= quintiles2['recency'][.2]:
            return 5
        elif y <= quintiles2['recency'][.4]:
            return 4
        elif y <= quintiles2['recency'][.6]:
            return 3
        elif y <= quintiles2['recency'][.8]:
            return 2
        else:
            return 1
        
    def fm_score2(self, y, k, quintiles2):
        if y <= quintiles2[k][.2]:
            return 1
        elif y <= quintiles2[k][.4]:
            return 2
        elif y <= quintiles2[k][.6]:
            return 3
        elif y <= quintiles2[k][.8]:
            return 4
        else:
            return 5   


    def mapl(self,salesgroup, r_rule, fm_rule, label, colname='new_label'):
        salesgroup.loc[(salesgroup['R2'].between(r_rule[0], r_rule[1]))
                & (salesgroup['F2'].between(fm_rule[0], fm_rule[1])), colname] = label
        return salesgroup
    
    
    def remove_null_data(self):
        bad_words = ['?','?????','back charges','bad quality','Came as green?','Came as green?','cant find','cant find','check','checked','checked','code mix up 72597','code mix up 72597','coding mix up','crushed','crushed','damaged','damaged/dirty','damaged?','damages','damages etc','damages, lost bits etc','damages?','damges','Damp and rusty','dirty','dirty, torn, thrown away.','display','entry error','faulty','for show','given away','gone','Gone','incorrect credit','lost','lost in space','lost?','missing','Missing','missing (wrongly coded?)','missing?','missings','reverse mistake','Rusty ','Rusty connections','show','show display','smashed','sold in wrong qnty','This is a test product.','used for show display','wet','wet & rotting','wet and rotting','wet cartons','wet ctn','wet damages','Wet, rusty-thrown away','wet/smashed/unsellable','wrong code','wrong ctn size','Zebra invcing error']
            
        sales = self.sales[self.sales['Price']>= 0]
        sales2 = sales[sales['Description'].isin(bad_words)]
        sales = sales[~sales.apply(tuple,1).isin(sales2.apply(tuple,1))]
        sales.dropna(inplace=True)

        # lets also take out all negative quantity as, they are either returns or errors in the data.
        sales = sales[sales['Quantity'] > 0]
        self.sales = sales
        
        
                

