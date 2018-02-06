        SELECT 
        job_details.job_id, job_details.job_code, job_details.qty, job_details.is_completed, 
        owner_route_task_details.owner_id, owner_route_task_details.truck_id,
        owner_route_tasks.proof_picture, owner_route_tasks.signature_picture, owner_route_tasks.owner_id,
        drivers.owner_id, drivers.owner_trucking_company, drivers.fname, drivers.lname, drivers.cellphone

        FROM job_details 
        INNER JOIN owner_route_task_details
              ON job_details.job_code = owner_route_task_details.job_code
        INNER JOIN owner_route_tasks 
              ON owner_route_tasks.owner_id = owner_route_task_details.owner_id
        INNER JOIN drivers
              ON drivers.owner_id = owner_route_tasks.owner_id

        WHERE job_details.date = '%s' 
        GROUP BY job_details.job_id




        SELECT 
        job_details.job_id, job_details.job_code, job_details.qty, job_details.is_completed, 
        owner_route_task_details.owner_id, owner_route_task_details.truck_id,
        owner_route_tasks.proof_picture, owner_route_tasks.signature_picture, owner_route_tasks.owner_id,
        drivers.owner_id, drivers.owner_trucking_company, drivers.fname, drivers.lname, drivers.cellphone
        FROM job_details 
        INNER JOIN owner_route_task_details
              ON job_details.job_code = owner_route_task_details.job_code
        INNER JOIN owner_route_tasks 
              ON owner_route_tasks.owner_id = owner_route_task_details.owner_id
        LEFT JOIN drivers
              ON drivers.owner_id = owner_route_task_details.owner_id
        WHERE job_details.date = '%s' 
        GROUP BY job_details.job_id



        SELECT 
        job_details.job_id, job_details.job_code, job_details.qty, job_details.is_completed, 
        owner_route_task_details.owner_id, owner_route_task_details.truck_id,
        owner_route_tasks.proof_picture, owner_route_tasks.signature_picture, owner_route_tasks.owner_id,
        drivers.owner_id, drivers.owner_trucking_company, drivers.fname, drivers.lname, drivers.cellphone
        FROM job_details 
        JOIN owner_route_task_details
              ON job_details.job_code = owner_route_task_details.job_code
        JOIN owner_route_tasks 
              ON owner_route_tasks.owner_id = owner_route_task_details.owner_id
        JOIN drivers
              ON drivers.owner_id = owner_route_task_details.owner_id
        WHERE job_details.date = '%s' 
        GROUP BY job_details.job_id

        //default
        SELECT 
        job_details.job_id, job_details.job_code, job_details.qty, job_details.is_completed, 
        owner_route_task_details.owner_id, owner_route_task_details.truck_id,
        owner_route_tasks.proof_picture, owner_route_tasks.signature_picture, owner_route_tasks.owner_id
        FROM job_details 
        INNER JOIN owner_route_task_details
              ON job_details.job_code = owner_route_task_details.job_code
        INNER JOIN owner_route_tasks 
              ON owner_route_tasks.owner_id = owner_route_task_details.owner_id
        WHERE job_details.date = '%s' 
        GROUP BY job_details.job_id


        SELECT 
        owner_route_tasks.proof_picture, owner_route_tasks.signature_picture, owner_route_tasks.owner_id, owner_route_tasks.job_code, owner_route_tasks.is_completed, owner_route_tasks.qty,
        drivers.owner_id, drivers.owner_trucking_company, drivers.fname, drivers.lname, drivers.cellphone

        FROM owner_route_tasks LEFT JOIN drivers  
             ON owner_route_tasks.owner_id = drivers.owner_id
       
        WHERE owner_route_tasks.date = '%s' 



          SELECT 
        owner_route_tasks.job_code, owner_route_tasks.owner_id, owner_route_tasks.proof_picture, owner_route_tasks.signature_picture,
        owner_route_task_details.owner_id, owner_route_task_details.truck_id,owner_route_task_details.driver_id,
        drivers.owner_id, drivers.cellphone, drivers.fname, drivers.lname
        FROM owner_route_tasks 
        INNER JOIN owner_route_task_details
              ON owner_route_tasks.job_code = owner_route_task_details.job_code
        INNER JOIN drivers 
              ON drivers.owner_id = owner_route_task_details.owner_id
        WHERE owner_route_tasks.date = '%s' 
        GROUP BY owner_route_tasks.job_code


        SELECT drivers.cellphone, drivers.fname, drivers.lname from drivers where driver_id = '%s' 



@app.route("/confirmed_image", methods=['GET','POST'])
def confirmed_image():
    data = []
    if request.method == 'POST':
       driver_id = request.form['driver_id']
       cursor = db.cursor(pymysql.cursors.DictCursor)
    try:

        query = """
       
        INSERT INTO image_verified (driver_id, confirmed) VALUES (driver_id,'1') 
        
        """ % (driver_id)

        cursor.execute(query)
       
    except:
        print "Error:" , sys.exc_info()[0]
    return render_template('voo.html',data=data)
    return jsonify('data',data)


    def get_driver_info():
    date = raw_input("enter date:")
    cursor = db.cursor()
    sql = "SELECT * FROM drivers \
       WHERE modified_timestamp = '%s'" % (date)   
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
          ownerid      = row[1]
          company_name = row[2]
          uname        = row[3]
          dfname       = row[7]
          dlname       = row[9]
          pic          = row[10]
          
    except:
        print ("Error: unable to fetch data")
        sql = "SELECT * FROM trucks \
            WHERE owner_id = '%d'" % (8)
    try:
        cursor.execute(sql)
        res1 = cursor.fetchall()
        for row in res1:
          truckid = row[3]
          clname = row[4]
          print ("ownerid = %s,company_name = %s,uname = %s,dfname = %s,dlname = %s,truckid = %s,clname = %s,pic = %s" % \
             (ownerid,company_name,uname, dfname, dlname,truckid, clname, pic))
          
    
    except:
     print ("Error: unable to fetch data")

    db.close()


     cursor.execute("INSERT INTO SMS (route_task_id, owner_id, truck_id, fname, lname, cellphone, timestamp) VALUES(%s, %s,%s,%s,%s,%s,%s)", (route_task, ownerid, tkid,fname,lname,cell,time))
            cursor.execute(query)



///////---------

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
account_sid = "AC14da0799655b1ce7bbddefb5ead5ab89"
auth_token  = "67edc7ccf6675e798d2c6f88a93e0851"
client = Client(account_sid, auth_token)
PEOPLE_FOLDER = os.path.join('static', 'people_photo')
time.strftime('%Y-%m-%d %H:%M:%S')
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='bull_local')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
'''
client.api.account.messages.create(
    to="2409387539",
    from_="+17727424910",
    body="Hello there!")
'''

@socketio.on('client_connected')
def handle_client_connect_event(json):
    print('received json: {0}'.format(str(json)))

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



@socketio.on('feed')
def handleMessage(msg):
    data = []
    cursor = db.cursor(pymysql.cursors.DictCursor)
    now = datetime.now()
    query = """

        SELECT * from owner_route_task_details where action_timestamp = 'now'

        """
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        data.append({
                'task_id': row['route_task_id'],
                'owner': row['owner_id'],
                'job': row['job_code'],
                'truck': row['truck_id'],
            })
        
    send(data, broadcast=True)


@app.route("/voo", methods=['GET','POST'])
def voo(page=1):
    data = []
    if request.method == 'POST':
       date = request.form['date']
       cursor = db.cursor(pymysql.cursors.DictCursor)
    try:

        query = """
       

        SELECT 
        job_details.job_id, job_details.job_code, job_details.qty, job_details.is_completed, 
        owner_route_task_details.owner_id, owner_route_task_details.truck_id, 
        owner_route_tasks.proof_picture, owner_route_tasks.signature_picture, owner_route_tasks.owner_id
        FROM job_details 
        INNER JOIN owner_route_task_details
              ON job_details.job_code = owner_route_task_details.job_code
        INNER JOIN owner_route_tasks 
              ON owner_route_tasks.owner_id = owner_route_task_details.owner_id
        WHERE job_details.date = '%s' 
        GROUP BY job_details.job_id
        
        
        """ % (date)

        cursor.execute(query)
        results = cursor.fetchall()
        #import ipdb; ipdb.set_trace()
        for row in results:
            data.append({
                'job_id': row['job_id'],
                'job_code': row['job_code'],
                'truck_id': row['truck_id'],
                'qty': row['qty'],
                'is_completed': row['is_completed'],
                'owner_id': row['owner_id'],
                'proof_picture': row['proof_picture'],
                'signature_picture': row['signature_picture']
            })
            print data
    except:
        print "Error:" , sys.exc_info()[0]
    return render_template('voo.html',data=data)
    return jsonify('data',data)



@app.route("/confirmed_image", methods=['GET','POST'])
def confirmed_image():
    if request.method == 'POST':
       owner_id = request.form['owner_id']
       user_id  = randint(1, 100)
       confirmed = 1
       now = datetime.now()
       cursor = db.cursor(pymysql.cursors.DictCursor)
       print owner_id
       cursor.execute("INSERT INTO image_verified(id, owner_id, confirmed) VALUES(%s, %s, %s)", (user_id, owner_id, confirmed))

       db.commit()
       cursor.close()
       return render_template('voo.html')
     

@app.route("/retake_picture", methods=['GET','POST'])
def retake_picture():
    data = []
    if request.method == 'POST':
       owner_id = request.form['owner_id']
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
        cursor.execute("INSERT INTO SMS (route_task_id, owner_id, truck_id, fname, lname, cellphone, timestamp) VALUES(%s, %s,%s,%s,%s,%s,%s)", (route_task, ownerid, tkid,fname,lname,cell,time))
        cursor.execute(query)
        db.commit()
        cursor.close()
        client.api.account.messages.create(
           to=cell, #change to cell for real numbers - using my number right now so I dont bother people
           from_="+17727424910",
           body="Please retake your picture--sorry testing---Disregard!")
    except:
        print "Error:" , sys.exc_info()[0]
    return render_template('voo.html',data=data)
    return jsonify('data',data)


if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)
    












    @app.route('/background_process')
def background_process():
    date = request.args.get('date')
    print date
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:

        query = """
       

        SELECT 
        job_details.job_id, job_details.job_code, job_details.qty, job_details.is_completed, 
        owner_route_task_details.owner_id, owner_route_task_details.truck_id, 
        owner_route_tasks.proof_picture, owner_route_tasks.signature_picture, owner_route_tasks.owner_id
        FROM job_details 
        INNER JOIN owner_route_task_details
              ON job_details.job_code = owner_route_task_details.job_code
        INNER JOIN owner_route_tasks 
              ON owner_route_tasks.owner_id = owner_route_task_details.owner_id
        WHERE job_details.date = '%s' 
        GROUP BY job_details.job_id desc LIMIT 1 offset 1
        
        
        """  %(date)
        #% (date, offset)

        cursor.execute(query)
        results = cursor.fetchall()
        #import ipdb; ipdb.set_trace()
        for row in results:
            data.append({
                'job_id': row['job_id'],
                'job_code': row['job_code'],
                'truck_id': row['truck_id'],
                'qty': row['qty'],
                'is_completed': row['is_completed'],
                'owner_id': row['owner_id'],
                'proof_picture': row['proof_picture'],
                'signature_picture': row['signature_picture'],
                'date': date
            })
        return jsonify(result=job_code)
    except Exception as e:
		return str(e)





         <ul class="collection">
                     <li class="collection-item">job id:{{row['job_id']}}</li>
                     <li class="collection-item">job code:{{row['job_code']}}</li>
                     <li class="collection-item">qty:{{row['qty']}}</li>
                     <li class="collection-item">completed:{{row['is_completed']}}</li>
                     <li class="collection-item">owner id:{{row['owner_id']}}</li>
                     <li class="collection-item">truck id:{{row['truck_id']}}</li>
                     <li class="collection-item">driver id:{{row['driver_id']}}</li>
                     <li class="collection-item">date:{{row['date']}}</li>
                     <li class="collection-item">
                        <form action="/confirmed_image" method="post">
                           <input type="hidden" name="owner_id" value="{{row['owner_id']}}">
                           <input type="submit" class="waves-effect waves-light btn" value="verify">
                        </form>
                     </li>
                     <li class="collection-item">
                        <form action="/retake_picture" method="post">
                           <input type="hidden" name="owner_id" value="{{row['owner_id']}}">
                           <input type="submit" class="waves-effect waves-light btn" value="retake">
                        </form>
                     </li>
                     <li class="collection-item">
                        <form action="/voo" method="post">
                           <input type="hidden" id="myText"   name="date" value="2017-07-01">
                           <input id="page_id"  name="offset" type="hidden" >
                           <input type="submit" class="waves-effect waves-light btn" value="next" onClick="pageUP()">
                        </form>
                     </li>
                  </ul>



                   SELECT DISTINCT(o.proof_picture), o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname) 
        from drivers d where d.id = o.assigned_driver) as Driver,
        (select d.cellphone from drivers d where d.id = o.assigned_driver) as "Driver's Phone#",
        (select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #", 
        (select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name", 
        (select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#",
        (select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) from owners ow where ow.id = o.owner_id )
        as "Owner", o.ticket_number, c.company as "Customer Name" from owner_route_tasks o  
        left join job_details jd on jd.job_code = o.job_code join jobs j on j.id = jd.job_id join customers c on 
        c.id = j.customer_id  WHERE o.task_status = 'Completed' and o.date = '2017-07-01' ORDER by o.ending_time desc LIMIT 1 offset 1



           data.append({
                'fname' : row['fname'],
                'mname' : row['mname'],
                'lname' : row['lname'],
                'cell_phone' : row['cell_phone'],
                'company_truck_number':row['company_truck_number'],
                'trucking_company_name':row['trucking_company_name'],
                'ticket_number': row['ticket_number'],
                'qty': row['qty'],
                'owner_id': row['owner_id'],
                'proof_picture': row['proof_picture'],
                'date': date
            })


             SELECT 
        job_details.job_id, job_details.job_code, job_details.qty, job_details.is_completed, 
        owner_route_task_details.owner_id, owner_route_task_details.truck_id, 
        owner_route_tasks.proof_picture, owner_route_tasks.signature_picture, owner_route_tasks.owner_id
        FROM job_details 
        INNER JOIN owner_route_task_details
              ON job_details.job_code = owner_route_task_details.job_code
        INNER JOIN owner_route_tasks 
              ON owner_route_tasks.owner_id = owner_route_task_details.owner_id
        WHERE job_details.date = '%s' 
        GROUP BY job_details.job_id desc LIMIT 1 offset %s
        



                                 <form action="/confirmed_image" method="post">
                                    <input type="hidden" name="owner_id" value="{{row['owner_id']}}">
                                    <input type="submit" class="waves-effect waves-light btn" value="verify">
                                 </form>
                                 <br>
                                 <form action="/retake_picture" method="post">
                                    <input type="hidden" name="owner_id" value="{{row['owner_id']}}">
                                    <input type="submit" class="waves-effect waves-light btn" value="retake">
                                 </form>
                                 <br>
                                 <form action="/voo" method="post">
                                    <input type="hidden" id="myText"   name="date">
                                    <input id="page_id"  name="offset" type="hidden" >
                                    <input type="submit" class="waves-effect waves-light btn" value="next" onClick="pageUP()">
                                 </form>



                                 SELECT COUNT(DISTINCT id) from owner_route_tasks WHERE added_date = '2017-07-01'
                                 SELECT COUNT(id) from owner_route_drivers WHERE date = '2017-07-01'




                                   cm_name  = row['Company Name']
            cus_name = row['Customer Name']
            print data
            print cm_name
            print cus_name

        query = """
        SELECT pick_address, delivery_address from jobs where customer_comp_name = '%s' and customer_name = '%s'
                """% (cm_name, cus_name)
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            pa = row['pick_address']
            da = row['delivery_address']
            
            print pa
            print da
        counter += 1




        SELECT DISTINCT(o.proof_picture), o.job_code, o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname) 
        from drivers d where d.id = o.assigned_driver) as Driver,
        (select d.cellphone from drivers d where d.id = o.assigned_driver) as "driver_phone",
        (select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #", 
        (select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name", 
        (select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#",
        (select jobs.unit_pay from jobs where id = o.id) as "type",
        (select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) from owners ow where ow.id = o.owner_id )
        as "Owner", o.ticket_number, c.company as "Customer Name" from owner_route_tasks o  
        left join job_details jd on jd.job_code = o.job_code join jobs j on j.id = jd.job_id join customers c  on 
        c.id = j.customer_id  WHERE o.task_status = 'Completed' and o.date = '2018-01-11' ORDER by o.ending_time desc LIMIT 1 offset 1



        SELECT DISTINCT(o.proof_picture), o.job_code, o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname) 
        from drivers d where d.id = o.assigned_driver) as Driver,
        (select d.cellphone from drivers d where d.id = o.assigned_driver) as "driver_phone",
        (select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #", 
        (select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name", 
        (select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#",
        (select job_details.id from job_details where id = t.id) as "test",
        (select jobs.unit_pay from jobs where id = o.id) as "type",
        (select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) from owners ow where ow.id = o.owner_id )
        as "Owner", o.ticket_number, c.company as "Customer Name" from owner_route_tasks o  
        left join job_details jd on jd.job_code = o.job_code join jobs j on j.id = jd.job_id join customers c  on 
        c.id = j.customer_id  WHERE o.task_status = 'Completed' and o.date = '2018-01-11' ORDER by o.ending_time desc LIMIT 1 offset 1


        select jobs.unit_pay from jobs join owners on owners.id = jobs.id




        <div class="btn-group">
						  <p>
							<input type="checkbox" id="i1" />
							<label for="i1">Verify Image</label>
							<p id="i1"></p>
						  |
							<input type="checkbox" id="i2" />
							<label for="i2">Retake Request</label>
							<p id="i2"></p>
						  </p>
					</div>


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


        SELECT DISTINCT(o.proof_picture), o.job_code, o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname) 
        from drivers d where d.id = o.assigned_driver) as Driver,
        (select d.cellphone from drivers d where d.id = o.assigned_driver) as "driver_phone",
        (select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #", 
        (select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name", 
        (select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#",
        (select jobs.unit_pay from jobs where id = o.owner_id) as "type1",
        (select jobs.pick_address from jobs where id = o.owner_id) as "type2",
        (select jobs.delivery_address from jobs where id = o.owner_id) as "type3",
        (select image_verified.confirmed from image_verified where cell = ow.cell_phone) as "type4",
        (select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) from owners ow where ow.id = o.owner_id )
        as "Owner", o.ticket_number, c.company as "Customer Name" from owner_route_tasks o  
        left join job_details jd on jd.job_code = o.job_code join jobs j on j.id = jd.job_id join customers c  on 
        c.id = j.customer_id  WHERE o.task_status = 'Completed' and o.date = '2017-07-01' ORDER by o.ending_time desc LIMIT 1 offset 1







		SELECT DISTINCT(o.proof_picture), o.id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname) 
		from drivers d where d.id = o.assigned_driver) as Driver,
        (select d.cellphone from drivers d where d.id = o.assigned_driver) as "Driver's Phone#",
        (select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #",
		(select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name", 
		(select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#", 
		(select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) 
		 from owners ow where ow.id = o.owner_id ) as "Owner", o.ticket_number, c.company as "Customer Name" 
		 from owner_route_tasks o  left join job_details jd on jd.job_code = o.job_code join jobs j 
		 on j.id = jd.job_id join customers c on c.id = j.customer_id join owner_route_task_details 
		 on owner_route_task_details.owner_id = o.owner_id   WHERE (o.proof_picture <> 'Null' || o.proof_picture <> '') 
		 and o.date = '2018-02-06' and (o.task_verification_status = '0' || o.task_verification_status ='2') 
		 order by owner_route_task_details.action_timestamp desc


		 	SELECT DISTINCT(o.proof_picture), o.id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname) 
		from drivers d where d.id = o.assigned_driver) as Driver,
        (select d.cellphone from drivers d where d.id = o.assigned_driver) as "Driver's Phone#",
        (select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #",
		(select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name", 
		(select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#", 
		(select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) 
		 from owners ow where ow.id = o.owner_id ) as "Owner", o.ticket_number, c.company as "Customer Name" 
		 from owner_route_tasks o  left join job_details jd on jd.job_code = o.job_code join jobs j 
		 on j.id = jd.job_id join customers c on c.id = j.customer_id join owner_route_task_details 
		 on owner_route_task_details.owner_id = o.owner_id   WHERE (o.proof_picture <> 'Null' || o.proof_picture <> '') 
		 and o.date = '%s' and (o.task_verification_status = '0' || o.task_verification_status ='2') 
		 order by owner_route_task_details.action_timestamp desc LIMIT 1




		 SELECT DISTINCT(o.proof_picture), o.id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname) 
		from drivers d where d.id = o.assigned_driver) as Driver,
        (select d.cellphone from drivers d where d.id = o.assigned_driver) as "Driver's Phone#",
        (select t.company_truck_number from trucks t where t.id = o.assigned_truck) as "Company Truck #",
		(select ow.trucking_company_name from owners ow where ow.id = o.owner_id ) as "Company Name", 
		(select ow.cell_phone from owners ow where ow.id = o.owner_id ) as "Owner Phone#", 
		(select concat(ow.fname, ' ', ow.mname, ' ', ow.lname) 
		 from owners ow where ow.id = o.owner_id ) as "Owner", o.ticket_number, c.company as "Customer Name" 
		 from owner_route_tasks o  left join job_details jd on jd.job_code = o.job_code join jobs j 
		 on j.id = jd.job_id join customers c on c.id = j.customer_id join owner_route_task_details 
		 on owner_route_task_details.owner_id = o.owner_id   WHERE (o.proof_picture <> 'Null' || o.proof_picture <> '') 
		 and o.date = '%s' and (o.task_verification_status = '0' || o.task_verification_status ='2') 
		 order by owner_route_task_details.action_timestamp desc LIMIT 1 offset %s


		 SELECT DISTINCT(o.proof_picture),o.id, o.job_code, o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname) 
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
		c.id = j.customer_id  WHERE o.proof_picture <> 'Null' and o.date = '%s' ORDER by o.ending_time asc LIMIT 1 offset %s





		socket.on('info', function(msg) {
					console.log(coo);
					page_max = Number(page_max);
					console.log(page_max);
					if (msg != coo) {
						page_max += 1;
						console.log(page_max);
						$('#page_max').html(page_max);
					}
                 });



	for row in results:
			t1 = row['Driver']
			t2 = row['job_code']
			t0 = row['id']
			t3 = row['ending_time']
			print t1
			#message = 'Lastest Ticket' + '-' +  str(t1)  + '-'+  str(t2)
			payload1 = 'Lastest Ticket' + '-' +  str(t1)  + '-'+  str(t2)
			payload2 = t0
			socketio.emit('info', payload2)
			socketio.emit('message', payload1)




			def background_thread():
	while True:
		current_date = '2018-02-06'
		cursor = db.cursor(pymysql.cursors.DictCursor)
		query = """
		select count(owner_id) from
			(SELECT DISTINCT(o.proof_picture), o.id,o.ending_time, o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname)
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
		cursor.execute(query)
		results = cursor.fetchall()
		for row in results:
			thecount = row['count(owner_id)']
			socketio.emit('count', thecount)
			socketio.sleep(10)
	


	def background_thread():
	while True:
		current_date = '2018-02-06'
		cursor = db.cursor(pymysql.cursors.DictCursor)
		query = """
		select count(owner_id) from
			(SELECT DISTINCT(o.proof_picture), o.id,o.ending_time, o.owner_id, o.qty, (select CONCAT(d.fname, ' ', d.mname, ' ', d.lname)
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
		cursor.execute(query)
		results = cursor.fetchall()
		for row in results:
			thecount = row['count(owner_id)']
			socketio.emit('count', thecount)
			socketio.sleep(10)
	





	def background_thread():
	while True:
		current_date = '2018-02-06'
		cursor = db.cursor(pymysql.cursors.DictCursor)
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
		cursor.execute(query)
		results = cursor.fetchall()
		for row in results:
			thecount = row['count(owner_id)']
			socketio.emit('count', thecount)
			socketio.emit('info',the_id)
			socketio.emit('message',ticket)
			socketio.sleep(10)





				 socket.on('info', function(msg) {
                    page_max = Number(page_max);
					console.log(page_max);
					if (msg != the_id) {
						page_max += 1;
						console.log(page_max);
						//$('#page_max').html(page_max);
					}
                 });





				 '''
def count_thread():
	while True:
		current_date = '2018-02-06'
		cursor = db.cursor(pymysql.cursors.DictCursor)
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
		cursor.execute(query)
		results = cursor.fetchall()
		for row in results:
			thecount = row['count(owner_id)']
			socketio.emit('count', thecount)
			socketio.sleep(10)
''' 