from flask import Flask,render_template
from flask import request ,jsonify , Response
import sqlite3
import time
import datetime
import random
import json
import numpy
from main import Retailor
# import pandas as pdS

app = Flask(__name__)

def np_to_int(arr):
  for num in arr:
    num = int(num)
  return arr


# #checking and validating user id pass
# def id_pass_check(email,pwd):
# 	name = ''
	
# 	con = sqlite3.connect('database/new_data.db')   #may need to change path of db
# 	cursorObj = con.cursor()
# 	cursorObj.execute('SELECT c_name FROM customer_data where c_login_id = ? AND c_password = ?',(email,pwd,))
# 	rows = cursorObj.fetchall()

# 	for row in rows:

# 		name = row[0]

# 	return name 

# def registering(email,name,phone,password):
# 	db_name = ''
# 	db_phone = ''
# 	reply = 'created'

# 	con = sqlite3.connect('database/Our_data.db')
# 	cursorObj = con.cursor()
# 	cursorObj.execute('SELECT c_name FROM customer_data where c_login_id = ?',(email,))
# 	rows = cursorObj.fetchall()



# 	for row in rows:
# 	    db_name = row[0]

	    
# 	cursorObj.execute('SELECT c_name FROM customer_data where c_ph_no = ?',(phone,))
# 	rows = cursorObj.fetchall()

# 	for row in rows:
# 	    db_phone = row[0]
	    


# 	if (db_name == '' and db_phone == ''):

# 	    reply = 'account can be created'
# 	    sql = ''' INSERT INTO customer_data(c_name,c_ph_no,c_login_id,c_password)
# 	              VALUES(?,?,?,?) '''
# 	    details = (name,phone,email,password)
# 	    cursorObj.execute(sql, details)
	 
	    
	    
	    
# 	elif(db_name != '' and db_phone ==''):
# 	    reply = 'email is already registered'
	    
# 	elif(db_name == '' and db_phone !=''):
# 	    reply = 'phone no is already registered'
	   
	    
# 	else:
# 	    reply = 'user account already exist'
	    
# 	con.commit()

# 	return reply


user = Retailor()
# user_id = ''
# user_name = ''
# user_type = ''


def convert(o):
    if isinstance(o, numpy.int64): return int(o)  
    raise TypeError

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register_page():
	return render_template('register.html')


@app.route('/login')
def login_page():
	return render_template('login.html')

@app.route('/register_user',methods=['POST']) 
def register_user():
	email = request.form['email']
	name = request.form['name']
	phone = request.form['phone']
	password = request.form['pass']
	type_of_user = request.form['type']

	# reply = email+name+phone+password+type_of_user
	reply = user.register(name,email,password,type_of_user,phone)

	return render_template('home.html', mssg=reply,name=None,type_of_user=None)



@app.route('/handle_data', methods=['POST'])
def handle_data():
    email = request.form['email']
    pwd  = request.form['pass']

    print('Email : {}   Pass : {}'.format(email,pwd))

    # string = id_pass_check(email,pwd)
    # return 'Welcome  : ' +string
    # error = None
    # if request.method == 'POST':
    #     if email == 'admin' or pwd == 'admin':
    #         error = 'valid Credentials. Please try again.'
    details = user.login(email,pwd)
    user.user_id = details[0]
    user.name = details[1]
    user.user_type = details[4]
    print('User',user.user_id)

    return jsonify("'Username':'{}','UserID':'{}".format(user.name,user.user_id))


@app.route('/show_data')
def show_data():
    months,years,invoice_counts,customer_counts,country_best_count,country_best_price,country_worst_count,country_worst_price,weekly_sales_days,weekly_sales_price,hourly_sales,hourly_sales_price= user.insights(user.user_id)
    data = {'months':months,'years':years,'invoice_counts':invoice_counts,'customer_counts':customer_counts,
           'country_best_count':country_best_count,'country_best_price':country_best_price,'country_worst_count':country_worst_count,
  'country_worst_price':country_worst_price,'weekly_sales_days':weekly_sales_days,'weekly_sales_price':weekly_sales_price,
  'hourly_sales':hourly_sales,'hourly_sales_price':hourly_sales_price}
    return(json.dumps(data,default=convert))

	# return render_template('transactions.html',months=months,years=years,invoice_counts=invoice_counts,customer_counts=customer_counts,country_best_count=country_best_count,country_best_price=country_best_price,country_worst_count=country_worst_count,country_worst_price=country_worst_price,weekly_sales_days=weekly_sales_days,weekly_sales_price=weekly_sales_price,hourly_sales=hourly_sales,hourly_sales_price=hourly_sales_price)
  

@app.route('/customer_data')
def customer_data():
  usermap = user.customer_segments(user.user_id)
  # lables=['Lost','Potential loyalist','At risk','Promising','Loyal customers','About to sleep','Needing attention','Cant loose them','New customers']
  return jsonify(usermap)


@app.route('/forcast')
def forcast():
    predictions,previous_sales = user.timeseries(user.user_id)
    data = {'predictions':predictions,'previous_sales':previous_sales}
    return(json.dumps(data))


@app.after_request
def add_header(response):
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response




if __name__ == '__main__':
    app.run(debug=True)