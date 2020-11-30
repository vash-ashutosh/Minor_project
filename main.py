from modules.apriori import Apriori
#    apriori.py will contain a class Apriori // similarly with other imported files

from modules.segmentation import segmentation
from sample_plots import plotting_sample

# it will contain only retailor specific functions
class  Retailor():
    def __init__(self, seg=segmentation(), Apriori = Apriori()):
        """
            loads respective class's object in Retailor class
        """
        # self.plotting = plotting_sample()
        self.seg = seg
        self.apriori = Apriori
        


    def clubbing(self):
        """
        use apriori class functions 
        """
        # print('apriori')
        self.apriori.show()
        # pass



    def forecast(self):
        plotting_sample()




    def customer_segments(self):
        """
        plot 2 plots of customer segments after dividing customer in different segments using RFM technique
        """
        self.seg.get_customer_segments()



# this object is for example only
R = Retailor()
R.customer_segments()
R.clubbing()
# R.forecast()
# R.clubbing()





