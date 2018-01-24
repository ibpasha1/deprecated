from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import time
import json
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
       cursor = db.cursor()
       sql = "SELECT * FROM job_details \
       WHERE date = '%s'" % (date)
       
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            job_id       = row[1]
            job_code     = row[2]
            qty          = row[4]
            is_completed = row[8]
            
        sql = "SELECT * FROM owner_route_task_details \
        WHERE job_code = '%s'" % (job_code)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            owner_id     = row[3]
            truckid      = row[9]
            data.append(row)
    except:
        print ("Error: unable to fetch data")
    return render_template('voo.html',data=data)




if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)