#display out put line by line
from __future__ import print_function
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import datetime
import random
import time
#from flask import jsonify
import argparse
import subprocess
import re
import sys

USER = 'root'
PASSWORD = 'root'
DBNAME = 'db1'
DBNAME2 = 'db2'
DBNAME3 = 'db3'
host='localhost'
port='8086'
metric = "tuple"

try:
	clientn = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)
	query = "SELECT last(*) from {0}".format(metric)
	result = clientn.query(query, database=DBNAME)
	cpoint = list(result.get_points(measurement=metric))
	sess=cpoint[0]['last_value']
	sess = sess+1
	print(sess)
except:
	sess=0




try:
	fo = open("spectre.conf", "r")
except:
        fo = open("spectre.conf", "w+")

x=fo.read()
y = re.split("\n",x)
z=[]
for i in range(len(y)):
        if(y[i])!='':
                z.append(y[i])
fo.close()

mylist= ['./tophosts','-s']
mylist.append(z[0])
if z[1]== 'apple':
	pass
else:
#	fine = re.split(';',line)
	mylist.append('-l')
	mylist.append(z[1])
#	fine = re.split(';',line)
if z[2]== 'apple':
	pass
else:
#	fine = re.split(';',line)
	mylist.append('-p')
	mylist.append(z[2])
mylist.append(z[3])
print (mylist)
proc = subprocess.Popen(mylist,stdout=subprocess.PIPE)
#proc1 =fine = re.split(';',line)     subprocess.Popen(['/tophosts' ,'-s','eth1','01::72'],stdout=subprocess.PIPE)
#proc1 = subprocess.popen(['./tophosts','-l',
#works in python 3.0+
#for line in proc.stdout:
A1=[]
A2=[]
A3=[]
A4=[]
flag="FALSE"
for line in iter(proc.stdout.readline,''):
	line = line.rstrip()
	if (line==''or line=='[]'):
		pass
        else:
		topout = line
		line = line.replace('[ [','')
		line = line.replace(']]','')
		line = line.replace('],[',';')                  ############# Replace unwanted symbols 
		fine = re.split(';',line)                               ############# Separate the tuples
		fine1 = "%s" %fine
		fine1 = fine1.replace("'",'')		
		
		pointValues = {
		"measurement": metric,
			'fields':  {
			'value': sess,
			},
			'tags': {
			"spdp": topout,
				},
			}
		dot = [pointValues]
		retention_policy="server_data2"
		client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)
		client.create_retention_policy(retention_policy, '1h', 2, default=True)
		client.write_points(dot,retention_policy=retention_policy)
		time.sleep(0.2)
					
		for i in range (len(fine)):
			value1 = fine[i]                                        ############# Taking the first term, needs to be looped for n terms
			value1 = re.split(',',value1)                           ############# Separate the tophosts and packet number
			ippart = value1[0]                                      ############# Taking out the src-prot-dst part
			pktpart = value1[1]; pktpart = pktpart.replace(' ','')  ############# Taking out the packet part
         		utime = int(time.time())
			j=0	
			while(j<len(A1)):
				if(ippart==A1[j]):
				#	print ("match")
		        		d= abs(int(pktpart)-int(A2[j]))
					A2[j]= int(pktpart)
                        		if(A3[j]<(utime)):
		           			a=float(A3[j])
                           			b=utime
                           			c= b-a

			   			A3[j]=utime

                           			result = float(d/c)
                           			pointValues = {
						"measurement": metric,
						'fields':  {
						'value': result,
						},
						'tags': {
						"tup": ippart,
						"stream": z[3],
						},
						}
						dotx = [pointValues]
						retention_policy="server_data2"
						client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME2)
						client.create_retention_policy(retention_policy, '1h', 2, default=True)
						client.write_points(dotx,retention_policy=retention_policy)  


						pointValues = {
						"measurement": metric,
						'fields':  {
						'value': (float(pktpart)/(sess + 1)),
						},
						'tags': {
						"tup": ippart,
						"stream": z[3],
						},
						}
						doty = [pointValues]

						client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME3)
						client.create_retention_policy(retention_policy, '1h', 2, default=True)
						client.write_points(doty,retention_policy=retention_policy)                       
			   			
                     
			   			flag="TRUE"
			   			break
				else:
					flag="FALSE"
				j+=1

			if(flag=="FALSE"):
				A1.append(ippart)
				A2.append(pktpart)
				A3.append(utime)





	
                
			
		#	print (".")
		sess = sess + 1;
			
