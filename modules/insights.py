import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import plotly.express as px
import seaborn as sns
import datetime as datetime
import sqlite3
# import plotly.graph_objs as go
# from plotly.offline import iplot

# import cufflinks
# cufflinks.go_offline()


# cufflinks.set_config_file(world_readable=True, theme='pearl', offline=True)

def insight_details(data):
	transaction_table = 'transactions_2'


	con = sqlite3.connect('database/new_data.db')
	cursorObj = con.cursor()
	cursorObj.execute('SELECT * FROM {}'.format(transaction_table))
	rows = cursorObj.fetchall()


	data = pd.read_sql_query("SELECT * FROM {}".format(transaction_table), con)
	print(data.head())


	data.isnull().sum()

	data.info()

	print('Quantity column')
	print(data.Quantity.describe())
	print('Price column')
	print(data.Price.describe())

	data = data[(data.Quantity>0)&(data.Price>0)]

	data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
	data = data.dropna(subset=['Customer ID'])
	data['CustomerID'] = data['Customer ID']

	data['TotalPrice'] = data['Quantity']*data['Price']
	data['Year'] = pd.DatetimeIndex(data['InvoiceDate']).year
	data['Month'] = pd.DatetimeIndex(data['InvoiceDate']).month


	#number of invoice per month

	invoice_counts = data.groupby(['Year', 'Month']).Invoice.count()
	invoice_counts.plot(kind='bar', title='Amount of invoices per month')
	plt.show()

	print(invoice_counts)


	#number of customer per month

	Customer_count_per_month = data.groupby(['Year', 'Month']).CustomerID.count()
	Customer_count_per_month.plot(kind='bar', title='Amount of customers per month')
	plt.show()

	print(Customer_count_per_month)



	# plt.bar(data[['InvoiceDate','TotalPrice']].set_index('InvoiceDate').resample('M').sum().reset_index(),
	#        x='InvoiceDate', y='TotalPrice', title = 'Total Revenue per month')

	# plt.show()

	#top best country by revenue
	country_pie_best = data.groupby('Country').TotalPrice.sum().reset_index()[:20]
	print(country_pie_best)

	print(country_pie_best['Country'])

	plt.pie(country_pie_best['TotalPrice'],labels=country_pie_best['Country'],autopct='%1.1f%%')
	plt.title('My Title')
	plt.axis('equal')
	plt.show()


	#top worst country by revenue

	country_pie_worst = data.groupby('Country').TotalPrice.sum().reset_index()[20:]
	print(country_pie_worst)

	print(country_pie_worst['Country'])

	plt.pie(country_pie_worst['TotalPrice'],labels=country_pie_worst['Country'],autopct='%1.1f%%')
	plt.title('My Title')
	plt.axis('equal')
	plt.show()



	# weekly sales 

	data['Hour'] = data['InvoiceDate'].dt.hour
	data['WeekDay']=data['InvoiceDate'].dt.weekday
	data['WeekDay'] = data['WeekDay'].replace({0:'Mon', 1:'Thu',2:'Wed', 3:'Thur', 4:'Fri', 5:'Sat', 6:'Sun'})

	weekly_sales = data.groupby('WeekDay').TotalPrice.sum().reset_index()

	print(weekly_sales)

	weekly_sales.plot(kind='bar')
	plt.show()


	#hourly sales

	hourly_sale = data.groupby('Hour').TotalPrice.sum().reset_index()
	print(hourly_sale)
	hourly_sale.plot(kind='bar')
	plt.show()