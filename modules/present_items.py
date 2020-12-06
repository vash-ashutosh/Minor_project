import pandas as pd 
import numpy as np 

import sqlite3


def list_of_items_available(filename):

	con = sqlite3.connect('../database/new_data.db')
	cursorObj = con.cursor()
	df = pd.read_sql_query("SELECT * FROM {}".format(filename), con)

	present_items = list(df['Description'])

	return present_items