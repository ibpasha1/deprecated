from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, HiddenField
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import time
import json
import os
import sys
from twilio.rest import Client
from random import random
from random import *
#from flask_socketio import SocketIO
import datetime
#from datetime import datetime
#from flask_socketio import send, emit
#from flask_socketio import SocketIO, send, emit
from flask_paginate import Pagination, get_page_args
import click
from flask import Blueprint
from decimal import Decimal
#from threading import Lock
account_sid = "AC14da0799655b1ce7bbddefb5ead5ab89"
auth_token  = "67edc7ccf6675e798d2c6f88a93e0851"
client = Client(account_sid, auth_token)
PEOPLE_FOLDER = os.path.join('static', 'people_photo')
time.strftime('%Y-%m-%d %H:%M:%S')
local = True
if local == True:
	db        = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='bull_local',autocommit=True)
	socketdb1 = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='bull_local',autocommit=True)
	socketdb2 = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='bull_local',autocommit=True)
	socketdb3 = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='bull_local',autocommit=True)
	maindb1   = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='bull_local',autocommit=True)
	maindb2   = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='bull_local',autocommit=True)
	con       = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='bull_local',autocommit=True)
else:
	socketdb1  = pymysql.connect(host='aggdirect.cflbgllnrj45.us-east-1.rds.amazonaws.com', port=3306, user='bulldog', passwd='AThousandRoads2357', db='aggdirect',autocommit=True)
	socketdb2  = pymysql.connect(host='aggdirect.cflbgllnrj45.us-east-1.rds.amazonaws.com', port=3306, user='bulldog', passwd='AThousandRoads2357', db='aggdirect',autocommit=True)
	socketdb3  = pymysql.connect(host='aggdirect.cflbgllnrj45.us-east-1.rds.amazonaws.com', port=3306, user='bulldog', passwd='AThousandRoads2357', db='aggdirect',autocommit=True)
	maindb1    = pymysql.connect(host='aggdirect.cflbgllnrj45.us-east-1.rds.amazonaws.com', port=3306, user='bulldog', passwd='AThousandRoads2357', db='aggdirect',autocommit=True)
	maindb2    = pymysql.connect(host='aggdirect.cflbgllnrj45.us-east-1.rds.amazonaws.com', port=3306, user='bulldog', passwd='AThousandRoads2357', db='aggdirect',autocommit=True)
	db         = pymysql.connect(host='aggdirect.cflbgllnrj45.us-east-1.rds.amazonaws.com', port=3306, user='bulldog', passwd='AThousandRoads2357', db='aggdirect',autocommit=True)

app = Flask(__name__)
#app = Flask(__name__, static_url_path='/static')
#app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app)
#async_mode = None
#thread  = None
#global client_count
#client_count = None


#thread2 = None
#thread_lock = Lock()
#socketio = SocketIO(app, async_mode=async_mode)
#app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
#socketio = SocketIO(app)

max_stmt_length = 1000000000

 
'''
@socketio.on( 'feeder' )
def background_thread(json):
	global client_count
	print "-----------TEST LAST KNOWN FROM CLIENT------------------"
	#last_known   = json['time']
	client_count = json['page']
	#print last_known
	print client_count
	count()
	#button_status()
	return client_count
'''

'''
@socketio.on( 'feed' )
def button_status(json):
	confirm_id = json['confirm_id']
	temp_id = confirm_id
	print "-------------print confirmed ID from button status--------------"
	print temp_id
	cursor_socket1 = socketdb1.cursor(pymysql.cursors.DictCursor)
	query = """
	SELECT confirmed from image_verified where confirm_id = '%s'
	""" %(temp_id)
	cursor_socket1.execute(query)
	results = cursor_socket1.fetchall()
	socketdb1.commit()
	for row in results:
		print "-----------Confirmed ID FROM SERVER 1 ------------------"
		the_status = row['confirmed']
		print "-----------Confirmed ID FROM SERVER 2------------------"
		print the_status
		socketio.emit('disable_status', the_status)
	cursor_socket1.close()
button_status()
'''



'''
@socketio.on( 'feed' )
def feed(json): 
	last_known   = json['last_known']
	print "-------------------LAST KNOWN TICKET TIME FROM CLIENT----------------------"
	print last_known
	current_date = datetime.date.today()
	#current_date = '2017-01-20'
	cursor_socket2 = socketdb2.cursor(pymysql.cursors.DictCursor)
	query = """
		SELECT DISTINCT(o.proof_picture),o.ending_time, o.id, o.job_code, o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname) 
		from drivers d where d.id = o.assigned_driver) as Driver,
		(select d.cellphone from drivers d where d.id = o.assigned_driver) as "driver_phone",
		(select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #", 
		(select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name", 
		(select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#",
		(select jobs.unit_pay from jobs where id = o.owner_id) as "type1",
		(select jobs.pick_address from jobs where id = o.owner_id) as "type2",
		(select jobs.delivery_address from jobs where id = o.owner_id) as "type3",
		(select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) from owners ow where ow.id = o.owner_id )
		as "Owner", o.ticket_number, c.company as "Customer Name" from owner_route_tasks o  
		left join job_details jd on jd.job_code = o.job_code join jobs j on j.id = jd.job_id join customers c  on 
		c.id = j.customer_id  WHERE o.proof_picture <> 'Null' and o.date = '%s' ORDER by o.ending_time desc LIMIT 1 
		""" % (current_date)
	cursor_socket2.execute(query)
	results = cursor_socket2.fetchall()
	for row in results:
		t3          = row['ending_time']
		print "-------------------LAST KNOWN TICKET TIME FROM SERVER----------------------"
		print t3
		owner_id    = row['owner_id']
		driver_name = row['Driver']
		the_owner   = row['Owner']
		#if  t3 > last_known:
		payload = 'Lastest Ticket' + 'Owner id:' +  str(owner_id)  + 'Driver name:' +  str(driver_name) + 'The owner:' +  str(the_owner) 
		emit('ticket', payload)
		emit('time_now', t3)
	 	print "-----------------TICKET------------------"
		print payload
	cursor_socket2.close()
'''

'''
@socketio.on( 'testloop' )
def testloop(json): 
	mess   = json['mess']
	code = 1
	cursor_socket1 = socketdb1.cursor(pymysql.cursors.DictCursor)
	query = """
		SELECT * from feed where code = '%s'
	""" %(code)
	cursor_socket1.execute(query)
	results = cursor_socket1.fetchall()
	socketdb1.commit()
	for row in results:
		ticket = 0
		ticket = row['name']
		socketio.emit('name', ticket)
	 	print "-----------------TICKET------------------"
		print ticket
	cursor_socket1.close()
'''
'''
@socketio.on( 'feeder' )
def count(json): 
	client_count = json['page']
	confirm_id   = json['con']
	print "----------------------LAST KNOWN MAX PAGE NUMBER FROM CLIENT-----------------------"
	print client_count
	current_date = datetime.date.today()
	# if were on localhost we dont have todays dynamic time so we need to hardcode the date
	#current_date = '2017-01-20'
	cursor_socket3 = socketdb3.cursor(pymysql.cursors.DictCursor)
	query = """
		select count(owner_id) from
		(SELECT DISTINCT(o.proof_picture),o.id,o.ending_time, o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname)
		from drivers d where d.id = o.assigned_driver) as Driver,
		(select d.cellphone from drivers d where d.id = o.assigned_driver) as "driver_phone",
		(select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #",
		(select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name",
		(select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#",
		(select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) from owners ow where ow.id = o.owner_id )
		as "Owner", o.ticket_number, c.company as "Customer Name" from owner_route_tasks o  
		left join job_details jd on jd.job_code = o.job_code join jobs j on j.id = jd.job_id join customers c on
		c.id = j.customer_id  WHERE o.task_status = 'Completed' and o.date = '%s' ORDER by o.ending_time desc
		)y
	""" %(current_date)
	cursor_socket3.execute(query)
	results = cursor_socket3.fetchall()
	for row in results:
		thecount = 0
		thecount = row['count(owner_id)']
		socketio.emit('count', thecount)
	 	print "-----------TEST LAST KNOWN MAX PAGE NUMBER FROM SERVER------------------"
		print thecount
	cursor_socket3.close()
	the_status = 0
	print "----------------Confirm_id-------------------------"
	cursor_socket1 = socketdb1.cursor(pymysql.cursors.DictCursor)
	query = """
		SELECT * from image_verified where confirm_id = '%s'
	""" %(confirm_id)
	cursor_socket1.execute(query)
	results = cursor_socket1.fetchall()
	one  = 1
	zero = 0
	for row in results:
		the_status = row['confirmed']
		print "the status-------"
		print the_status
	if the_status > 0:
		socketio.emit('disable_status', one)
	else:
		socketio.emit('disable_status', zero)
#count()





@socketio.on( 'send_message_1' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'image_callback', json, callback=messageRecived )
'''

def makeUSNumber(num):
	result = re.sub('[^0-9]', '', num)
	if result[0] == '1':
		result = '+' + result
	else:
		result = '+1' + result
	if len(result) != 12:
		return 0
	return result


@app.route("/", methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route("/verify", methods=['GET','POST'])
def verify():
	if request.method == 'POST':
		print "REQ OBJ:"
		print request.form
		owner_id     = request.form['owner_id']
		confirmed    = '1'
		SMS          = '0'
		driver_name  = request.form['driver_name']
		the_owner    = request.form['the_owner']
		confirm_id   = request.form['confirm_id']
		com_name     = request.form['com_name']
		curr_date    = request.form['curr_date']
		cell         = request.form['cellphone']
		cursor = db.cursor(pymysql.cursors.DictCursor)
		query = """
		select count(confirmed) from image_verified where confirm_id = '%s'
		""" %(confirm_id)
		cursor.execute(query)
		results = cursor.fetchall()
		for row in results:
			c_id = row['count(confirmed)']
		if c_id == 0:
			cursor.execute("INSERT INTO image_verified(owner_id,confirmed,driver_name,the_owner,confirm_id,com_name,curr_date,cell) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (owner_id, confirmed,driver_name,the_owner,confirm_id,com_name,curr_date,cell))
			db.commit()
			cursor.close()
		return "failed"

@app.route("/retake", methods=['GET','POST'])
def retake():
	if request.method == 'POST':
		print "REQ OBJ:"
		print request.form
		owner_id     = request.form['owner_id']
		confirmed    = '1'
		SMS          = '0'
		driver_name  = request.form['driver_name']
		the_owner    = request.form['the_owner']
		confirm_id   = request.form['confirm_id']
		com_name     = request.form['com_name']
		curr_date    = request.form['curr_date']
		cell         = request.form['cellphone']
		textmessage  = request.form['textmessage']
		#now = datetime.now()
		cursor = db.cursor(pymysql.cursors.DictCursor)
		print owner_id
		cursor.execute("INSERT INTO image_verified(owner_id,confirmed,driver_name,the_owner,confirm_id,com_name,curr_date,cell) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (owner_id, SMS,driver_name,the_owner,confirm_id,com_name,curr_date,cell))
		db.commit()
		cursor.close()
		client.api.account.messages.create(
				to=2409387539, #change to cell for real numbers - using my number right now so I dont bother people
				from_="+17727424910",
				body=textmessage)
	return "success"	

@app.route("/voo", methods=['GET','POST'])
def voo(): 
	data = []
	counter = 1
	status  = 0
	confirm_id = 0
	e_time = 0
	print counter
	if request.method == 'POST':
		print "REQ OBJ: "
		print request.form
		date          = request.form['date']
		offset        = request.form['offset']
		img_status    = request.form['img_status']
		retake_status = request.form['retake_status']
		print offset
		#counter = request.form['offset']
		cursor_main1 = maindb1.cursor(pymysql.cursors.DictCursor)
		counter = offset
		query = """
		select count(owner_id),ending_time from
		(SELECT DISTINCT(o.proof_picture),o.ending_time,o.id, o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname)
		from drivers d where d.id = o.assigned_driver) as Driver,
		(select d.cellphone from drivers d where d.id = o.assigned_driver) as "driver_phone",
		(select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #", 
		(select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name", 
		(select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#",
		(select jobs.unit_pay from jobs where id = o.owner_id) as "type1",
		(select jobs.pick_address from jobs where id = o.owner_id) as "type2",
		(select jobs.delivery_address from jobs where id = o.owner_id) as "type3",
		(select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) from owners ow where ow.id = o.owner_id )
		as "Owner", o.ticket_number, c.company as "Customer Name" from owner_route_tasks o  
		left join job_details jd on jd.job_code = o.job_code  join jobs j on j.id = jd.job_id join customers c  on 
		c.id = j.customer_id   WHERE o.proof_picture <> 'Null' and o.date = '%s' and o.id not in (select confirm_id from image_verified where confirmed = '1') ORDER by o.ending_time desc
		)x
		""" %(date)
		print "PRINT THE QUERY::::::"
		print query
		cursor_main1.execute(query)
		results = cursor_main1.fetchall()
		

		for row in results:
			thecount = row['count(owner_id)']
			e_time   = row['ending_time']
			#print thecount
		#cursor_main1.close()
		print "-------print counter:----------:"
		print counter
		print "-------print the count:----------:"
		print thecount
		print "-------print the E_time:----------:"
		print e_time
	cursor_main2 = maindb2.cursor(pymysql.cursors.DictCursor)
	print 'THIS SHIT BREAKS AND WONT PRINT'
	try:
		query = """
		SELECT DISTINCT(o.proof_picture),o.ending_time,o.id,o.job_code, o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname)
		from drivers d where d.id = o.assigned_driver) as Driver,
		(select d.cellphone from drivers d where d.id = o.assigned_driver) as "driver_phone",
		(select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #", 
		(select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name", 
		(select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#",
		(select jobs.unit_pay from jobs where id = o.owner_id) as "type1",
		(select jobs.pick_address from jobs where id = o.owner_id) as "type2",
		(select jobs.delivery_address from jobs where id = o.owner_id) as "type3",
		(select image_verified.confirmed from image_verified where confirm_id = o.id) as "type4",
		(select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) from owners ow where ow.id = o.owner_id )
		as "Owner", o.ticket_number, c.company as "Customer Name" from owner_route_tasks o  
		left join job_details jd on jd.job_code = o.job_code  join jobs j on j.id = jd.job_id join customers c  on 
		c.id = j.customer_id   WHERE o.proof_picture <> 'Null' and o.date = '%s' and o.id not in (select confirm_id from image_verified where confirmed = '1')  ORDER by o.ending_time asc LIMIT 1 offset %s
		""" % (date, offset)
		print "BEFORE EXECUTE 2nd query"
		cursor_main2.execute(query)
		results = cursor_main2.fetchall()
		print "AFTER EXECUTE 2nd query"
		print counter
		#import ipdb; ipdb.set_trace()
		confirm_id = 'fuku'
		remove_id = 'dk'
		for row in results:
			print "ROW: "
			print row
			data.append({
				'proof_picture': row['proof_picture'],
				'qty': row['qty'],
				'driver': row['Driver'],
				'owner_name': row['Owner'],
				'owner_num': row['Owner Phone#'],
				'ticket_num': row['ticket_number'],
				'customer_name': row['Customer Name'],
				'company_name': row['Company Name'],
				'company_truck': row['Company Truck #'],
				'cell_phone': row['driver_phone'],
				'owner_id': row['owner_id'],
				'job_code': row['job_code'],
				'date': date,
				'thecount':thecount,
				'unit_pay':row['type1'],
				'pick_address':row['type2'],
				'delivery_address':row['type3'],
				'id10':row['id'],
				'timestamp':row['ending_time'],
				'confirmed_id':row['type4']
				
			})
			print data
			owner_id    = row['owner_id']
			confirmed   = '1'
			SMS         = '0'
			driver_name = row['Driver']
			the_owner   = row['Owner']
			confirm_id  = row['id']
			com_name    = row['Company Name']
			curr_date   = date
			cell        = row['driver_phone']
			status      = row['type4']

		print "------------------------CONFIRMED_ID--------------------------------------"
		print confirm_id
		

		#cursor_main2.close()
		counter += 1
		print counter
		
		
	except:
		print "Error V:" , sys.exc_info()[0]
	
	
	print "STATUS: "
	print status
	return render_template('voo.html',data=data, counter=counter, status=status, e_time=e_time)
	#return jsonify({'counter' : counter})
	# return jsonify('data',data)
	

if __name__ == "__main__":
	#app.secret_key = 'secret123'
	app.run(debug=True)
	#socketio.run(app, debug=True)
	