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
from flask_socketio import SocketIO
from datetime import datetime
from flask_socketio import send, emit
from flask_paginate import Pagination, get_page_args
import click
from flask import Blueprint
from decimal import Decimal
from threading import Lock
account_sid = "AC14da0799655b1ce7bbddefb5ead5ab89"
auth_token  = "67edc7ccf6675e798d2c6f88a93e0851"
client = Client(account_sid, auth_token)
PEOPLE_FOLDER = os.path.join('static', 'people_photo')
time.strftime('%Y-%m-%d %H:%M:%S')
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='bull_local')
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
async_mode = None
thread = None
thread_lock = Lock()
#socketio = SocketIO(app, async_mode=async_mode)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
'''
client.api.account.messages.create(
    to="2409387539",
    from_="+17727424910",
    body="Hello there!")
'''
'''
@socketio.on('message')
def handleMessage(msg):
    for i in range(0,10):
	    emit('message', {'hello': "Hello"})
'''
'''
def background_thread():                                                        
    while True:                                                                 
        socketio.emit('message', 'Welcome - Socket Begin...')                   
        time.sleep(5)
        socketio.emit('message', 'testing connection to backend') 
        time.sleep(5)
        socketio.emit('message', 'connection pending......') 
        time.sleep(5)
        socketio.emit('message', 'connection established') 
        time.sleep(5)
        socketio.emit('message', 'looping content in.....') 
        time.sleep(1)
        socketio.emit('message', '5..') 
        time.sleep(1)
        socketio.emit('message', '4..') 
        time.sleep(1)
        socketio.emit('message', '3..')
        time.sleep(1)
        socketio.emit('message', '2..')
        time.sleep(1)
        socketio.emit('message', '1..') 
        print 'wtf'
'''

def feed():
    cursor = db.cursor(pymysql.cursors.DictCursor)
    query = """
            SELECT action_timestamp from owner_route_task_details order by action_timestamp desc LIMIT 1
            """
    
    cursor.execute(query)
    results = cursor.fetchall()
        
    for row in results:
        t1 = row['action_timestamp']
        print t1
    
    time.sleep(5)
    
    query = """
            SELECT action_timestamp from owner_route_task_details order by action_timestamp desc LIMIT 1
            """

    for row in results:
        t2 = row['action_timestamp']
        print t2
    
    if t2 > t1:
        socketio.emit('database', 'New Ticket') 
    cursor.close()



@socketio.on('connect')                                                         
def runFeed():                                                                  
    global thread                                                               
    if thread is None:                                                          
        thread = socketio.start_background_task(target=feed)  

'''
@socketio.on('connect')                                                         
def connect():                                                                  
    global thread                                                               
    if thread is None:                                                          
        thread = socketio.start_background_task(target=background_thread)  
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
    
@app.route("/voo", methods=['GET','POST'])
def voo(): 
    data = []
    counter = 1
    if request.method == 'POST':
       date   = request.form['date']
       offset  = request.form['offset']
       #counter = request.form['offset']
       cursor = db.cursor(pymysql.cursors.DictCursor)
       counter = offset
       query = """

        select count(owner_id) from
 
        (SELECT DISTINCT(o.proof_picture), o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname)
        from drivers d where d.id = o.assigned_driver) as Driver,
        (select d.cellphone from drivers d where d.id = o.assigned_driver) as "driver_phone",
        (select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #",
        (select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name",
        (select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#",
        (select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) from owners ow where ow.id = o.owner_id )
        as "Owner", o.ticket_number, c.company as "Customer Name" from owner_route_tasks o  
        left join job_details jd on jd.job_code = o.job_code join jobs j on j.id = jd.job_id join customers c on
        c.id = j.customer_id  WHERE o.task_status = 'Completed' and o.date = '%s' ORDER by o.ending_time desc
        )x

        """ %(date)
       cursor.execute(query)
       results = cursor.fetchall()

       for row in results:
           thecount = row['count(owner_id)']
           #print thecount
            
    try:
        query = """
        SELECT DISTINCT(o.proof_picture), o.job_code, o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname) 
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
        c.id = j.customer_id  WHERE o.task_status = 'Completed' and o.date = '%s' ORDER by o.ending_time desc LIMIT 1 offset %s
        """ % (date, offset)
        cursor.execute(query)
        results = cursor.fetchall()
        #import ipdb; ipdb.set_trace()
        for row in results:
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
                'delivery_address':row['type3']
                
                
            })
           
        counter += 1
             
    except:
        
        print "Error:" , sys.exc_info()[0]
    return render_template('voo.html',data=data, counter=counter)
    return jsonify('data',data)



@app.route("/confirmed_image", methods=['GET','POST'])
def confirmed_image():
    if request.method == 'POST':
       owner_id     = request.form['owner_id']
       confirmed    = 'Confirmed'
       driver_name  = request.form['driver_name']
       the_owner    = request.form['the_owner']
       tk_num       = request.form['tk_num']
       com_name     = request.form['com_name']
       curr_date    = request.form['curr_date']
       #user_id  = randint(1, 100)
       now = datetime.now()
       cursor = db.cursor(pymysql.cursors.DictCursor)
       print owner_id
       cursor.execute("INSERT INTO image_verified(owner_id,confirmed,driver_name,the_owner,tk_num,com_name,curr_date,timestamp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (owner_id, confirmed,driver_name,the_owner,tk_num,com_name,curr_date,now))
       db.commit()
       cursor.close()
       return render_template('confirmed_image.html')
     

@app.route("/retake_picture", methods=['GET','POST'])
def retake_picture():
    data = []
    if request.method == 'POST':
       owner_id = request.form['owner_id']
       tk_num       = request.form['tk_num']
       now = datetime.now()
       cursor = db.cursor(pymysql.cursors.DictCursor)
       print owner_id
    try:

        query = """

        SELECT 
        owner_route_task_details.owner_id,owner_route_task_details.truck_id,owner_route_task_details.route_task_id,owner_route_task_details.job_code,
        drivers.fname, drivers.lname, drivers.cellphone
        FROM owner_route_task_details 
        INNER JOIN drivers
              ON owner_route_task_details.owner_id = drivers.owner_id
        WHERE owner_route_task_details.owner_id = '%s' 
        GROUP BY owner_route_task_details.owner_id

        """ % (owner_id)

        cursor.execute(query)
        results = cursor.fetchall()
        #import ipdb; ipdb.set_trace()
        for row in results:
            data.append({
                'fname': row['fname'],
                'lname': row['lname'],
                'cellphone': row['cellphone']
            })
            time       = datetime.now()
            cell       = row['cellphone']
            first_name = row['fname']
            last_name  = row['lname']
            tkid       = row['truck_id']
            route_task = row['route_task_id']
            jobe_code  = row['job_code']
            ownerid    = row['owner_id']
            fname      = row['fname']
            lname      = row['lname']
            print data
        cursor.execute("INSERT INTO SMS (route_task_id, owner_id, truck_id, tk_num, fname, lname, cellphone, timestamp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (route_task, ownerid, tkid,tk_num,fname,lname,cell,time))
        cursor.execute(query)
        db.commit()
        cursor.close()
        #hell = 2409387539
        #cell = makeUSNumber(cell)
        client.api.account.messages.create(
           to=cell, #change to cell for real numbers - using my number right now so I dont bother people
           from_="+17727424910",
           body="Please retake your picture--sorry testing---Disregard!")
    except:
        print "Error:" , sys.exc_info()[0]
    return render_template('retake_confirmed.html')
    return jsonify('data',data)


if __name__ == "__main__":
    #app.secret_key = 'secret123'
    #app.run(debug=True)
    socketio.run(app)
    