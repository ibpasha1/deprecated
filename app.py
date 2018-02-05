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
socketio = SocketIO(app, async_mode=async_mode)
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

def background_thread():
    while True:
        cursor = db.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT tk_num, com_name from image_verified order by timestamp desc LIMIT 1
            """
    
        cursor.execute(query)
        results = cursor.fetchall()
        
        for row in results:
            t1 = row['tk_num']
            t2 = row['com_name']
            print t1
            message = 'Lastest Ticket' + '-'+  str(t1)  + '-'+  str(t2)
            socketio.emit('message', message)
            time.sleep(10)
    


@socketio.on('connect')                                                         
def connect():                                                                  
    global thread                                                               
    if thread is None:                                                          
        thread = socketio.start_background_task(target=background_thread)  


        
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
       date          = request.form['date']
       offset        = request.form['offset']
       img_status    = request.form['img_status']
       retake_status = request.form['retake_status']
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
        (select image_verified.confirmed from image_verified where id = o.owner_id) as "type4",
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
                'delivery_address':row['type3'],
                'confirmed': row['type4']
            })
            owner_id    = row['owner_id']
            confirmed   = 'Confirmed'
            SMS         = 'SMS Sent'
            driver_name = row['Driver']
            the_owner   = row['Owner']
            tk_num      = row['ticket_number']
            com_name    = row['Company Name']
            curr_date   = date
            now         = datetime.now()
            cell        = row['Owner Phone#']
        print img_status
        print retake_status
        if img_status == '1':
            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute("INSERT INTO image_verified(owner_id,confirmed,driver_name,the_owner,tk_num,com_name,curr_date,timestamp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (owner_id, confirmed,driver_name,the_owner,tk_num,com_name,curr_date,now))
            db.commit()
            cursor.close()
        elif retake_status == '1':
            cursor = db.cursor(pymysql.cursors.DictCursor)
            cursor.execute("INSERT INTO image_verified(owner_id,confirmed,driver_name,the_owner,tk_num,com_name,curr_date,timestamp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (owner_id, SMS,driver_name,the_owner,tk_num,com_name,curr_date,now))
            db.commit()
            cursor.close()
            client.api.account.messages.create(
              to=cell, #change to cell for real numbers - using my number right now so I dont bother people
              from_="+17727424910",
              body="Please retake your picture--sorry testing---Disregard!")

        

        counter += 1
             
    except:
        
        print "Error:" , sys.exc_info()[0]
    return render_template('voo.html',data=data, counter=counter)
    return jsonify('data',data)






if __name__ == "__main__":
    #app.secret_key = 'secret123'
    #app.run(debug=True)
    socketio.run(app, debug=True)
    