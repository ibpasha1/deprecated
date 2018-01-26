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