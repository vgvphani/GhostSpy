#!flask/bin/python
from __future__ import print_function
import argparse
from influxdb.client import InfluxDBClientError
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import datetime
from flask import url_for
import random, threading, webbrowser
import subprocess
from influxdb import InfluxDBClient
from influxdb import DataFrameClient
import time
from functools import wraps
from flask import request, Response, render_template
import re

host='localhost'
port=8086
user = 'root'
password = 'root'
DBNAME = 'db1'
DBNAME2 = 'db2'
client = InfluxDBClient(host, port, user, password, DBNAME)
client.switch_database(DBNAME)



metric = "tuple"



app = Flask(__name__)
proc = subprocess.Popen(['python','spectrelink.py'], stdout=subprocess.PIPE)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'password'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated



@app.route('/tasks', methods=['GET'])
@requires_auth
def get_tasks1():
    
  

 
    query = "SELECT * from {0}".format(metric)
    result = client.query(query, database=DBNAME)	
   #result = "%s" %result
    
    cpoint = list(result.get_points(measurement= metric))
    		
    return jsonify({'tuples':str(cpoint)})



@app.route('/last', methods=['GET'])
@requires_auth
def get_tasks2():

    query = "SELECT * from {0} order by desc limit 1".format(metric)
    result = client.query(query, database=DBNAME)	
   #result = "%s" %result
    
    cpoint = list(result.get_points(measurement= metric))
   # sess= cpoint[0]['last_value']
    		
    return jsonify({'latest':str(cpoint[0])})


@app.route('/stop', methods=['GET'])
@requires_auth
def stoptoplink():

    proc.kill()
    		
    return jsonify({'status':'Tophost will stop now'})



@app.route('/stream/<string:stream_name>', methods=['GET'])
@requires_auth
def change_stream(stream_name):
    stream = stream_name

    proc.kill()

    banner=""
    
    try:
	f = open("spectre.conf",'r+')
	banner="Changed Stream"
	x=f.read()
    	y = re.split("\n",x)
    	z=[]
    	for i in range(len(y)):
       	 if(y[i])!='':
                z.append(y[i])
    	try:
		z[3]=stream_name
        except:
		pass
    	f.seek(0)
    	for i in range(len(z)):
		fw="%s\n"%z[i]
		f.write(fw)
    	f.close()
    except:
	banner="Unable to Open file spectre.conf"
    
    global proc
    proc = subprocess.Popen(['python','spectrelink.py'], stdout=subprocess.PIPE)

    return jsonify({'status':banner})

@app.route('/ma/<string:ma_name>', methods=['GET'])
@requires_auth
def change_ma(ma_name):

    banner=""
    
    try:
	f = open("spectre.conf",'r+')
	banner="Changed Interface"
	x=f.read()
    	y = re.split("\n",x)
    	z=[]
    	for i in range(len(y)):
     	   if(y[i])!='':
                z.append(y[i])
    	try:
		z[0]=ma_name
    	except:
		pass
    	f.seek(0)
    	for i in range(len(z)):
		fw="%s\n"%z[i]
		f.write(fw)
    	f.close()
    except:
	banner="Unable to Open file spectre.conf"
	

    
    global proc
    proc = subprocess.Popen(['python','spectrelink.py'], stdout=subprocess.PIPE)

    return jsonify({'status':banner})


@app.route('/status', methods=['GET'])
@requires_auth
def get_status(
):
    banner=''
    
    try:
	f = open("spectre.conf",'r+')
	x=f.read()
    	y = re.split("\n",x)
    	z=[]
    	for i in range(len(y)):
    	    if(y[i])!='':
                z.append(y[i])
    	f.close()
	return jsonify({'ma':z[0], 'stream': z[3]})
    except:
	banner="Unable to Open file spectre.conf"
	return jsonify({'status':banner})



@app.route('/matuple', methods=['GET'])
@requires_auth
def get_tasks3():

    query = "SELECT * from {0} order by desc limit 1".format(metric)
    result = client.query(query, database=DBNAME)	
   #result = "%s" %result
    
    cpoint = list(result.get_points(measurement= metric))

    line = cpoint[0]['spdp'].replace('[ [','')
    line = line.replace(']]','')
    line = line.replace('],[',';')                  ############# Replace unwanted symbols 
    fine = re.split(';',line) 
    fine1= fine[0].replace('"','')                         ############# Separate the tuples
    fine1 = "%s" %fine1
    x = re.split(',',fine1) 

    #fine1 = fine1.replace("'",'')
   # sess= cpoint[0]['last_value']'''
    
    return jsonify({'matuple': x[0]})

@app.route('/min', methods=['GET'])
@requires_auth
def get_tasks4():

    query = "SELECT * from {0} order by desc limit 1".format(metric)
    result = client.query(query, database=DBNAME)	
   #result = "%s" %result
    
    cpoint = list(result.get_points(measurement= metric))

    line = cpoint[0]['spdp'].replace('[ [','')
    line = line.replace(']]','')
    line = line.replace('],[',';')                  ############# Replace unwanted symbols 
    fine = re.split(';',line) 
    fine1= fine[len(fine)-1].replace('"','')                         ############# Separate the tuples
    fine1 = "%s" %fine1
    x = re.split(',',fine1) 

    #fine1 = fine1.replace("'",'')
   # sess= cpoint[0]['last_value']'''
    
    return jsonify({'minptuple': x[0],'packet':int(x[1])})

@app.route('/max', methods=['GET'])
@requires_auth
def get_tasks():

    query = "SELECT * from {0} order by desc limit 1".format(metric)
    result = client.query(query, database=DBNAME)	
   #result = "%s" %result
    
    cpoint = list(result.get_points(measurement= metric))

    line = cpoint[0]['spdp'].replace('[ [','')
    line = line.replace(']]','')
    line = line.replace('],[',';')                  ############# Replace unwanted symbols 
    fine = re.split(';',line) 
    fine1= fine[0].replace('"','')                         ############# Separate the tuples
    fine1 = "%s" %fine1
    x = re.split(',',fine1) 

    #fine1 = fine1.replace("'",'')
   # sess= cpoint[0]['last_value']'''
    
    return jsonify({'maxptuple': x[0],'packet':int(x[1])})

@app.route('/pax', methods=['GET'])
@requires_auth
def get_tasks6():

    query = "SELECT * from {0} order by desc limit 1".format(metric)
    result = client.query(query, database=DBNAME)	
   #result = "%s" %result
    
    cpoint = list(result.get_points(measurement= metric))

    line = cpoint[0]['spdp'].replace('[ [','')
    line = line.replace(']]','')
    line = line.replace('],[',';')                  ############# Replace unwanted symbols 
    fine = re.split(';',line)
    a=0
    for i in range(len(fine)): 
    	x = re.split(',',fine[i])
	y=x[1]
	y=int(y)
    	a=a+y

    return jsonify({'Total Packets exchanged': a})


if __name__ == '__main__':
    app.run('0.0.0.0',5000)
