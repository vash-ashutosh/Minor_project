from flask import Flask,render_template
from flask import request ,jsonify , Response
import sqlite3
import time
import datetime
import random
print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

import main
# import pandas as pdS

app = Flask(__name__)




#checking and validating user id pass
def id_pass_check(email,pwd):
	name = ""
	
	con = sqlite3.connect('database/new_data.db')
	cursorObj = con.cursor()
	cursorObj.execute('SELECT c_name FROM customer_data where c_login_id = ? AND c_password = ?',(email,pwd,))
	rows = cursorObj.fetchall()

	for row in rows:

		name = row[0]

	return name 

def registering(email,name,phone,password):
	db_name = ""
	db_phone = ""
	reply = "created"

	con = sqlite3.connect('database/Our_data.db')
	cursorObj = con.cursor()
	cursorObj.execute('SELECT c_name FROM customer_data where c_login_id = ?',(email,))
	rows = cursorObj.fetchall()



	for row in rows:
	    db_name = row[0]

	    
	cursorObj.execute('SELECT c_name FROM customer_data where c_ph_no = ?',(phone,))
	rows = cursorObj.fetchall()

	for row in rows:
	    db_phone = row[0]
	    


	if (db_name == '' and db_phone == ''):

	    reply = 'account can be created'
	    sql = ''' INSERT INTO customer_data(c_name,c_ph_no,c_login_id,c_password)
	              VALUES(?,?,?,?) '''
	    details = (name,phone,email,password)
	    cursorObj.execute(sql, details)
	 
	    
	    
	    
	elif(db_name != '' and db_phone ==''):
	    reply = 'email is already registered'
	    
	elif(db_name == '' and db_phone !=''):
	    reply = 'phone no is already registered'
	   
	    
	else:
	    reply = 'user account already exist'
	    
	con.commit()

	return reply






@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/register_user',methods=['POST']) 
def register_user():
	email = request.form['email']
	name = request.form['name']
	phone = request.form['phone']
	password = request.form['password']

	reply = registering(email,name,phone,password)
	

	return reply



@app.route('/handle_data', methods=['POST'])
def handle_data():
    email = request.form['email']
    pwd  = request.form['pass']

    print("Email : {}   Pass : {}".format(email,pwd))

    string = id_pass_check(email,pwd)
    return "Welcome  : " +string

@app.route('/get_data')
def get_data():
	datasets = [{
        'type'                : 'line',
        'data'                : [100, 120, 170, 80, 180, 177, 160,45,467,23,456,12,356,46],
        'backgroundColor'     : 'transparent',
        'borderColor'         : '#007bff',
        'pointBorderColor'    : '#007bff',
        'pointBackgroundColor': '#007bff',
        'fill'                : 'false'

      },
        {
          'type'                : 'line',
          'data'                : [60, 80, 160,45,467,23,456,12,356,46,80, 67, 80, 77, 100],
          'backgroundColor'     : 'tansparent',
          'borderColor'         : '#ced4da',
          'pointBorderColor'    : '#ced4da',
          'pointBackgroundColor': '#ced4da',
          'fill'                : 'false'

        }]

	return jsonify(datasets)

@app.after_request
def add_header(response):
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response
if __name__ == '__main__':
    app.run(debug=True)