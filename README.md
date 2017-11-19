# ghostspy
gHOSTspy : noun (pl. ghostspies) UK:/g??stspa?/ US:/go?stspa?/ An application made by Spectre to spy on Hosts.
## USER DOCUMENT VR 1.0


	########         ####        ####       ######          ######  ###############     ######   #######       ###        ###
      ####   ####        ####        ####     ####  ####      #####           ###         #####      ###    ###     ###      ###
     ####     ####       ####        ####    ####     ####  ####              ###      ####          ###      ###    ###    ###
     ####		 ####        ####   ####       ####  ####             ###        ####        ###     ###      ###  ###
     ####     #########  ################   ####       ####    ####           ###          ####      ###   ###         ######
     ####     #########  ################   ####       ####       ####        ###            ####    ######             ####
      ####    ####  ###  ####        ####    ####     ####         #####      ###             #####  ###                ####
      ####  ####   ###  ####        ####     ####   ####        #####        ###           #####    ###                ####
	########    ###  ####        ####       ######        #######         ###        #######     ###                ####


- Developers : Spectre005 : K. Lohit Srihas, Robin P. Joseph, J. Rohith Reddy, R. Rajashekar Reddy, G. Phani Varanasi 


INDEX :

1. User Guide :

2. Installation :

3. REST-API manual :

4. Acknowledgement :


I. USER GUIDE :


** About TOPHOST:

=> Tophost is a consumer that interfaces with DPMI streams.
=> Tophost takes arguments as interface and stream name (along with optional IP and port number).
=> The output of tophost consists of set of tuples for every 10 seconds.
=> Each tuple has source IP, protocol, destination IP, number of packets.
=> The tuples are in the descending order of number of packets.

** Data available to the user via REST-API

=> Most active tuple: The tuple that contains the most number of packets in a sample .
=> Maximum no. of packets: Maximum value of number of packets in a sample.
=> Minimum no. of packets: Minimum value of number of packets in a sample.
=> Average number of packets: Average of the packets of a tuple among all samples.
=> Packets exchanged : The total packets exchanged in one sample. 
=> Last sample : The last sampled value from Tophost.
=> All samples : All the samples in the database
=> Status : The interface and stream that tophost listens to.
=> Packet rate : The rate of change of packets of a tuple from Tophost


** Additional features:

=> Password protection
=> Data upto 300 sample points
=> Stream selection
=> Interface selection
=> Graphs via Grafana
=> Stops the background tophost process



II. INSTALLATION :

	A. SYSTEM REQUIREMENTS :
		1. InfluxDB
		2. InfluxDB python Module
		3. Flask Python Module
		4. Python
		5. Pip
		6. Curl
		7. libqd-dev
		8. Tophost
		9. Grafana
		10. DPMI stream
		11. Shared Key

	B. Steps to install :

		1. Tophost Consumer :
			In the terminal:

			>cd SPECTRE005/consumer-tophost
			>sudo make

		2. Libcaputils :
			- use the below link to install libcaputils 
			link => https://github.com/DPMI/libcap_utils

		3. InfluxDB :
			- In the terminal :

			>wget https://dl.influxdata.com/influxdb/releases/influxdb_1.0.2_amd64.deb
			>sudo dpkg -i influxdb_1.0.2_amd64.deb
			>influx
			>create database db1
			>create database db2
			>create database db3

		4. Grafana :
			- In the terminal :
	
			>wget https://grafanarel.s3.amazonaws.com/builds/grafana_3.1.1-1470047149_amd64.deb
			>sudo apt-get install -y adduser libfontconfig
			>sudo dpkg -i grafana_3.1.1-1470047149_amd64.deb
			
			- Importing the Dashboard and Data Sources:			
			
			-> Add two data sources with name = 'spectre', database = 'db2' and name = 'spectreavg', database = 'db3'
			-> Click on the home button in grafana
			-> Select 'import' and import the spectredash.json file

		5. Ghostspy REST-server :
			- To install REST server dependencies, In the terminal :
			>pip install flask
			>sudo apt-get install python-influxdb
			
			- To start the REST server
			>cd SPECTRE005/consumer-tophost
			>sudo python sprectrerest.py 



III. RESTFUL API

** The REST server runs on port 5000 and gives output in json format. The requests need to be made using curl or a web browser. 
The default username and password are admin and password.
The following requests are served by GHOSTSPY server:
	
	1. To display all samples :

		>curl -u admin http://localhost:5000/tuples

	2. To display last sample :

		>curl -u admin http://localhost:5000/last 
 
	3. To stop the tophost :

		>curl -u admin http://localhost:5000/stop

	4. To change the stream of tophost :

		>curl -u admin http://localhost:5000/stream/<stream_name>
		
	5. To change the interface of tophost :

		>curl -u admin http://localhost:5000/ma/<ma_name>

	6. To get the most active tuple :

		>curl -u admin http://localhost:5000/matuple

	7. To get the minimum number of packets transfered in the latest sample :

		>curl -u admin http://localhost:5000/min

	8. To get the maximum number of packets transfered in the latest sample :

		>curl -u admin http://localhost:5000/max

	9. To get the total number of packets transfered in the latest sample :

		>curl -u admin http://localhost:5000/pax

	10. To stop the background tophost process :

		>curl -u admin http://localhost:5000/stop

	11. To get the status ie., the interface and stream Tophost listens to:

		>curl -u admin http://localhost:5000/status


IV. ACKNOWLEDGEMENTS

This project could not be completed without the guidance of Patrik Arlos, Professor of BTH, Karlskrona, Sweden. Spectre005 would like to express our gratitude
in the form of this acknowledgement.
