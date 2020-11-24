from modules.apriori import Apriori

#    apriori.py will contain a class Apriori // similarly with other imported files
from modules.segmentation import segmentation
from sample_plots import plotting_sample

# it will contain only retailor specific functions
class  Retailor():
    def __init__(self, seg=segmentation()):
        """
            loads respective class's object in Retailor class
        """
        # self.plotting = plotting_sample()
        self.seg = seg
        
    def clubbing(self):
        """
        use apriori class functions 
        """
        # print('apriori')
        self.Apriori.show()
        # pass

    def forecast(self):
        plotting_sample()
        
    def customer_segments(self):
        self.seg.preprocess()



# this object is for example only
R = Retailor()
R.customer_segments()
# R.forecast()
# R.clubbing()