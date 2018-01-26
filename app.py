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
account_sid = "AC14da0799655b1ce7bbddefb5ead5ab89"
auth_token  = "67edc7ccf6675e798d2c6f88a93e0851"
client = Client(account_sid, auth_token)
PEOPLE_FOLDER = os.path.join('static', 'people_photo')
time.strftime('%Y-%m-%d %H:%M:%S')
db = pymysql.connect(host='localhost', port=8889, user='root', passwd='root', db='bull_local')
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
           to=2409387539,
           from_="+17727424910",
           body="Please retake your picture--sorry testing---Disregard!")
    except:
        print "Error:" , sys.exc_info()[0]
    return render_template('voo.html',data=data)
    return jsonify('data',data)


if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)