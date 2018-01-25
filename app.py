from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import time
import json
import os
import sys
time.strftime('%Y-%m-%d %H:%M:%S')
db = pymysql.connect(host='localhost', port=8889, user='root', passwd='root', db='bull_local')
app = Flask(__name__)


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
                'qty': row['qty'],
                'is_completed': row['is_completed'],
                'owner_id': row['owner_id'],
                'truck_id': row['truck_id'],
                'proof_picture': row['proof_picture'],
                'signature_picture': row['signature_picture']
            })
    except:
        print "Error:" , sys.exc_info()[0]
    return render_template('voo.html',data=data)
    return jsonify('data',data)




if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)