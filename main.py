from modules.apriori import Apriori

#    apriori.py will contain a class Apriori // similarly with other imported files



# it will contain only retailor specific functions
class  Retailor():
    def __init__(self, Apriori = Apriori()):
        """
            loads respective class's object in Retailor class
        """
        self.Apriori = Apriori
        
    def clubbing(self):
        """
        use apriori class functions 
        """
        print('apriori')
        self.Apriori.show()


# this object is for example only
R = Retailor()
R.clubbing()