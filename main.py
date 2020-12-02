from modules.apriori import Apriori
#    apriori.py will contain a class Apriori // similarly with other imported files

from modules.segmentation import segmentation
from sample_plots import plotting_sample
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
        


    def clubbing(self):
        """
        use apriori class functions 
        """
        # print('apriori')
        df = pd.read_sql_query("select * from transactions_1", self.database)
        data = self.apriori.club(df)
        print(data.head())
        # pass


    def forecast(self):
        plotting_sample()


    def customer_segments(self):
        """
        plot 2 plots of customer segments after dividing customer in different segments using RFM technique
        """
        df = pd.read_sql_query("select * from transactions_1", self.database)
        self.seg.get_customer_segments(df)



# this object is for example only
R = Retailor()
R.clubbing()
R.customer_segments()

# R.forecast()
# R.clubbing()





