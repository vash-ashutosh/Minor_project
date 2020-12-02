import numpy as np  
import matplotlib.pyplot as plt  
import pandas as pd  
from mlxtend.frequent_patterns import apriori  
from mlxtend.frequent_patterns import association_rules
import os
class Apriori():

    def __init__(self):
        self.data = pd.read_csv(str(os.getcwd())+'/database/create_manage/retailer/transactions_1.csv')
        self.rules = None
        self.final_rules = None

    def get_rules(self):
        rules = self.rules.copy()

        # RULES WITH CONFIDENSE GREATER THAN 80%
        final_rules = rules[ (rules['lift'] >= 0) &
            (rules['confidence'] >= 0.0) ]
        final_rules = final_rules.sort_values(by=["confidence"], ascending=False)

        # final_rules['antecedents','consequents', 'confidence']
        final_apriori_rules = final_rules[['antecedents','consequents','confidence']]
        self.final_rules = final_rules
        # print(final_rules.head())

    def preprocess(self):
        df = self.data.copy()
        #Droping rows without invoice number
        df.dropna(axis=0, subset=['Invoice'], inplace=True)
        df['Invoice'] = df['Invoice'].astype('str')
        #Droping credit transaction
        df = df[~df['Invoice'].str.contains('C')]
        
        #droping blank description
        df.dropna(axis=0, subset=['Description'], inplace=True)


        # Converting all items in desciption of same invoice to columns 
        basket = (df[df['Country'] == 'France'].groupby(['Invoice', 'Description'])['Quantity']
                .sum().unstack().reset_index().fillna(0)
                .set_index('Invoice'))

            
        # as we are creating a set so we dont need frequencies so if quantity is greater than 1 it is marked as present and when 0 it is absent
        basket_sets = basket.applymap(self.encode_units)
        #one columns of postage is also created so we have to remove it as it only contains post info.
        basket_sets.drop('POSTAGE', inplace=True, axis=1)
        
        #Using Association
        frequent_itemsets = apriori(basket_sets, min_support=0.03, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
        self.rules = rules

    def club(self):
        self.preprocess()
        self.get_rules()
        return self.rules

    def encode_units(self, x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1
